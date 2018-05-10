# Visibility Graph & Shortest Path
Algorithms for constructing visibility graphs and calculating shortest obstructed path in Python.

## Quickstart
Requirements:
 - Python 3.5 or above
```bash
git clone https://github.com/lanPN85/visi-graph
cd visi-graph
pip3 install -r requirements.txt

# Run a sample input using brute force
# Results can be found in the out/ directory
python3 main.py -i data/ggb/vg-1.ggb
```

## Input format
### Geogebra
Allows reading of [Geogebra](https://www.geogebra.org/graphing)'s .ggb file format. Configurations can be drawn using the tool, exported and then used by visi-graph.

Conventions on Geogebra input:
- Starting points must always be labeled 'S'.
- Ending points must always be labeled 'T'.
- Polygons must be drawn using the polygon tool (not by connecting multiple lines)

For examples, see the `data/ggb` directory.

## Current implementations

### Visibility graph
- Brute force checking (`O(n^3)`)
- Rotational plane sweep (`O(n^2logn)`)

### Shortest path
- Dijkstra's algorithm
