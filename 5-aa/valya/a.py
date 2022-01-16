from collections import namedtuple

class Node(namedtuple("Node", "location left_child right_child")):
   pass
      
def insert(point, tree):  
  def _insert(point, node, depth):
    if node is None:
      return Node(
        location=point,
        left_child=None,
        right_child=None
      )
    
    axis = depth % 2
    if point[axis] <= node.location[axis]:
      return Node(
      	location= node.location,
        left_child= _insert(point, node.left_child, depth+1),
        right_child= node.right_child
      )
    else:
      return Node(
      	location= node.location,
        left_child= node.left_child,
        right_child= _insert(point, node.right_child, depth+1)
      )
    
  return _insert(point, tree, 0)
    
def contains(point, tree):
  def _contains(point, node, depth):
    if node is None:
      return False
    
    if node.location == point:
      return True
    
    axis = depth % 2
    if point[axis] <= node.location[axis]:
      return _contains(point, node.left_child, depth+1)
    else:
      return _contains(point, node.right_child, depth+1)
  return _contains(point, tree, 0)
  
def print_tree(tree):
  def print_subtree(node, prefix, children_prefix):
    if node is None:
      return prefix + "None\n"
    output = ""
    output += prefix + str(node.location) + "\n"
    output += print_subtree(node.left_child, children_prefix + "L-- ", children_prefix + "|   ")
    output += print_subtree(node.right_child, children_prefix + "L-- ", children_prefix + "   ")
    return output
    
  return print_subtree(tree, "", "")  

def select_all(tree):
  if tree is None:
    return []

  points = [tree.location]
  points += select_all(tree.left_child)
  points += select_all(tree.right_child)
  return points


def main():
  points = [(0,0), (-1,0), (1,0), (-1,1), (-100,100), (0,2)]
  
  tree = None
  for p in points:
    tree = insert(p, tree)
  
  print(print_tree(tree))
  return tree
