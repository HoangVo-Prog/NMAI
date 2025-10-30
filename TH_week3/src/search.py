from __future__ import annotations
from typing import Callable, Dict, List, Tuple, Optional
import heapq
import networkx as nx

Path = List[str]
Heu = Dict[str, float]

def reconstruct_path(came_from: Dict[str, Optional[str]], goal: str) -> Path:
    path: Path = []
    node: Optional[str] = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path

def greedy_best_first(G: nx.Graph, start: str, goal: str, h: Heu) -> Tuple[Path, float, int]:
    if start not in G or goal not in G:
        raise ValueError("start or goal not in graph")
    open_heap: List[Tuple[float, str]] = [(h[start], start)]
    came_from: Dict[str, Optional[str]] = {start: None}
    visited = set()
    expanded = 0
    while open_heap:
        _, u = heapq.heappop(open_heap)
        if u in visited:
            continue
        visited.add(u)
        expanded += 1
        if u == goal:
            path = reconstruct_path(came_from, goal)
            cost = path_cost(G, path)
            return path, cost, expanded
        for v in sorted(G.neighbors(u)):
            if v in visited:
                continue
            if v not in came_from:
                came_from[v] = u
            heapq.heappush(open_heap, (h.get(v, float("inf")), v))
    return [], float("inf"), expanded

def a_star(G: nx.Graph, start: str, goal: str, h: Heu) -> Tuple[Path, float, int]:
    if start not in G or goal not in G:
        raise ValueError("start or goal not in graph")
    open_heap: List[Tuple[float, str]] = []
    heapq.heappush(open_heap, (h[start], start))
    g: Dict[str, float] = {start: 0.0}
    came_from: Dict[str, Optional[str]] = {start: None}
    closed = set()
    expanded = 0
    while open_heap:
        f_u, u = heapq.heappop(open_heap)
        if u in closed:
            continue
        closed.add(u)
        expanded += 1
        if u == goal:
            path = reconstruct_path(came_from, goal)
            return path, g[goal], expanded
        for v in G.neighbors(u):
            w = G[u][v]["weight"]
            tentative = g[u] + w
            if v in closed and tentative >= g.get(v, float("inf")):
                continue
            if tentative < g.get(v, float("inf")):
                came_from[v] = u
                g[v] = tentative
                f_v = tentative + h.get(v, float("inf"))
                heapq.heappush(open_heap, (f_v, v))
    return [], float("inf"), expanded

def path_cost(G: nx.Graph, path: Path) -> float:
    if not path or len(path) == 1:
        return 0.0
    total = 0.0
    for a, b in zip(path, path[1:]):
        total += G[a][b]["weight"]
    return total
