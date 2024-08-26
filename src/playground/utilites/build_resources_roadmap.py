from collections import deque
from dataclasses import dataclass, field
from pprint import pprint
from typing import List, Optional, Dict

import networkx as nx
from matplotlib import pyplot as plt
from pydantic import TypeAdapter
from pyvis.network import Network

from src.playground.characters import SkillType, EquipmentSlot
from src.playground.characters.proxy.proxy_character import ProxyCharacter
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Item
from src.playground.items.crafting import ItemDetails
from src.playground.monsters import Monster
from src.playground.resources import Resource
from src.playground.utilites.equipment_estimator import EquipmentEstimator
from src.playground.utilites.fight_results import FightEstimator

SKILL_MAX_LEVEL = 30
CHARACTER_MAX_LEVEL = 30


@dataclass
class CharacterInfo:
    level: int


@dataclass
class SkillInfo:
    level: int
    skill: SkillType


@dataclass
class NodeInfo:
    target_item: Optional[Item] = None
    skill_info: Optional[SkillInfo] = None
    resource_info: Optional[Resource] = None
    monster_info: Optional[Monster] = None
    character_info: Optional[CharacterInfo] = None


@dataclass
class Node:
    node_info: Optional[NodeInfo] = field(default_factory=NodeInfo)
    parent: Optional["Node"] = None
    children: Optional[List["Node"]] = field(default_factory=list)

    def add_child(self, node: "Node"):
        node.parent = self
        self.children.append(node)


NodeInfoAdapter = TypeAdapter(NodeInfo)


def from_json(obj, adapter=NodeInfoAdapter):
    return adapter.validator.validate_python(obj)


def to_json(obj, adapter=NodeInfoAdapter):
    return adapter.dump_python(obj)


def get_code(node_info: NodeInfo):
    code = None
    codes = [node_info.target_item is not None, node_info.resource_info is not None,
             node_info.monster_info is not None, node_info.skill_info is not None,
             node_info.character_info is not None]
    assert sum(codes) == 1, codes
    if node_info.target_item:
        code = f"item:{node_info.target_item.code}"
    elif node_info.resource_info:
        code = f"resource:{node_info.resource_info.code}"
    elif node_info.monster_info:
        code = f"monster:{node_info.monster_info.code}"
    elif node_info.skill_info is not None:
        skill = node_info.skill_info
        code = f"{skill.skill.value}:{skill.level}"
    elif node_info.character_info is not None:
        code = f"character:{node_info.character_info.level}"
    return code


