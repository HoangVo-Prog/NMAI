from __future__ import annotations
import argparse
from typing import Tuple
from data_loader import load_heuristic, load_positions, load_graph
from search import greedy_best_first, a_star, path_cost
from plot_map import draw_graph

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("GBFS and A* on Romania map")
    p.add_argument("--data", default="data", help="data directory")
    p.add_argument("--start", default="Arad", help="start city")
    p.add_argument("--goal", default="Hirsova", help="goal city")
    p.add_argument("--algo", choices=["gbfs", "astar"], default="astar", help="search algorithm")
    p.add_argument("--plot", action="store_true", help="save a PNG of the route")
    p.add_argument("--out", default="route.png", help="output figure path if --plot is set")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    H = load_heuristic(f"{args.data}/heuristic.txt")
    pos = load_positions(f"{args.data}/cities.txt")
    G = load_graph(f"{args.data}/citiesGraph.txt")

    if args.algo == "gbfs":
        path, cost, expanded = greedy_best_first(G, args.start, args.goal, H)
        print(f"[GBFS] path={path} cost={cost:.0f} expanded={expanded}")
        title = "GBFS path"
    else:
        path, cost, expanded = a_star(G, args.start, args.goal, H)
        print(f"[A*] path={path} cost={cost:.0f} expanded={expanded}")
        title = "A* path"

    if args.plot:
        draw_graph(G, pos, path, args.out, f"{title}: {args.start} to {args.goal}")

if __name__ == "__main__":
    main()
