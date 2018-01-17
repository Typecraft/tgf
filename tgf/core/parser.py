import json
import xml.etree.ElementTree as ET
from io import BytesIO

from tgf.core.tree import Tree, Node


def _parse_node_attributes(node_etree):
    """
    Parses the attributes of a node etree.

    :param node_etree: An etree representation of the node.
    :return: A Node object.
    """
    attributes = {}

    for attribute in node_etree.findall('attribute'):
        key = attribute.attrib['name']
        value = attribute.text

        attributes[key] = value

    return attributes


def _parse_node(node_etree):
    """
    Parses an etree-representation of a Node.

    :param node_etree: An etree representation of a node.
    :return: A Node object.
    """
    parsed_node = Node()
    parsed_node.node_type = node_etree.attrib.get('type')
    parsed_node.add_attributes(_parse_node_attributes(node_etree))
    parsed_node.add_children(map(_parse_node, node_etree.findall('node')))

    return parsed_node


def _parse_tgf(tgf_etree):
    """
    Parses the root-tgf node of a tgf xml document.

    :param tgf_etree: The tgf root xml node
    :return: An etree
    """
    tree = tgf_etree.find('tree')

    parsed_tree = Tree()

    for node_etree in tree.findall('node'):
        parsed_node = _parse_node(node_etree)
        parsed_tree.add_root(parsed_node)

    return parsed_tree


def parse_file(filename_or_fp):
    """
    Parses a file (by filename or fp) on the .tgf.xml format into a Tree.

    :param filename_or_fp: A file object or a filename.
    :return: A Tree.
    """
    tgf_etree = ET.parse(filename_or_fp)
    return _parse_tgf(tgf_etree)


def parse_string(tgf_xml_string):
    """
    Parses a string-representation of a xml.

    :param tgf_xml_string: A string representing a tgf-xml-string.
    :return: A Tree.
    """
    tgf_etree = ET.fromstring(tgf_xml_string)
    return _parse_tgf(tgf_etree)


def _serialize_node_attributes(node_etree, node):
    """
    Serializes a Node objects attributes.

    :param node_etree:
    :param node:
    :return:
    """
    for k, v in node.attributes.items():
        attribute_etree = ET.SubElement(node_etree, 'attribute', name=k)
        attribute_etree.text = v


def _serialize_node(parent_etree, node):
    """
    Serializes a Node object into an ElementTree representation.

    :param parent: The etree-parent element to nest this node under.
    :param node: The Node object to serialize.
    :return: void, all additions are done in-place.
    """
    node_etree = ET.SubElement(parent_etree, 'node', type=node.node_type)
    _serialize_node_attributes(node_etree, node)

    for child in node.child_nodes:
        _serialize_node(node_etree, child)


def _serialize_tree(tree):
    """
    Serializes a Tree into an ElementTree representation.

    :param tree:
    :return:
    """
    root_etree = ET.Element('tgf', {'version': '1.0'})
    tree_etree = ET.SubElement(root_etree, 'tree')

    for root in tree.roots:
        _serialize_node(tree_etree, root)

    return ET.ElementTree(root_etree)


def serialize_to_string(tree):
    """
    Serializes a Tree object into a xml-representation of the tree.

    :param tree: A Tree object.
    :return: A string with the serialized tree.
    """
    serialized = _serialize_tree(tree)
    f = BytesIO()
    serialized.write(f, encoding="UTF-8", xml_declaration=True)
    return f.getvalue()


def serialize_to_file(tree, filename_or_fp):
    """
    Serializes a Tree object into a xml-representation of the tree, and saves it
    to a file.

    :param tree: A Tree object.
    :param filename_or_fp: Either a file object, or a path to a file.
    :return: void
    """
    serialized = _serialize_tree(tree)
    serialized.write(filename_or_fp, encoding="UTF-8", xml_declaration=True)


def serialize_json_to_string(tree):
    """
    Serializes a Tree object into a json-representation of the tree.

    :param tree: A tree Object
    :type tree: Tree
    :return: A string with the serialized tree
    """
    return json.dumps(tree.to_dict())


def serialize_json_to_file(tree, filename_or_fp):
    """
    Serializes a Tree object into a json-representation of the tree, and saves it
    to a file.

    :param tree: A tree Object
    :type tree: Tree
    :param filename_or_fp: Either a file object, or a path to a file.
    :return: void
    """
    json.dump(filename_or_fp, tree)
