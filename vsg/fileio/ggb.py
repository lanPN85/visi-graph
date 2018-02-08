import zipfile
import re
import numpy as np

from xml.etree import ElementTree

from vsg.models import Point, Polygon


def _point_from_element(element):
    x = float(element.find('coords').get('x'))
    y = float(element.find('coords').get('y'))
    x = float(np.around(x, 5))
    y = float(np.around(y, 5))
    return Point(x, y)


def config_from_ggb(path):
    with zipfile.ZipFile(path, mode='r') as ggbf:
        with ggbf.open('geogebra.xml') as f:
            tree = ElementTree.parse(f)
            root = tree.getroot()
            constr = root.find('construction')

            s_el = constr.find("./element[@type='point'][@label='S']")
            t_el = constr.find("./element[@type='point'][@label='T']")
            s = _point_from_element(s_el)
            t = _point_from_element(t_el)

            p_els = constr.findall("./element[@type='point']")
            p_els.remove(s_el)
            p_els.remove(t_el)

            points = {}
            for el in p_els:
                name = el.get('label')
                pos = _point_from_element(el)
                points[name] = pos

            poly_els = constr.findall("./command[@name='Polygon']/input")
            obstacles = []
            ppattern = re.compile('a[0-9]+')
            for el in poly_els:
                attrs = el.attrib
                plist = []
                for k, v in attrs.items():
                    if re.match(ppattern, k):
                        pname = el.get(k)
                        p = points[pname]
                        plist.append(p)
                obstacles.append(Polygon(plist))

            return s, t, obstacles

