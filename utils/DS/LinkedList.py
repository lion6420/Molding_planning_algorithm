class Node:
  def __init__(self, value):
    self.value = value
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None
    self.length = 0

  def add(self, value):
    newNode = Node(value)
    if (self.length == 0):
      self.head = newNode
      self.tail = newNode
    else:
      self.tail.next = newNode
      self.tail = newNode
    self.length+=1

  def delete(self, index):
    node = self.head
    lastNode = None
    if (index >= self.length):
      return None
    if (index == 0): # if 刪除head
      self.head = node.next
      node.next = None
    else:
      while(index>0): # traverse到要刪除的index
        lastNode = node
        node = node.next
        index-=1

      lastNode.next = node.next
      node.next = None
      if (index == self.length-1): # if 刪除最後一個
        self.tail = lastNode
    self.length-=1

    return node

  def insert(self, index, value):
    newNode = Node(value)
    if (index >= self.length):
      return None
    if (index == 0): # if 插入head位置
      newNode.next = self.head
      self.head = newNode
    
    else:
      while(index>0): # traverse到要insert的index
        lastNode = node
        node = node.next
        index-=1

      newNode.next = lastNode.next
      lastNode.next = newNode   
      if (index == self.length-1): # if insert在最後一個位置
        self.tail = newNode

    self.length+=1
    