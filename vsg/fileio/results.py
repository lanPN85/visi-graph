"""
Stores and retrieves results from custom XML files.
"""

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
from typing import List

from vsg.models import Point, VisibilityGraph, LineSegment


def path_to_xml(path: List[Point], filepath: str):
    root = Element('path')
    for p in path:
        _node = SubElement(root, 'point', {
            'x': str(p.x), 'y': str(p.y)
        })

    tree_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='    ')
    with open(filepath, 'w') as f:
        f.write(tree_str)


def path_from_xml(filepath: str):
    with open(filepath, 'r') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        path = []
        for node in root.iter('point'):
            x = float(node.get('x'))
            y = float(node.get('y'))
            path.append(Point(x, y))

    return path


def graph_to_xml(graph: VisibilityGraph, filepath: str):
    root = Element('vgraph')

    s = SubElement(root, 'start', {
        'x': str(graph.start.x), 'y': str(graph.start.y)
    })
    t = SubElement(root, 'end', {
        'x': str(graph.end.x), 'y': str(graph.end.y)
    })

    for sg in graph.segments:
        _snode = SubElement(root, 'segment')
        _p1 = SubElement(_snode, 'point', {
            'x': str(sg.p1.x), 'y': str(sg.p1.y)
        })
        _p2 = SubElement(_snode, 'point', {
            'x': str(sg.p2.x), 'y': str(sg.p2.y)
        })

    tree_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent='    ')
    with open(filepath, 'w') as f:
        f.write(tree_str)


def graph_from_xml(filepath: str):
    with open(filepath, 'r') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        snode = tree.find('start')
        s = Point(float(snode.get('x')), float(snode.get('y')))
        tnode = tree.find('end')
        t = Point(float(tnode.get('x')), float(tnode.get('y')))

        segments = []
        for node in root.iter('segment'):
            pnodes = node.findall('point')
            p1 = Point(float(pnodes[0].get('x')), float(pnodes[0].get('y')))
            p2 = Point(float(pnodes[1].get('x')), float(pnodes[1].get('y')))
            segments.append(LineSegment(p1, p2))

        graph = VisibilityGraph(s, t, segments)

    return graph
