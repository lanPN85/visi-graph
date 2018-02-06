# Visibility Graph & Shortest Path
Algorithms for constructing visibility graphs and calculating shortest obstructed path in Python.

## Quickstart
Requirements:
 - Python 3.5 or above
```
git clone https://github.com/lanPN85/visi-graph
cd visi-graph
pip install -r requirements.txt
```

## Input format
### Geogebra
Allows reading of [Geogebra](https://www.geogebra.org/geometry)'s .ggb file types. Configurations can be drawn using the tool, exported and then used by visi-graph.

Conventions on Geogebra input:
- Starting points must always be labeled 'S'.
- Ending points must always be labeled 'T'.

For examples, see the `data/ggb` directory.

## Current implementations

### Visibility graph
- Brute force checking (`O(n^3)`)

### Shortest path
- Dijkstra's algorithm
