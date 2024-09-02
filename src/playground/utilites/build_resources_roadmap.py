import logging
from collections import deque, Counter
from dataclasses import dataclass, field
from typing import List, Optional, Dict

import networkx as nx
from matplotlib import pyplot as plt
from pydantic import TypeAdapter
from pyvis.network import Network

from src.playground.characters import SkillType, EquipmentSlot
from src.playground.characters.proxy.proxy_character import ProxyCharacter
from src.playground.constants import SKILL_MAX_LEVEL, CHARACTER_MAX_LEVEL
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Item, Items
from src.playground.items.crafting import ItemDetails
from src.playground.monsters import Monster
from src.playground.resources import Resource
from src.playground.utilites.equipment_estimator import EquipmentEstimator
from src.playground.utilites.fight_results import FightEstimator
from src.playground.utilites.np_hard_equipment_estimator import NPHardEquipmentEstimator


logger = logging.getLogger(__name__)


@dataclass
class CharacterInfo:
    level: int


@dataclass
class SkillInfo:
    level: int
    skill: SkillType


@dataclass
class TaskInfo:
    level: int


@dataclass
class NodeInfo:
    target_item: Optional[Item] = None
    skill_info: Optional[SkillInfo] = None
    resource_info: Optional[Resource] = None
    monster_info: Optional[Monster] = None
    character_info: Optional[CharacterInfo] = None
    task_info: Optional[TaskInfo] = None


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
             node_info.character_info is not None, node_info.task_info is not None]
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
    elif node_info.task_info is not None:
        code = f"task:{node_info.task_info.level}"
    return code


