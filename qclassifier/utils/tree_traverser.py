from nltk.tree import Tree


class TreebankNodeVisitor(object):

    def visit(self, tree_node):
        raise NotImplementedError()


def dfs_traverse_tree(parsed_tree, visitor):
    """
    Note that any non-tree-structure leave node is ignored
    :param parsed_tree: root of the Tree to be traversed
    :param visitor: the visitor will be applied to all the subtrees under the given root, in DFS order
    """
    if not isinstance(parsed_tree, Tree):
        return
    for child in parsed_tree:
        dfs_traverse_tree(child, visitor)
    # visit current node after visited all the children
    visitor.visit(parsed_tree)


