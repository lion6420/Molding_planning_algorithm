from utils.DS.LinkedList import LinkedList, Node

class ReadyQueue():
  def __init__(self):
    self.orderList = LinkedList()

  def enqueue(self, order):
    self.orderList.add(order)

  def dequeue(self):
    removedOrder = self.orderList.delete(0)
    return removedOrder

  def InsertionSort(self):
    dummyOrder = {'priority': -1}
    dummy = Node(dummyOrder)
    current = self.orderList.head

    while(current!=None):
      node = dummy
      while(node.next!=None and node.next.value['priority'] < current.value['priority']):
        node = node.next
      temp = current.next
      current.next = node.next
      node.next = current
      current = temp

    self.orderList.head = dummy.next

  def get_orderNumber(self):
    return self.orderList.length

  def printPriority(self):
    node = self.orderList.head
    while(node):
      print(node.value['priority'])
      node = node.next
         