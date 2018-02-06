from typing import List

from vsg.models import Point, Polygon, VisibilityGraph, LineSegment


def plot_polygon(polygon: Polygon, axes, *args, point_color=None, **kwargs):
    for e in polygon.edges:
        plot_line(e, axes, *args, point_color=point_color, **kwargs)


def plot_point(point: Point, axes, *args, **kwargs):
    axes.plot(point.x, point.y, 'o', *args, **kwargs)


def plot_line(line: LineSegment, axes, *args, point_color=None, **kwargs):
    axes.plot([line.p1.x, line.p2.x], [line.p1.y, line.p2.y], *args, **kwargs)

    if point_color is not None:
        kwargs['color'] = point_color
    kwargs.pop('label', None)

    plot_point(line.p1, axes, *args, **kwargs)
    plot_point(line.p2, axes, *args, **kwargs)


def plot_path(path: List[Point], axes, *args, point_color=None, **kwargs):
    x = list(map(lambda p: p.x, path))
    y = list(map(lambda p: p.y, path))
    axes.plot(x, y, *args, **kwargs)

    if point_color is not None:
        kwargs['color'] = point_color
    kwargs.pop('label', None)

    for _x, _y in zip(x, y):
        plot_point(Point(_x, _y), axes, *args, **kwargs)


def plot_initial_state(s: Point, t: Point, obstacles: List[Polygon], axes):
    plot_point(s, axes, color='teal', label='Start point')
    plot_point(t, axes, color='orange', label='End point')
    for obs in obstacles:
        plot_polygon(obs, axes, color='black', point_color='black')


def plot_visi_graph(graph: VisibilityGraph, axes, obstacles=None):
    for segment in graph.segments:
        plot_line(segment, axes, point_color='black', color='green')

    if obstacles is not None:
        for obs in obstacles:
            plot_polygon(obs, axes, point_color='black', color='black')

    plot_point(graph.start, axes, color='teal', label='Start point')
    plot_point(graph.end, axes, color='orange', label='End point')


def plot_shortest_path(path: List[Point], axes, obstacles=None):
    if obstacles is not None:
        for obs in obstacles:
            plot_polygon(obs, axes, point_color='black', color='black')

    plot_path(path, axes, point_color='red', color='red', label='Path')
    plot_point(path[0], axes, color='teal', label='Start point')
    plot_point(path[-1], axes, color='orange', label='End point')
