# Frame
# index    col1    col2    col3    col4
#   0   [   a1,     b1,     c1,     d1   ]
#   1   [   a2,     b2,     c2,     d2   ]
#   2   [   a3,     b3,     c3,     d3   ]
#   3   [   a4,     b4,     c4,     d4   ]

from .LinkedList import LinkedList, Node

class Header:
  def __init__(self, cols):
    self.cols = cols
    self.headerMap = {}
    for c_index, col in enumerate(self.cols):
      self.headerMap.update({
        col: c_index
      })

  def getHeaderIndex(self, value):
    return self.headerMap[value]

class Body:
  def __init__(self, data, cols):
    self.bodyMap = {}
    self.cols = cols
    self.head = None
    self.data = data
    self.constructBody()

  def constructBody(self):
    lastNode = None
    for r_index, row in enumerate(self.data):
      currentNode = Node(r_index)

      # new BodyRow
      bodyRow = BodyRow(r_index, row, self.cols)
      bodyRow.rowPtr = currentNode

      self.bodyMap.update({
        r_index: bodyRow
      })

      # Link the next Node
      if(lastNode == None):
        self.head = currentNode
      else:
        lastNode.next = currentNode
      lastNode = currentNode

  def getRow(self, index):
    return self.bodyMap[index]


class BodyRow:
  def __init__(self, index, data, cols):
    self.rowPtr = Node(index)
    self.data = data
    self.header = Header(cols)

  def __getitem__(self, colName):
    colIndex = self.header.getHeaderIndex(colName)
    return self.data[colIndex]
  
  def toList(self):
    return list(self.data)


class Frame:
  def __init__(self, data, cols=[]):
    self.body = Body(data, cols)
    self.header = Header(cols)
    self.cols = cols
    self.data = data
    self.height = len(data)

  def __getitem__(self, index):
    resultRow = self.body.getRow(index)
    return resultRow

  def __str__(self):
    printStr = ''
    for col in self.cols:
      printStr = printStr + '   ' + col
    printStr = printStr + '\n'
    for row in self.data:
      for row_ele in row:
        printStr = printStr + '   ' + str(row_ele)
      printStr = printStr + '\n'
    return printStr
    

        