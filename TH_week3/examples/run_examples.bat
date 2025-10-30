@echo off
python -m src.main --algo astar --start Arad --goal Hirsova --plot --out route_astar.png
python -m src.main --algo gbfs  --start Arad --goal Hirsova --plot --out route_gbfs.png
