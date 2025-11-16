#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import heapq
from collections import deque, defaultdict

# -----------------------------
# Geometry utilities
# -----------------------------
@dataclass(frozen=True)
class Node:
    x: float
    y: float
    pid: Optional[int]  # polygon id (None for S and G)
    idx: Optional[int]  # vertex index within polygon (None for S and G)
    label: str          # "S", "G", or "V"

def orientation(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    # cross product orientation (b - a) x (c - a). Positive if CCW.
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def on_segment(a: Tuple[float, float], b: Tuple[float, float], p: Tuple[float, float]) -> bool:
    # Check if point p lies on segment ab (inclusive).
    minx, maxx = min(a[0], b[0]), max(a[0], b[0])
    miny, maxy = min(a[1], b[1]), max(a[1], b[1])
    eps = 1e-9
    if p[0] + eps < minx or p[0] - eps > maxx or p[1] + eps < miny or p[1] - eps > maxy:
        return False
    return abs(orientation(a, b, p)) <= 1e-9

def proper_intersection(a: Tuple[float, float], b: Tuple[float, float],
                        c: Tuple[float, float], d: Tuple[float, float]) -> bool:
    # True if ab and cd intersect strictly interior to both segments.
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)
    return (o1 * o2 < 0) and (o3 * o4 < 0)

def segments_intersect(a: Tuple[float, float], b: Tuple[float, float],
                       c: Tuple[float, float], d: Tuple[float, float]) -> bool:
    # General segment intersection, including colinear/touching as intersection.
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    if (o1 * o2 < 0) and (o3 * o4 < 0):
        return True

    # Colinear/touching cases
    if abs(o1) <= 1e-9 and on_segment(a, b, c): return True
    if abs(o2) <= 1e-9 and on_segment(a, b, d): return True
    if abs(o3) <= 1e-9 and on_segment(c, d, a): return True
    if abs(o4) <= 1e-9 and on_segment(c, d, b): return True
    return False

def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])

# -----------------------------
# Parsing
# -----------------------------
def parse_input(text: str):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    first = lines[0].split()
    if len(first) != 5:
        raise ValueError("First line must be: N Sx Sy Gx Gy")
    N = int(first[0])
    Sx, Sy, Gx, Gy = map(float, first[1:])

    polygons: List[List[Tuple[float,float]]] = []
    for i in range(N):
        parts = lines[1 + i].split()
        M = int(parts[0])
        coords = list(map(float, parts[1:]))
        if len(coords) != 2 * M:
            raise ValueError(f"Polygon {i}: expected {M} vertices, got {len(coords)//2}")
        poly = [(coords[2*j], coords[2*j+1]) for j in range(M)]
        polygons.append(poly)

    return N, (Sx, Sy), (Gx, Gy), polygons

# -----------------------------
# Visibility graph
# -----------------------------
def adjacent_indices(m: int, i: int, j: int) -> bool:
    # Adjacent on a cycle if they share an edge.
    return (i - j) % m == 1 or (j - i) % m == 1

def build_edges_from_polygons(polygons: List[List[Tuple[float,float]]]) -> List[Tuple[Tuple[float,float], Tuple[float,float], int]]:
    # Return list of all polygon boundary edges (a,b,pid).
    edges = []
    for pid, poly in enumerate(polygons):
        m = len(poly)
        for i in range(m):
            a = poly[i]
            b = poly[(i+1) % m]
            edges.append((a, b, pid))
    return edges

def is_visible(u: Node, v: Node, all_edges, polygons) -> bool:
    # Visible if the segment uv does not cross any polygon edge except possibly at shared endpoints.
    # Also, two vertices of the same polygon are only visible if they are adjacent (share an edge).
    if u.x == v.x and u.y == v.y:
        return False

    # Same polygon adjacency rule
    if (u.pid is not None) and (v.pid is not None) and (u.pid == v.pid):
        m = len(polygons[u.pid])
        if u.idx is None or v.idx is None:
            return False
        if not adjacent_indices(m, u.idx, v.idx):
            return False

    a = (u.x, u.y)
    b = (v.x, v.y)

    def same_point(p, q) -> bool:
        return abs(p[0] - q[0]) <= 1e-9 and abs(p[1] - q[1]) <= 1e-9

    for (c, d, eid_pid) in all_edges:
        # If the polygon edge shares an endpoint with uv, allow the touch (unless proper intersection)
        if same_point(a, c) or same_point(a, d) or same_point(b, c) or same_point(b, d):
            if proper_intersection(a, b, c, d):
                return False
            continue

        # If segments intersect anywhere else, it's blocked
        if segments_intersect(a, b, c, d):
            return False

    return True

def build_graph(S, G, polygons):
    nodes: List[Node] = []
    nodes.append(Node(S[0], S[1], None, None, "S"))
    nodes.append(Node(G[0], G[1], None, None, "G"))
    for pid, poly in enumerate(polygons):
        for idx, (x, y) in enumerate(poly):
            nodes.append(Node(x, y, pid, idx, "V"))

    all_edges = build_edges_from_polygons(polygons)

    # Build adjacency list with weights
    n = len(nodes)
    adj: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    for i in range(n):
        for j in range(i+1, n):
            u, v = nodes[i], nodes[j]
            if is_visible(u, v, all_edges, polygons):
                w = dist((u.x, u.y), (v.x, v.y))
                adj[i].append((j, w))
                adj[j].append((i, w))
    return nodes, adj

