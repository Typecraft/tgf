

class Node(object):
    """
    Class representing a node.
    """

    def __init__(
        self,
        root=None,
        attributes=None,
        children=None,
        **kwargs
    ):
        """
        Constructor.
        :param root: Optional reference to the root node.
        :param attributes: Optional argument accepting an initial dictionary of attributes. Will call `add_attributes`.
        :param child_nodes:  Optional argument accepting an initial list of child nodes. Will call `add_childs`.
        :param kwargs: Some kwargs that we send to the attributes object.
        """
        self.attributes = {}
        self.child_nodes = []
        self.root = root

        if attributes is not None and isinstance(attributes, dict):
            self.add_attributes(attributes)

        if attributes is not None and hasattr(children, '__iter__'):
            self.add_children(children, **kwargs)

    def add_attribute(self, key, value):
        """
        Adds an attribute to the node.
        :return: Void
        """
        self.attributes[key] = value

    def add_attributes(self, attributes={}, **kwargs):
        """
        Merges a dictionary of attributes with the current attributes.
        :param attributes: A dictionary of attributes.
        :param kwargs: Other kwargs that is also added.
        :return: Void
        """
        if not isinstance(attributes, dict):
            raise Exception('Bad input to Node#add_attributes. Expected dict, got %s' % str(type(attributes)))
        assert isinstance(attributes, dict)
        self.attributes.update(attributes, **kwargs)

    def remove_attribute(self, key):
        """
        Removes a named attribute from the node.
        :return: Void
        """
        del self.attributes[key]

    def clear_attributes(self):
        """
        Clears all attributes from the node.
        :return: Void
        """
        self.attributes.clear()

    def add_children(self, children):
        """
        Adds an iterable of child nodes to the node.

        :param children:
        :return: Void
        """
        if not hasattr(children, '__iter__'):
            raise Exception('Invalid argument to add_children. Expect something iterable.')

        for child in children:
            self.add_child(child)

    def add_child(self, child):
        """
        Adds a Node-instance as a child of this node.
        :param child: A Node-instance.
        :return: void
        """
        assert isinstance(child, Node)

        self.child_nodes.append(child)

    def remove_child(self, child):
        """
        Removes a Node-instance as a child of this node.
        :param child: A Node-instance
        :return: void
        """
        assert isinstance(child, Node)

        self.child_nodes.remove(child)


class Tree(object):
    """
    Class representing a TGF-tree.

    The class simply wraps a root-node.
    """
    def __init__(
        self,
        root=None
    ):
        """
        Constructor.
        :param root: Optional root node.
        """
        if root is not None:
            assert isinstance(root, Node)

        self.root = root

