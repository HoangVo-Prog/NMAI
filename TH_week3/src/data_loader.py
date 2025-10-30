from __future__ import annotations
from typing import Dict, Tuple
import networkx as nx

def load_heuristic(path: str) -> Dict[str, float]:
    h: Dict[str, float] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            city, val = line.split()
            h[city] = float(val)
    return h

def load_positions(path: str) -> Dict[str, Tuple[float, float]]:
    pos = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            city, x, y = line.split()
            pos[city] = (float(x), float(y))
    return pos

def load_graph(path: str) -> nx.Graph:
    G = nx.Graph()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a, b, w = line.split()
            w = float(w)
            G.add_edge(a, b, weight=w)
    return G
