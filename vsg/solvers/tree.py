from typing import Union

from vsg.models import LineSegment


class EdgeNode:
    def __init__(self, edge: Union[LineSegment, None], weight,
                 left=None, right=None, parent=None):
        self._weight = weight
        self._edge = edge
        self._left = left
        self._right = right
        self._parent = parent

    @property
    def edge(self):
        return self._edge

    @property
    def weight(self):
        return self._weight

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if value is not None:
            value.parent = self
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        if value is not None:
            value.parent = self
        self._right = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def successor(self):
        if self.right is None:
            return None
        else:
            if self.right.left is None:
                return self.right
            else:
                cn = self.right.left
                while cn.left is not None:
                    cn = cn.left
                return cn

    @property
    def left_depth(self):
        if self.left is None:
            return 0
        else:
            return 1 + self.left.depth

    @property
    def right_depth(self):
        if self.right is None:
            return 0
        else:
            return 1 + self.right.depth

    @property
    def depth(self):
        return max(self.left_depth, self.right_depth)

    @property
    def balance_factor(self):
        return self.left_depth - self.right_depth

    def __repr__(self):
        return '%s [W: %.2f]' % (self.edge, self.weight)


class BalancedEdgeSearchTree:
    def __init__(self, edges=None, weights=None):
        self._root = None
        if edges is not None and weights is not None:
            for e, w in zip(edges, weights):
                self.add_node(e, w)

    @property
    def depth(self):
        if self._root is None:
            return 0
        return self._root.depth + 1

    def __repr__(self):
        return '[ROOT]| ' + self.__node2str(self._root).rstrip()

    def __node2str(self, node: EdgeNode, indent=0):
        prefix = '  ' * (indent + 1)

        s = '%s\n' % node
        if node.left is not None:
            s += prefix + '[L]|- ' + self.__node2str(node.left, indent=indent+1)
        if node.right is not None:
            s += prefix + '[R]|- ' + self.__node2str(node.right, indent=indent+1)
        return s

    def add_node(self, edge: LineSegment, weight):
        en = EdgeNode(edge, weight)

        if self._root is None:
            self._root = en
        else:
            current_node = self._root
            while True:
                if weight >= current_node.weight:
                    if current_node.right is None:
                        current_node.right = en
                        break
                    else:
                        current_node = current_node.right
                else:
                    if current_node.left is None:
                        current_node.left = en
                        break
                    else:
                        current_node = current_node.left

            # Retrace for balance
            prev_depth = current_node.depth
            prev_b = current_node.balance_factor

            while True:
                parent = current_node.parent
                if parent is None:
                    break
                gp = parent.parent

                if current_node == parent.right:
                    other_depth = parent.left_depth
                    bfactor = other_depth - (prev_depth + 1)
                    prev_depth = max(prev_depth + 1, other_depth)

                    if bfactor < -1:
                        if prev_b > 0:
                            new_root = self._rotate_rightleft(parent, current_node)
                        else:
                            new_root = self._rotate_left(parent, current_node)
                    else:
                        if bfactor == 0:
                            break
                        else:
                            current_node = parent
                            prev_b = bfactor
                            continue
                else:
                    other_depth = parent.right_depth
                    bfactor = (prev_depth + 1) - other_depth
                    prev_depth = max(prev_depth + 1, other_depth)

                    if bfactor > 1:
                        if prev_b < 0:
                            new_root = self._rotate_leftright(parent, current_node)
                        else:
                            new_root = self._rotate_right(parent, current_node)
                    else:
                        if bfactor == 0:
                            break
                        else:
                            current_node = parent
                            prev_b = bfactor
                            continue
                if gp is not None:
                    if parent == gp.left:
                        gp.left = new_root
                    else:
                        gp.right = new_root
                    break
                else:
                    self._root = new_root
                    self._root.parent = None
                    break

    def delete_node(self, edge: LineSegment, weight):
        current_node = self._root
        replace_node = None

        while current_node is not None:
            parent = current_node.parent

            if current_node.edge == edge:
                if current_node.left is None and current_node.right is None:
                    if parent is None:
                        self._root = None
                    else:
                        if current_node == parent.right:
                            parent.right = None
                        else:
                            parent.left = None
                    replace_node = parent
                elif current_node.left is not None and current_node.right is None:
                    if parent is None:
                        self._root = current_node.left
                        self._root.parent = None
                    else:
                        if current_node == parent.right:
                            parent.right = current_node.left
                        else:
                            parent.left = current_node.left
                    replace_node = current_node.left
                elif current_node.right is not None and current_node.left is None:
                    if parent is None:
                        self._root = current_node.right
                        self._root.parent = None
                    else:
                        if current_node == parent.right:
                            parent.right = current_node.right
                        else:
                            parent.left = current_node.right
                    replace_node = current_node.right
                else:
                    sc = current_node.successor
                    sc.parent.left = sc.right
                    if parent is None:
                        self._root = sc
                        self._root.parent = None
                    else:
                        if current_node == parent.right:
                            parent.right = sc
                        else:
                            parent.left = sc
                    replace_node = sc
                break
            elif weight >= current_node.weight:
                current_node = current_node.right
            else:
                current_node = current_node.left

        # Retrace for balance
        if replace_node is None:
            return

        current_node = replace_node
        prev_depth = current_node.depth
        while True:
            parent = current_node.parent
            if parent is None:
                break
            gn = parent.parent

            if current_node == parent.left:
                other_depth = parent.right_depth
                bfactor = other_depth - (prev_depth + 1)
                prev_depth = max(prev_depth + 1, other_depth)

                if bfactor < -1:
                    z = parent.right
                    b = z.balance_factor
                    if b > 0:
                        new_root = self._rotate_rightleft(parent, z)
                    else:
                        new_root = self._rotate_left(parent, z)
                else:
                    if bfactor == -1:
                        break
                    else:
                        current_node = parent
                        continue
            else:
                other_depth = parent.left_depth
                bfactor = (prev_depth + 1) - other_depth
                prev_depth = max(prev_depth + 1, other_depth)

                if bfactor > 1:
                    z = parent.left
                    b = z.balance_factor
                    if b < 0:
                        new_root = self._rotate_leftright(parent, z)
                    else:
                        new_root = self._rotate_right(parent, z)
                else:
                    if bfactor == 1:
                        break
                    else:
                        current_node = parent
                        continue

            if gn is None:
                self._root = new_root
                self._root.parent = None
            else:
                if parent == gn.left:
                    gn.left = new_root
                else:
                    gn.right = new_root
                if b == 0:
                    break


    @staticmethod
    def _rotate_rightleft(parent, child):
        lc = child.left
        lc.right = child
        lc.left = parent

        parent.right = None
        child.left = None
        lc.parent = None

        return lc

    @staticmethod
    def _rotate_leftright(parent, child):
        rc = child.right
        rc.left = child
        rc.right = parent

        rc.parent = None
        parent.left = None
        child.right = None

        return rc

    @staticmethod
    def _rotate_left(parent, child):
        mv = child.left
        parent.right = mv
        child.left = parent
        return child

    @staticmethod
    def _rotate_right(parent, child):
        mv = child.right
        parent.left = mv
        child.right = parent
        return child
