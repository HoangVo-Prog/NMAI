#!/usr/bin/env bash
python src/main.py --algo astar --start Arad --goal Hirsova --plot --out route_astar.png
python src/main.py --algo gbfs  --start Arad --goal Hirsova --plot --out route_gbfs.png
