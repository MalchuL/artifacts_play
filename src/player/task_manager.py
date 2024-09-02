from dataclasses import dataclass
from threading import Lock
from typing import Dict, Optional, List

import networkx as nx
from pyvis.network import Network

from src.player.task import TaskInfo


@dataclass
class ManagerTask:
    task_id: int
    task_info: TaskInfo
    player_id: Optional[str] = None

    def __repr__(self):
        return f"{self.player_id}-{self.task_id}: {self.task_info}"


class WorldTaskManager:
    def __init__(self):
        self.__task_id = 0
        self.mutex = Lock()
        self.task_graph = nx.DiGraph()
        self.task_info: Dict[int, ManagerTask] = {}

    def add_task(self, task: TaskInfo, player: Optional["Player"] = None,
                 depend_on: Optional[ManagerTask] = None) -> ManagerTask:
        with self.mutex:
            manager_task = ManagerTask(task_id=self.__task_id, task_info=task,
                                       player_id=None if player is None else player.player_id)
            if depend_on:
                self.task_graph.add_edge(depend_on.task_id, manager_task.task_id)
            else:
                self.task_graph.add_node(manager_task.task_id)
            self.task_info[manager_task.task_id] = manager_task
            self.__task_id += 1
        self.dump_graph()
        return manager_task

    def parent_task(self, manager_task: ManagerTask):
        parent_nodes = list(self.task_graph.predecessors(manager_task.task_id))
        assert len(parent_nodes) <= 1
        if parent_nodes:
            return self.task_info[parent_nodes[0]]
        else:
            return None

    def assign_task(self, player: "Player", manager_task: ManagerTask) -> ManagerTask:
        with self.mutex:
            assert manager_task.player_id is None
            manager_task.player_id = player.player_id
            # Double check to avoid double assignment
            self.task_info[manager_task.task_id].player_id = player.player_id
        self.dump_graph()
        return manager_task

    def _is_pending(self, task_id: str) -> bool:
        return not self._is_pending(task_id)

    def _is_can_be_done(self, task_id: str) -> bool:
        # Check is leaf node
        return len(tuple(self.task_graph.successors(task_id))) == 0

    def remove_task(self, task: ManagerTask):
        with self.mutex:
            self.task_graph.remove_node(task.task_id)
            del self.task_info[task.task_id]
            self.dump_graph()

    def tasks_to_do(self, player: "Player") -> List[ManagerTask]:
        with self.mutex:
            leaf_node_names = [node_name for node_name in self.task_graph.nodes if
                               self._is_can_be_done(node_name)]
            leaf_nodes = [self.task_info[node_name] for node_name in leaf_node_names]
            player_nodes = [node for node in leaf_nodes if
                            node.player_id is not None and node.player_id == player.player_id]
        return player_nodes

    def unassigned_tasks(self) -> List[ManagerTask]:
        with self.mutex:
            leaf_node_names = [node_name for node_name in self.task_graph.nodes if
                               self._is_can_be_done(node_name)]
            leaf_nodes = [self.task_info[node_name] for node_name in leaf_node_names]
            player_nodes = [node for node in leaf_nodes if
                            node.player_id is None]
        return player_nodes


    def dump_graph(self):
        graph_copy = self.task_graph.copy()
        for node in graph_copy.nodes:
            graph_copy.nodes[node]["label"] = str(self.task_info[node])
        nt = Network("1080px", "1920px", directed=True, neighborhood_highlight=True,
                     select_menu=True,
                     filter_menu=True)
        nt.from_nx(graph_copy)
        nt.write_html("tasks.html", open_browser=False, notebook=False)