# -----------------------------
# Search algorithms
# -----------------------------
def reconstruct_path(parents: Dict[int,int], goal: int):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parents.get(cur, None)
    return list(reversed(path))

def bfs(adj, start: int, goal: int):
    q = deque([start])
    parents = {start: None}
    while q:
        u = q.popleft()
        if u == goal:
            return reconstruct_path(parents, goal)
        for v, _ in adj[u]:
            if v not in parents:
                parents[v] = u
                q.append(v)
    return None

def dfs(adj, start: int, goal: int):
    stack = [start]
    parents = {start: None}
    while stack:
        u = stack.pop()
        if u == goal:
            return reconstruct_path(parents, goal)
        for v, _ in adj[u]:
            if v not in parents:
                parents[v] = u
                stack.append(v)
    return None

def ucs(adj, start: int, goal: int):
    pq = [(0.0, start)]
    dist_map = {start: 0.0}
    parents = {start: None}
    visited = set()
    while pq:
        g, u = heapq.heappop(pq)
        if u in visited: 
            continue
        visited.add(u)
        if u == goal:
            return reconstruct_path(parents, goal)
        for v, w in adj[u]:
            ng = g + w
            if v not in dist_map or ng < dist_map[v] - 1e-12:
                dist_map[v] = ng
                parents[v] = u
                heapq.heappush(pq, (ng, v))
    return None

def greedy_best_first(adj, nodes, start: int, goal: int):
    def h(i): 
        return dist((nodes[i].x, nodes[i].y), (nodes[goal].x, nodes[goal].y))
    pq = [(h(start), start)]
    parents = {start: None}
    visited = set()
    while pq:
        _, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            return reconstruct_path(parents, goal)
        for v, _w in adj[u]:
            if v not in visited and v not in parents:
                parents[v] = u
                heapq.heappush(pq, (h(v), v))
    return None

def astar(adj, nodes, start: int, goal: int):
    def h(i): 
        return dist((nodes[i].x, nodes[i].y), (nodes[goal].x, nodes[goal].y))
    pq = [(h(start), 0.0, start)]  # (f, g, node)
    best_g = {start: 0.0}
    parents = {start: None}
    closed = set()
    while pq:
        f, g, u = heapq.heappop(pq)
        if u in closed:
            continue
        closed.add(u)
        if u == goal:
            return reconstruct_path(parents, goal)
        for v, w in adj[u]:
            ng = g + w
            if v not in best_g or ng < best_g[v] - 1e-12:
                best_g[v] = ng
                parents[v] = u
                heapq.heappush(pq, (ng + h(v), ng, v))
    return None

# -----------------------------
# Printing
# -----------------------------
def format_node(n: Node) -> str:
    if n.label == "S":
        return f"({n.x}, {n.y}, S)"
    if n.label == "G":
        return f"({n.x}, {n.y}, G)"
    return f"({n.x}, {n.y}, p{n.pid})"

def path_length(nodes: List[Node], path) -> float:
    if not path or len(path) < 2:
        return 0.0
    total = 0.0
    for i in range(len(path)-1):
        a, b = nodes[path[i]], nodes[path[i+1]]
        total += math.hypot(a.x - b.x, a.y - b.y)
    return total

def print_path(title: str, nodes: List[Node], path):
    print("="*80)
    print(title)
    if path is None:
        print("Không tìm thấy đường đi.")
        return
    segs = " -> ".join(format_node(nodes[i]) for i in path)
    print(segs)
    print(f"Độ dài (Euclid): {path_length(nodes, path):.6f}")

# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Visibility-graph search among convex polygon obstacles.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to input txt file.")
    parser.add_argument("--algo", "-a", type=str, default="all",
                        choices=["bfs","dfs","ucs","greedy","astar","all"],
                        help="Which algorithm to run.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
    N, S, G, polygons = parse_input(text)

    nodes, adj = build_graph(S, G, polygons)
    start, goal = 0, 1

    if args.algo in ("bfs","all"):
        p = bfs(adj, start, goal)
        print_path("BFS (cạnh bằng nhau, không tối ưu độ dài):", nodes, p)
    if args.algo in ("dfs","all"):
        p = dfs(adj, start, goal)
        print_path("DFS (không đảm bảo ngắn nhất):", nodes, p)
    if args.algo in ("ucs","all"):
        p = ucs(adj, start, goal)
        print_path("UCS / Dijkstra (tối ưu độ dài):", nodes, p)
    if args.algo in ("greedy","all"):
        p = greedy_best_first(adj, nodes, start, goal)
        print_path("Greedy Best-First (tham lam theo heuristic):", nodes, p)
    if args.algo in ("astar","all"):
        p = astar(adj, nodes, start, goal)
        print_path("A* (heuristic khoảng cách thẳng):", nodes, p)

if __name__ == "__main__":
    main()