class ResourcesRoadmap:
    def __init__(self, world: PlaygroundWorld, items: List[ItemDetails], winrate=0.99):
        self.items = items
        self.world = world
        self.winrate = winrate
        self.readable = False

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
                    if self.readable:
                        # Make graph readable
                        character_node = NodeInfo(character_info=CharacterInfo(level=level))
                        nodes_dict[get_code(skill_node)] = skill_node
                        graph.add_edge(get_code(character_node), get_code(skill_node))
                        graph.add_edge(get_code(parent_node), get_code(skill_node))
                        parent_node = skill_node
                    else:
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
                    if self.readable:
                        # Make graph readable
                        character_node = NodeInfo(character_info=CharacterInfo(level=level))
                        graph.add_edge(get_code(character_node), get_code(skill_node))
                        graph.add_edge(get_code(parent_node), get_code(skill_node))
                    else:
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
        # Check nodes
        for edge in graph.edges():

            assert isinstance(edge, (list, tuple))
            assert edge[0] != edge[1], edge
        counter = Counter(nodes_queue)
        has_duplicate = False
        for node, count in counter.items():
            if count > 1:
                has_duplicate = True
                logger.error(f"Node {node} is duplicated")
        if has_duplicate:
            raise ValueError("Node is duplicated")

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
                    if adj_node not in nodes_queue: # and adj_node not in available_nodes:  # Loop condition
                        nodes_queue.append(adj_node)
            else:
                nodes_queue.appendleft(current_node)

        return available_nodes, list(nodes_queue)

    def _recursive_monsters(self, root_node: NodeInfo, graph: nx.DiGraph,
                            nodes_dict: Dict[str, NodeInfo]):
        monsters = self.world.monsters.monsters
        fight_estimator = FightEstimator(world=self.world, simulate_fights_number=100)

        available_nodes = [get_code(root_node)]
        remaining_nodes = available_nodes.copy()

        for monster in sorted(monsters, key=lambda mnstr: mnstr.stats.level):
            # Check for cycles
            graph_cycles = list(nx.simple_cycles(graph))
            if graph_cycles:
                logger.error(f"Graph contains cycles: {graph_cycles}")
                raise ValueError("Graph contains cycles")

            logger.info("-" * 20)
            logger.info(f"Try to find optimal with monster: {monster.name}")

            # 1. Check monster can be beaten by optimal equipment and maybe consumables
            # 2. Check monster can be beaten by task items (which are very rare) and maybe consumables
            # 3. Search as NP hard problem
            for is_add_task_items, use_np_hard in zip([False, True, True], [False, False, True]):
                # Items that can be retrieved by quests
                if is_add_task_items:
                    for task_item_node in self._task_roadmap(level=monster.stats.level, graph=graph,
                                                             nodes_dict=nodes_dict):
                        task_item_code = get_code(task_item_node)
                        # It's possible that nodes already in queue
                        if task_item_code not in available_nodes and task_item_code not in remaining_nodes:
                            remaining_nodes.append(task_item_code)
                logger.info(f"Try to find optimal with nodes: {is_add_task_items=}, {use_np_hard=}")

                available_nodes, remaining_nodes = self._find_accessible_nodes(graph, available_nodes, remaining_nodes)
                available_nodes, remaining_nodes = list(set(available_nodes)), list(set(remaining_nodes))
                available_items = [
                    self.world.item_details.get_item(nodes_dict[node_info].target_item) for
                    node_info in available_nodes if nodes_dict[node_info].target_item is not None]

                # Fast estimation
                equipment_estimator = EquipmentEstimator(available_items, use_consumables=False)
                optimal_equipment: Dict[
                    EquipmentSlot, Items] = equipment_estimator.optimal_vs_monster(None,
                                                                                   monster=monster)
                proxy_character = ProxyCharacter(monster.stats.level,
                                                 optimal_equipment,
                                                 world=self.world)
                simulation_results = fight_estimator.simulate_fights(proxy_character, monster)
                if simulation_results.success_rate >= self.winrate:
                    logger.info(f"monster={monster.name}:{monster.stats.level} has winrate "
                                f"{simulation_results.success_rate}. At the final "
                                f"monster_hp={simulation_results.result.monster_hp}<char_hp="
                                f"{simulation_results.result.character_hp}, "
                                f"in turns={simulation_results.result.turns}, "
                                f"items={[value.item.code for value in optimal_equipment.values()]}")
                    break
                else:
                    logger.error(f"Can't found optimal equipment, current={[items.item.code for items in optimal_equipment.values()]}")
                # Long estimation if monster hasn't been beaten with consumables
                if simulation_results.success_rate < self.winrate:
                    logger.info(f"NP Hard Estimation, {is_add_task_items=}, {use_np_hard=}, current_winrate={simulation_results.success_rate}")
                    if use_np_hard:
                        # Search with all equipment
                        initial_equipment = None
                    else:
                        # Search with consumables
                        initial_equipment: Dict[EquipmentSlot, Items] = optimal_equipment
                    np_hard_estimator = NPHardEquipmentEstimator(self.world, available_items,
                                                                 use_consumables=True,
                                                                 winrate=self.winrate,
                                                                 initial_equipment=initial_equipment,
                                                                 max_equipment_count=1)
                    optimal_equipment = np_hard_estimator.optimal_vs_monster(proxy_character,
                                                                                 monster)
                    proxy_character = ProxyCharacter(monster.stats.level,
                                                     optimal_equipment,
                                                     world=self.world)
                    simulation_results = fight_estimator.simulate_fights(proxy_character, monster)
                    if simulation_results.success_rate >= self.winrate:
                        logger.info(f"monster={monster.name}:{monster.stats.level} has winrate "
                                    f"{simulation_results.success_rate}. At the final "
                                    f"monster_hp={simulation_results.result.monster_hp}<char_hp="
                                    f"{simulation_results.result.character_hp}, "
                                    f"in turns={simulation_results.result.turns}, "
                                    f"items={[value.item.code for value in optimal_equipment.values()]}"
                                    f"consumables={simulation_results.result.spent_consumables}")
                        break

            assert simulation_results.success_rate >= self.winrate, \
                f"{simulation_results.success_rate}, Maybe rerun will help"

            # We think monster has been beaten
            # Add monster node
            monster_node = NodeInfo(monster_info=monster)
            character_node = NodeInfo(character_info=CharacterInfo(level=monster.stats.level))
            nodes_dict[get_code(character_node)] = character_node
            graph.add_edge(get_code(character_node), get_code(monster_node))
            # Add dependency that we get next level only when monster is beaaten
            if monster.stats.level + 1 < CHARACTER_MAX_LEVEL:
                next_character_node = NodeInfo(
                    character_info=CharacterInfo(level=monster.stats.level + 1))
                graph.add_edge(get_code(monster_node), get_code(next_character_node))

            logger.info(f"Used items={[items.item.code for items in optimal_equipment.values()]}")
            for items in optimal_equipment.values():
                item_node = NodeInfo(target_item=items.item)
                graph.add_edge(get_code(item_node), get_code(monster_node))


            nodes_dict[get_code(monster_node)] = monster_node
            remaining_nodes.append(get_code(monster_node))
            remaining_nodes.append(get_code(character_node))
            # Can add drops
            for drop in monster.drops:
                drop_node = NodeInfo(target_item=drop.item)
                if get_code(drop_node) not in nodes_dict:
                    graph.add_edge(get_code(monster_node), get_code(drop_node))
                    remaining_nodes.append(get_code(drop_node))
                    nodes_dict[get_code(drop_node)] = drop_node

            logger.info(f"Finish with monster: {monster}")
            logger.info("-" * 20)


    def _task_roadmap(self, level:int, graph: nx.DiGraph, nodes_dict: Dict[str, NodeInfo]):
        items_from_task = self.world.item_details.items
        task_items = [item for item in items_from_task if item.subtype == "task" and item.level <= level]
        new_nodes = []
        for item in task_items:
            character_node = NodeInfo(character_info=CharacterInfo(level=item.level))
            task_node = NodeInfo(task_info=TaskInfo(level=item.level))
            graph.add_edge(get_code(character_node), get_code(task_node))
            nodes_dict[get_code(task_node)] = task_node

            item_node = NodeInfo(target_item=item)
            item_code = get_code(item_node)
            graph.add_edge(get_code(task_node), item_code)
            nodes_dict[item_code] = item_node

            new_nodes.append(task_node)
        return new_nodes


    def create_items_roadmap(self):

        root_node = NodeInfo(character_info=CharacterInfo(1))
        DG = nx.DiGraph()
        nodes_dict: Dict[str, NodeInfo] = {get_code(root_node): root_node}

        parent_node = root_node
        for i in range(2, CHARACTER_MAX_LEVEL+1):
            character_node = NodeInfo(character_info=CharacterInfo(level=i))
            nodes_dict[get_code(character_node)] = character_node
            DG.add_edge(get_code(parent_node), get_code(character_node))
            parent_node = character_node

        self._resource_roadmap(root_node, DG, nodes_dict)
        self._recursive_craft(root_node, DG, nodes_dict)
        self._recursive_monsters(root_node, DG, nodes_dict)
        # Update for missed nodes
        self._task_roadmap(CHARACTER_MAX_LEVEL, DG, nodes_dict)

        has_disconnected_nodes = False
        for node in DG.nodes():
            if DG.predecessors(node) == 0:
                logger.warning(f"Node {node} is not connected")
                has_disconnected_nodes = True
        if has_disconnected_nodes:
            raise Exception("Disconnected nodes")

        # Remove useless nodes
        DG.remove_node("item:wooden_stick")
        # Check that all nodes are connected
        for node in DG.nodes():
            assert node in nodes_dict, (f"node: {node} not in nodes_dict, try to change "
                                        f"something maybe there is bug in hashable, keys={list(nodes_dict.keys())})")

        return DG, nodes_dict


def graph(graph: nx.DiGraph, reduce: bool = False):
    nt = Network("1080px", "1920px", directed=True, neighborhood_highlight=True, select_menu=True,
                 filter_menu=True)
    if reduce:
        graph = graph.copy()
        for node in list(graph.nodes()):
            if not list(graph.successors(node)):
                graph.remove_node(node)


    nt.from_nx(graph)
    nt.show("nx.html", notebook=False)
    # nx.draw(graph, with_labels=True, font_weight='bold')
    # plt.show()
