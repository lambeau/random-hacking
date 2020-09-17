class Node:
    left = None
    right = None

    def __init__(self, value):
        self.value = value

    def insert(self, new_value):
        current_node = self
        while True:
            if new_value < current_node.value:
                if current_node.left is None:
                    current_node.left = Node(new_value)
                    break
                else:
                    current_node = current_node.left
            elif new_value > current_node.value:
                if current_node.right is None:
                    current_node.right = Node(new_value)
                    break
                else:
                    current_node = current_node.right


def find_path(root, value):
    current_node = root
    path = []
    while current_node:
        path.append(current_node.value)
        if value == current_node.value:
            break
        elif value < current_node.value and current_node.left is not None:
            current_node = current_node.left
        elif value > current_node.value and current_node.right is not None:
            current_node = current_node.right
        else:
            return None
    return path if len(path) > 0 else None


def find_distance(num, values, node_1, node_2):
    if not values or num < 1 or len(set(values)) != num:
        return -1

    # build tree
    root = Node(values[0])
    for value in values[1:]:
        root.insert(value)

    # find paths
    node_1_path = find_path(root, node_1)
    node_2_path = find_path(root, node_2)
    if node_1_path is None or node_2_path is None:
        return -1

    # remove common edges
    while len(node_1_path) > 0 and len(node_2_path) > 0 and node_1_path[0] == node_2_path[0]:
        node1_path = node_1_path[1:]
        node2_path = node_2_path[1:]
    return len(node_1_path) + len(node_2_path)
