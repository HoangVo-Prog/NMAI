import argparse
import heapq
from math import inf
from typing import List, Tuple, Optional


class TSPSolverAStar:
    """
    Giai bai toan TSP bang A* voi heuristic la chi phi cay khung nho nhat (MST)
    tren tap cac thanh pho chua tham.
    """

    def __init__(self, dist: List[List[float]], start: int = 0) -> None:
        if not dist or any(len(row) != len(dist) for row in dist):
            raise ValueError("Ma tran khoang cach phai la NxN va khong rong")
        self.dist = dist
        self.n = len(dist)
        if not (0 <= start < self.n):
            raise ValueError("Chi so thanh pho bat dau khong hop le")
        self.start = start

    def mst_cost(self, nodes: List[int]) -> float:
        """
        Tinh chi phi MST tren danh sach dinh nodes su dung Prim.
        """
        if len(nodes) <= 1:
            return 0.0

        in_mst = {nodes[0]}
        not_in_mst = set(nodes[1:])
        total = 0.0

        while not_in_mst:
            best_cost = inf
            best_v = None
            for u in in_mst:
                for v in not_in_mst:
                    c = self.dist[u][v]
                    if c < best_cost:
                        best_cost = c
                        best_v = v
            if best_v is None:
                return 0.0
            total += best_cost
            in_mst.add(best_v)
            not_in_mst.remove(best_v)

        return total

    def heuristic(self, current: int, visited_mask: int) -> float:
        """
        Heuristic A*:
          - Neu chua tham het:
            MST tren cac dinh chua tham
            cong canh re nhat tu current den mot dinh chua tham
            cong canh re nhat tu start den mot dinh chua tham
          - Neu da tham het:
            chi phi can thiet de ve lai start
        """
        all_visited_mask = (1 << self.n) - 1

        if visited_mask == all_visited_mask:
            return self.dist[current][self.start]

        remaining = [i for i in range(self.n) if not (visited_mask & (1 << i))]
        if not remaining:
            return self.dist[current][self.start]

        mst = self.mst_cost(remaining)
        min_from_current = min(self.dist[current][j] for j in remaining)
        min_from_start = min(self.dist[self.start][j] for j in remaining)

        return mst + min_from_current + min_from_start

    def solve(self) -> Tuple[Optional[float], Optional[List[int]]]:
        """
        Chay A* de giai TSP.
        Tra ve:
          - best_cost: chi phi tour
          - best_path: danh sach thanh pho theo thu tu tham
        """
        start_mask = 1 << self.start
        start_state = (self.start, start_mask)

        pq = []
        g_start = 0.0
        h_start = self.heuristic(self.start, start_mask)
        heapq.heappush(pq, (g_start + h_start, g_start, self.start, start_mask))

        best_g = {start_state: 0.0}
        parent = {}

        all_visited_mask = (1 << self.n) - 1

        while pq:
            f, g, current, visited_mask = heapq.heappop(pq)
            state = (current, visited_mask)

            if best_g.get(state, inf) < g:
                continue

            if visited_mask == all_visited_mask and current == self.start and g > 0:
                path = [current]
                s = state
                while s in parent:
                    s = parent[s]
                    path.append(s[0])
                path.reverse()
                return g, path

            remaining = [i for i in range(self.n) if not (visited_mask & (1 << i))]

            if remaining:
                for nxt in remaining:
                    new_mask = visited_mask | (1 << nxt)
                    new_g = g + self.dist[current][nxt]
                    new_state = (nxt, new_mask)
                    if new_g < best_g.get(new_state, inf):
                        best_g[new_state] = new_g
                        parent[new_state] = state
                        h = self.heuristic(nxt, new_mask)
                        heapq.heappush(pq, (new_g + h, new_g, nxt, new_mask))
            else:
                if current != self.start:
                    nxt = self.start
                    new_mask = visited_mask
                    new_g = g + self.dist[current][nxt]
                    new_state = (nxt, new_mask)
                    if new_g < best_g.get(new_state, inf):
                        best_g[new_state] = new_g
                        parent[new_state] = state
                        h = self.heuristic(nxt, new_mask)
                        heapq.heappush(pq, (new_g + h, new_g, nxt, new_mask))

        return None, None


def load_distance_matrix(path: str) -> List[List[float]]:
    """
    Doc ma tran khoang cach tu file text.

    Dinh dang:
      - Dong 1: so nguyen N
      - N dong tiep theo: N so (int hoac float) cach nhau boi khoang trang

    Vi du:
      4
      0 2 9 10
      1 0 6 4
      15 7 0 8
      6 3 12 0
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    if not lines:
        raise ValueError("File rong")

    n = int(lines[0])
    if len(lines) != n + 1:
        raise ValueError("So dong trong file khong phu hop voi N")

    dist: List[List[float]] = []
    for i in range(1, n + 1):
        parts = lines[i].split()
        if len(parts) != n:
            raise ValueError(f"Dong {i + 1} khong co dung {n} phan tu")
        row = [float(x) for x in parts]
        dist.append(row)

    return dist


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Giai bai toan TSP bang A* voi heuristic MST",
    )
    parser.add_argument(
        "matrix_file",
        help="Duong dan file chua ma tran khoang cach",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Chi so thanh pho bat dau, mac dinh 0",
    )
    args = parser.parse_args()

    dist = load_distance_matrix(args.matrix_file)
    solver = TSPSolverAStar(dist, start=args.start)
    cost, tour = solver.solve()

    if tour is None:
        print("Khong tim duoc tour hop le")
    else:
        print("Chi phi tour tot nhat:", cost)
        print("Tour:", " -> ".join(str(c) for c in tour))


if __name__ == "__main__":
    main()
