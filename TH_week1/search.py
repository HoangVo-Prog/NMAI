import heapq

class Queue:
    """Cấu trúc dữ liệu hàng đợi (FIFO - First In First Out)"""
    def __init__(self):
        self.items = []

    def put(self, item):
        """Thêm phần tử vào cuối hàng đợi"""
        self.items.append(item)

    def get(self):
        """Lấy và loại bỏ phần tử ở đầu hàng đợi"""
        if not self.empty():
            return self.items.pop(0)
        else:
            raise Exception("Queue is empty!")

    def empty(self):
        """Kiểm tra xem hàng đợi có trống không"""
        return len(self.items) == 0

    def __str__(self):
        return f"Queue({self.items})"


class PriorityQueue:
    """Cấu trúc dữ liệu hàng đợi ưu tiên (Priority Queue - Min-Heap)"""
    def __init__(self):
        self.elements = []

    def put(self, item):
        """Thêm phần tử vào hàng đợi (item phải là tuple (priority, value))"""
        heapq.heappush(self.elements, item)

    def get(self):
        """Lấy phần tử có độ ưu tiên nhỏ nhất"""
        if not self.empty():
            return heapq.heappop(self.elements)
        else:
            raise Exception("PriorityQueue is empty!")

    def empty(self):
        """Kiểm tra xem hàng đợi có trống không"""
        return len(self.elements) == 0

    def __str__(self):
        return f"PriorityQueue({self.elements})"


def BFS(graph, start, end):
    visited = []
    frontier = Queue()

    # thêm node start vào frontier và visited
    frontier.put(start)
    visited.append(start)

    # start không có node cha
    parent = dict()
    parent[start] = None

    path_found = False

    while True:
        if frontier.empty():
            raise Exception("No way Exception")

        current_node = frontier.get()
        visited.append(current_node)

        # Kiểm tra current_node có là end hay không
        if current_node == end:
            path_found = True
            break

        for node in graph[current_node]:
            if node not in visited:
                frontier.put(node)
                parent[node] = current_node
                visited.append(node)

    # Xây dựng đường đi
    path = []
    if path_found:
        path.append(end)
        while parent[end] is not None:
            path.append(parent[end])
            end = parent[end]
        path.reverse()

    return path


def DFS(graph, start, end):
    visited = []
    frontier = []

    # thêm node start vào frontier và visited
    frontier.append(start)
    visited.append(start)

    # start không có node cha
    parent = dict()
    parent[start] = None

    path_found = False

    while True:
        if frontier == []:
            raise Exception("No way Exception")

        current_node = frontier.pop()
        visited.append(current_node)

        # Kiểm tra current_node có là end hay không
        if current_node == end:
            path_found = True
            break

        for node in graph[current_node]:
            if node not in visited:
                frontier.append(node)
                parent[node] = current_node
                visited.append(node)

    # Xây dựng đường đi
    path = []
    if path_found:
        path.append(end)
        while parent[end] is not None:
            path.append(parent[end])
            end = parent[end]
        path.reverse()

    return path


def UCS_old(graph, start, end):
    visited = []
    frontier = PriorityQueue()

    # thêm node start vào frontier và visited
    frontier.put((0, start))
    visited.append(start)

    # start không có node cha
    parent = dict()
    parent[start] = None

    path_found = False

    while True:
        if frontier.empty():
            raise Exception("No way Exception")

        current_w, current_node = frontier.get()
        visited.append(current_node)

        # Kiểm tra current_node có là end hay không
        if current_node == end:
            path_found = True
            break

        for nodei in graph[current_node]:
            node, weight = nodei
            if node not in visited:
                frontier.put((current_w + weight, node))
                parent[node] = current_node
                visited.append(node)

    # Xây dựng đường đi
    path = []
    if path_found:
        path.append(end)
        while parent[end] is not None:
            path.append(parent[end])
            end = parent[end]
        path.reverse()

    return current_w, path


def UCS_new(graph, start, goal):
    # graph: dict[node] -> list[(neighbor, weight)]
    frontier = [(0, start)]          # heap of (cost, node)
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()

    while frontier:
        current_cost, u = heapq.heappop(frontier)
        if u in explored:
            continue
        explored.add(u)

        if u == goal:
            # reconstruct path
            path = []
            v = goal
            while v is not None:
                path.append(v)
                v = came_from[v]
            path.reverse()
            return current_cost, path

        for v, w in graph.get(u, []):
            if w < 0:
                raise ValueError("UCS requires nonnegative edge weights")
            new_cost = current_cost + w
            if v not in cost_so_far or new_cost < cost_so_far[v]:
                cost_so_far[v] = new_cost
                came_from[v] = u
                heapq.heappush(frontier, (new_cost, v))

    # not found
    return float("inf"), []
