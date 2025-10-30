import sys, os
sys.path.append(os.path.dirname(__file__))
from utils import read_txt, convert_graph, convert_graph_weight
from search import BFS, DFS, UCS_old, UCS_new

def main():
    # Đọc file Input.txt và InputUCS.txt
    file_1 = open("input/Input.txt", "r")
    file_2 = open("input/InputUCS.txt", "r")


    size_1, start_1, goal_1, matrix_1 = read_txt(file_1)
    size_2, start_2, goal_2, matrix_2 = read_txt(file_2)
    file_1.close()
    file_2.close()

    graph_1 = convert_graph(matrix_1)
    graph_2 = convert_graph_weight(matrix_2)

    # Thực thi thuật toán BFS
    result_bfs = BFS(graph_1, start_1, goal_1)
    print("Kết quả sử dụng thuật toán BFS:\n", result_bfs)

    # Thực thi thuật toán DFS
    result_dfs = DFS(graph_1, start_1, goal_1)
    print("Kết quả sử dụng thuật toán DFS:\n", result_dfs)

    # Thực thi thuật toán UCS_old
    result_ucs, cost = UCS_old(graph_2, start_2, goal_2)
    print("Kết quả sử dụng thuật toán UCS_old:\n", result_ucs, "với tổng chi phí là", cost)
    
    # Thực thi thuật toán UCS_new
    result_ucs, cost = UCS_new(graph_2, start_2, goal_2)
    print("Kết quả sử dụng thuật toán UCS_new:\n", result_ucs, "với tổng chi phí là", cost)


    # Kết quả sử dụng thuật toán BFS:
    #  [0, 2, 7, 8, 10, 14, 15, 16, 17]
    # Kết quả sử dụng thuật toán DFS:
    #  [0, 3, 4, 13, 10, 14, 15, 16, 17]
    # Kết quả sử dụng thuật toán UCS_old:
    #  6919 với tổng chi phí là [0, 2, 7, 8, 10, 14, 15, 16, 17]
    # Kết quả sử dụng thuật toán UCS_new:
    #  6919 với tổng chi phí là [0, 2, 7, 8, 10, 14, 15, 16, 17]

if __name__ == "__main__":
    main()