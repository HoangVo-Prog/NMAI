# AI Search on Romania Map

Cài đặt Greedy Best First Search và A* tìm đường trên bản đồ Romania. Dữ liệu đọc từ `heuristic.txt`, `cities.txt`, `citiesGraph.txt`. Có chức năng vẽ đường đi.

## Cấu trúc thư mục

```
ai-search-romania/
├── README.md
├── requirements.txt
├── data/
│   ├── heuristic.txt
│   ├── cities.txt
│   └── citiesGraph.txt
└── src/
    ├── data_loader.py
    ├── search.py
    ├── plot_map.py
    └── main.py
```

## Cài đặt

Python 3.10 trở lên.

```bash
pip install -r requirements.txt
```

## Chạy nhanh

Từ thư mục gốc:

```bash
python -m src.main --algo astar --start Arad --goal Hirsova --plot --out route_astar.png
python -m src.main --algo gbfs  --start Arad --goal Hirsova --plot --out route_gbfs.png
```

Console sẽ in đường đi, tổng chi phí, số nút mở rộng. Hình sẽ lưu tại file PNG tương ứng.

## Định dạng tệp dữ liệu

- `data/heuristic.txt`: mỗi dòng `City h_value`

- `data/cities.txt`: mỗi dòng `City x y` dùng để vẽ

- `data/citiesGraph.txt`: mỗi dòng `CityA CityB distance` là cạnh vô hướng

Các tên thành phố dùng dấu gạch dưới thay cho dấu cách, ví dụ `Rimnicu_Vilcea`.
