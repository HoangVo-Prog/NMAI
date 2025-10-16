from collections import defaultdict
from queue import Queue, PriorityQueue

# đọc dữ liệu từ file txt
from typing import TextIO

def _next_nonempty_line(f: TextIO) -> str:
    for ln in f:
        ln = ln.strip()
        if ln:
            return ln
    raise ValueError("Unexpected end of file while reading.")

def read_txt(file: TextIO):
    # Dòng 1: N
    size_line = _next_nonempty_line(file)
    size = int(size_line)

    # Dòng 2: start goal (2 số)
    sg_line = _next_nonempty_line(file)
    sg = sg_line.split()
    if len(sg) != 2:
        raise ValueError(f"Expected two integers 'start goal' on line 2, got: {sg_line}")
    start, goal = map(int, sg)

    # Đọc đúng N dòng ma trận (bỏ qua dòng trống)
    matrix = []
    while len(matrix) < size:
        row_line = _next_nonempty_line(file)
        row = list(map(int, row_line.split()))
        matrix.append(row)

    # Kiểm tra kích thước
    if len(matrix) != size:
        raise ValueError(f"Expected {size} rows, got {len(matrix)}")
    for i, row in enumerate(matrix):
        if len(row) != size:
            raise ValueError(f"Row {i} has {len(row)} cols, expected {size}")

    return size, start, goal, matrix



# chuyển ma trận kề thành danh sách kề
def convert_graph(a):
    adjList = defaultdict(list)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] == 1:
                adjList[i].append(j)
    return adjList

def convert_graph_weight(a):
    adjList = defaultdict(list)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] != 0:
                adjList[i].append((j, a[i][j]))
    return adjList
