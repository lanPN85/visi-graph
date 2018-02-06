from typing import List

from vsg.models import VisibilityGraph, Coordinate


def dijkstra(graph: VisibilityGraph) -> List[Coordinate]:
    if not graph.constructed:
        graph.construct_adj_list()

    vertices, edges = graph.vertices, graph.adjacent_list
    distances, checked, prev = {}, set(), {}
    for v in vertices:
        distances[v] = float('inf')
        prev[v] = None
    distances[graph.start] = 0.

    while len(checked) < len(vertices):
        u_dist = dict(filter(lambda x: x[0] not in checked, distances.items()))  # Only consider unchecked vertices
        sv = min(u_dist.items(), key=lambda x: x[1])[0]  # Select vertex with smallest distance

        checked.add(sv)
        for node in edges[sv]:
            tv, w = node.coord, node.w  # Extract adjacent vertex tv and distance w
            total_w = distances[sv] + w
            if tv not in checked and total_w < distances[tv]:
                distances[tv] = total_w
                prev[tv] = sv

    # Construct path to graph.end using back-tracing
    path = [graph.end]
    cv = graph.end
    while cv != graph.start:
        cv = prev[cv]
        path.append(cv)

    path = list(reversed(path))  # Reverse stack for actual path

    return path