class ResourcesRoadmap:
    def __init__(self, world: PlaygroundWorld, items: List[ItemDetails], winrate=0.95):
        self.items = items
        self.world = world
        self.winrate = winrate

    def _resource_roadmap(self, root_node: NodeInfo, graph: nx.DiGraph,
                          nodes_dict: Dict[str, NodeInfo]):
        resources = self.world.resources.resources
        for skill_type in SkillType:
            parent_node = root_node
            for level in range(1, SKILL_MAX_LEVEL + 1):
                skill_node = NodeInfo(skill_info=SkillInfo(level=level, skill=skill_type))
                has_resource_at_level = False
                for resource in resources:
                    if resource.skill == skill_type and resource.level == level:
                        has_resource_at_level = True
                        resource_node = NodeInfo(resource_info=resource)
                        nodes_dict[get_code(resource_node)] = resource_node
                        graph.add_edge(get_code(skill_node), get_code(resource_node))

                        for drop in resource.drops:
                            drop_node = NodeInfo(target_item=drop.item)
                            drop_code = get_code(drop_node)
                            # If we already can gather item skip it
                            if drop_code not in nodes_dict:
                                nodes_dict[drop_code] = drop_node
                                graph.add_edge(get_code(resource_node), drop_code)
                if has_resource_at_level:
                    nodes_dict[get_code(skill_node)] = skill_node
                    graph.add_edge(get_code(parent_node), get_code(skill_node))
                    parent_node = skill_node

    def _recursive_craft(self, root_node: NodeInfo, graph: nx.DiGraph,
                         nodes_dict: Dict[str, NodeInfo]):
        crafting_items = self.world.item_details.get_crafts()
        for skill_type in SkillType:
            parent_node = root_node
            skill_items = [item for item in crafting_items if item.craft.skill == skill_type]
            for level in range(1, SKILL_MAX_LEVEL + 1):
                level_items = [item for item in skill_items if item.level == level]
                if level_items:
                    skill_node = NodeInfo(skill_info=SkillInfo(level=level, skill=skill_type))
                    nodes_dict[get_code(skill_node)] = skill_node
                    graph.add_edge(get_code(parent_node), get_code(skill_node))
                    for level_item in level_items:
                        item_node = NodeInfo(target_item=level_item)
                        crafted_item_code = get_code(item_node)
                        # If we already can craft item skip it
                        if crafted_item_code not in nodes_dict:
                            nodes_dict[crafted_item_code] = item_node
                            graph.add_edge(get_code(skill_node), crafted_item_code)
                            for item2craft in level_item.craft.items:
                                craft_item_node = NodeInfo(target_item=item2craft.item)
                                graph.add_edge(get_code(craft_item_node), crafted_item_code)
                    parent_node = skill_node

    def _find_accessible_nodes(self, graph: nx.DiGraph, available_nodes: List[str],
                               remaining_nodes: List[str]):
        available_nodes = available_nodes.copy()
        nodes_queue = deque(remaining_nodes)
        # Update available_items
        while len(nodes_queue) > 0:
            is_all_not_complete = True
            for _ in list(nodes_queue):
                node = nodes_queue.pop()
                is_complete = True
                for succ in graph.predecessors(node):
                    if succ not in available_nodes:
                        is_complete = False
                        break
                if is_complete:
                    is_all_not_complete = False
                    nodes_queue.append(node)
                else:
                    nodes_queue.appendleft(node)
            # If all task can't be complete we'll break loop
            if is_all_not_complete:
                break

            current_node = nodes_queue.pop()

            is_complete = True
            # If all predecessors is complete we can move forward
            for succ in graph.predecessors(current_node):
                if succ not in available_nodes:
                    is_complete = False
                    break
            # Add new nodes
            if is_complete:
                available_nodes.append(current_node)
                for adj_node in graph.neighbors(current_node):
                    nodes_queue.append(adj_node)
            else:
                nodes_queue.appendleft(current_node)

        return available_nodes, list(nodes_queue)

    def _recursive_monsters(self, root_node: NodeInfo, graph: nx.DiGraph,
                            nodes_dict: Dict[str, NodeInfo]):
        monsters = self.world.monsters.monsters
        fight_estimator = FightEstimator(world=self.world)

        available_nodes = [get_code(root_node)]
        remaining_nodes = available_nodes.copy()

        for monster in sorted(monsters, key=lambda mnstr: mnstr.stats.level):
            available_nodes, remaining_nodes = self._find_accessible_nodes(graph, available_nodes, remaining_nodes)
            available_nodes, remaining_nodes = list(set(available_nodes)), list(set(remaining_nodes))
            available_items = [
                self.world.item_details.get_item(nodes_dict[node_info].target_item) for
                node_info in available_nodes if nodes_dict[node_info].target_item is not None]

            equipment_estimator = EquipmentEstimator(available_items)
            optimal_equipment = equipment_estimator.optimal_vs_monster(None,
                                                                       monster=monster)
            proxy_character = ProxyCharacter(monster.stats.level,
                                             optimal_equipment,
                                             world=self.world)
            simulation_results = fight_estimator.simulate_fights(proxy_character, monster)
            print(proxy_character.stats)
            print(monster.stats)
            print(monster.code, monster.stats.level, simulation_results.success_rate,
                  simulation_results.result.monster_hp, simulation_results.result.character_hp,
                  simulation_results.result.turns, simulation_results.result.spent_consumables,
                  {slot: value.code for slot, value in optimal_equipment.items()})
            # We think monster has been beaten
            # Add monster node
            monster_node = NodeInfo(monster_info=monster)
            graph.add_edge(get_code(root_node), get_code(monster_node))
            nodes_dict[get_code(monster_node)] = monster_node
            remaining_nodes.append(get_code(monster_node))
            # Can add drops
            for drop in monster.drops:
                drop_node = NodeInfo(target_item=drop.item)
                graph.add_edge(get_code(monster_node), get_code(drop_node))
                remaining_nodes.append(get_code(drop_node))
                if get_code(drop_node) not in nodes_dict:
                    nodes_dict[get_code(drop_node)] = drop_node

            root_node = monster_node
            # TOOD add dependency of items to beat

    def create_items_roadmap(self):

        root_node = NodeInfo(character_info=CharacterInfo(1))
        DG = nx.DiGraph()
        nodes_dict: Dict[str, NodeInfo] = {get_code(root_node): root_node}
        DG.add_node(get_code(root_node), **to_json(root_node))
        self._resource_roadmap(root_node, DG, nodes_dict)
        self._recursive_craft(root_node, DG, nodes_dict)
        self._recursive_monsters(root_node, DG, nodes_dict)
        return DG, nodes_dict


def graph(graph: nx.DiGraph):
    nt = Network("1080px", "1920px", directed=True, neighborhood_highlight=True, select_menu=True, filter_menu=True)
    nt.from_nx(graph)
    nt.show("nx.html", notebook=False)
    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
