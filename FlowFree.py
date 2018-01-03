from random import randint, shuffle
import sys

class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.startValue = False
        self.availableColors = []

class Puzzle:
    # Variables: Nodes in the puzzle
    # Domain: List of starting colors, ie [(, colors)]
    # Constraints: Each variable can be only one color, all variables of the
    # same color must be connected either vertically or horizontally, all variables
    # must have a color, for none start nodes at most two connected nodes can be
    # the same color

    def __init__(self, filename):
        self.startingValues = []
        self.colList = []
        self.colsInMaze = 0
        self.rowsInMaze = 0
        self.colors = []
        self.emptyNodes = 0
        self.numAssignments = 0
        self.endPoints = []

        puzzleObject = open(filename, 'r')
        rows = 0

        for line in puzzleObject:
            rowList = []
            cols = 0

            for char in line[:-1]:
                node = Node(rows, cols, char)

                if char != '_':
                    node.startValue = True
                    exists = False
                    for color in self.colors:
                        if char == color:
                            exists = True
                    if not exists:
                        self.colors.append(char)
                    self.endPoints.append(node)
                else:
                    self.emptyNodes += 1

                rowList.append(node)

                cols += 1

            rows += 1

            self.colList.append(rowList)
            self.colsInMaze = len(rowList)

        self.rowsInMaze = rows

    def printPuzzle(self):
        for row in self.colList:
            line = ""
            for node in row:
                line += node.value
            print(line)

    def btAlgorithm(self):
        #print("Starting backtracking...")
        #print(self.colors)
        if self.goalTest():
            #print("Goal Found")
            return True

        nextNode = self.getRandomUnassignedNode()
        if nextNode == None:
            #print("No Nodes")
            return None
        else:
            #print(str(nextNode.row) + "," + str(nextNode.col))
            pass

        self.randomOrderColors()
        for color in self.colors:
            #print("Checking color: " + color)
            if self.meetsSmartContraints(nextNode, color):
                self.numAssignments += 1
                nextNode.value = color
                self.emptyNodes -= 1
                #self.printPuzzle()
                #input("Press Enter to continue")
                currentState = self.btAlgorithm()
                if currentState != None:
                    return currentState
                else:
                    nextNode.value = '_'
                    self.emptyNodes += 1
        return None

    def randomOrderColors(self):
        shuffle(self.colors)

    def smartBtAlgorithm(self):
        #print("Starting backtracking...")
        #print(self.colors)
        if self.goalTest():
            #print("Goal Found")
            return True

        nextNode = self.getUnassignedNode()
        if nextNode == None:
            #print("No Nodes")
            return None
        else:
            #print(str(nextNode.row) + "," + str(nextNode.col))
            pass

        self.orderColors(nextNode)
        for color in self.colors:
            #print("Checking color: " + color)
            if self.meetsSmartContraints(nextNode, color):
                self.numAssignments += 1
                nextNode.value = color
                self.emptyNodes -= 1
                #self.printPuzzle()
                #input("Press Enter to continue")
                currentState = self.smartBtAlgorithm()
                if currentState != None:
                    return currentState
                else:
                    nextNode.value = '_'
                    self.emptyNodes += 1
        return None

    def smarterBtAlgorithm(self):
        #print("Starting backtracking...")
        #print(self.colors)
        if self.goalTest():
            #print("Goal Found")
            return True

        nextNode = self.getBestUnassignedNode()
        if nextNode == None:
            #print("No Nodes")
            return None
        else:
            #print(str(nextNode.row) + "," + str(nextNode.col))
            pass

        self.orderColors(nextNode)
        for color in nextNode.availableColors:
            #print("Checking color: " + color)
            if self.meetsSmartContraints(nextNode, color):
                self.numAssignments += 1
                nextNode.value = color
                self.emptyNodes -= 1
                #self.printPuzzle()
                #input("Press Enter to continue")
                currentState = self.smarterBtAlgorithm()
                if currentState != None:
                    return currentState
                else:
                    nextNode.value = '_'
                    self.emptyNodes += 1
        return None

    def orderColors(self, node):
        adjacentNodes = self.getAdjacentNodes(node)
        colorCount = {}
        for color in self.colors:
            colorCount[color] = 0
        for adjacentNode in adjacentNodes:
            if adjacentNode.value != '_':
                colorCount[adjacentNode.value] += 1
        sortedColors = sorted(colorCount.items(), key=lambda x: x[1], reverse=True)
        node.availableColors = []
        for color, count in sortedColors:
            node.availableColors.append(color)

    def sortColors(self):
        colors = {}
        for color in self.colors:
            startingNode = None
            for node in self.endPoints:
                if node.value == color:
                    if startingNode == None:
                        startingNode = node
                    else:
                        distance = abs(startingNode.row - node.row) + abs(startingNode.col - node.col)
                        colors[color] = distance
        sortedColors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
        self.colors = []
        for color, distance in sortedColors:
            self.colors.append(color)

    def getUnassignedNode(self):
        availableNodes = []
        for row in self.colList:
            for node in row:
                if node.value == '_':
                    availableNodes.append(node)

        if len(availableNodes) == 0:
            return None

        return availableNodes[0]

    def getBestUnassignedNode(self):
        # Assign constraints to available nodes
        numColors = sys.maxsize
        mostConstrained = None

        for row in self.colList:
            for node in row:
                if node.value == '_':
                    node.availableColors = []
                    #print(str(node.row) + "," + str(node.col))
                    for color in self.colors:
                        #print(color)
                        if self.meetsSmartContraints(node, color):
                            #print("Add: " + color)
                            node.availableColors.append(color)
                    if len(node.availableColors) == 0:
                        return None
                    if len(node.availableColors) < numColors:
                        mostConstrained = node
                        numColors = len(node.availableColors)
                    elif len(node.availableColors) == numColors:
                        if self.evalConstraints(node) < self.evalConstraints(mostConstrained):
                            mostConstrained = node
                            numColors = len(node.availableColors)
        #print(str(mostConstrained.row) + "," + str(mostConstrained.col))

        return mostConstrained

    def evalConstraints(self, node):
        adjacentNodes = self.getAdjacentNodes(node)

        count = 0
        for adjacentNode in adjacentNodes:
            if adjacentNode == '_':
                count += 1
        return count

    def getRandomUnassignedNode(self):
        availableNodes = []
        for row in self.colList:
            for node in row:
                if node.value == '_':
                    availableNodes.append(node)


        if len(availableNodes) == 0:
            return None

        randNode = availableNodes[randint(0, len(availableNodes) - 1)]
        return randNode

    def getAdjacentNodes(self, node):
        adjacentNodes = []

        # Top Node
        if node.row > 0:
            adjacentNodes.append(self.colList[node.row - 1][node.col])
        # Bottom Node
        if node.row < self.rowsInMaze - 1:
            adjacentNodes.append(self.colList[node.row + 1][node.col])
        # Left Node
        if node.col > 0:
            adjacentNodes.append(self.colList[node.row][node.col - 1])
        # Right Node
        if node.col < self.colsInMaze - 1:
            adjacentNodes.append(self.colList[node.row][node.col + 1])

        return adjacentNodes

    def meetsContraints(self, node, color):
        adjacentNodes = self.getAdjacentNodes(node)

        # Check to make sure node is not Isolated
        matchingColorNodes = 0
        for otherNode in adjacentNodes:
            if otherNode.value == '_' or otherNode.value == color:
                matchingColorNodes += 1
        if node.startValue and matchingColorNodes < 1:
            #print("Failed Constraint: No matching adjacent nodes")
            return False
        if not node.startValue and matchingColorNodes < 2:
            return False

        # Check for zig-zag pattern on non-start nodes
        for otherNode in adjacentNodes:
            matchingColorNodes = 0
            if otherNode.startValue == False:
                otherAdjacentNodes = self.getAdjacentNodes(otherNode)
                for otherAdjNode in otherAdjacentNodes:
                    if otherAdjNode.value == color:
                        matchingColorNodes += 1
                if matchingColorNodes >= 2:
                    #print("Failed Constraint: Zig-zag pattern")
                    return False

        # All contraints pass
        return True

    def meetsSmartContraints(self, node, color):
        adjacentNodes = self.getAdjacentNodes(node)

        # Forward Checking
        # Check to make sure node is not isolating an adjacent node
        for otherNode in adjacentNodes:
            if otherNode.value != '_':
                matchingColorNodes = 0
                otherAdjacentNodes = self.getAdjacentNodes(otherNode)
                for otherAdjNode in otherAdjacentNodes:
                    if otherAdjNode.value == otherNode.value or otherAdjNode.value == '_':
                        matchingColorNodes += 1
                    if otherNode.value == color:
                        matchingColorNodes += 1
                if otherNode.startValue:
                    if matchingColorNodes <= 1:
                        #print("Failed Constraint: Isolated starting node: " + str(otherNode.row) + "," + str(otherNode.col))
                        return False
                else:
                    if matchingColorNodes <= 2:
                        #print("Failed Constraint: Isolated non-starting node: " + str(otherNode.row) + "," + str(otherNode.col))
                        return False

        # Check to make sure node is not Isolated
        matchingColorNodes = 0
        for otherNode in adjacentNodes:
            if otherNode.value == '_' or otherNode.value == color:
                matchingColorNodes += 1
        if node.startValue and matchingColorNodes < 1:
            #print("Failed Constraint: No matching adjacent nodes")
            return False
        if not node.startValue and matchingColorNodes < 2:
            return False

        # Check for zig-zag pattern on non-start nodes
        for otherNode in adjacentNodes:
            matchingColorNodes = 0
            if otherNode.startValue == False:
                otherAdjacentNodes = self.getAdjacentNodes(otherNode)
                for otherAdjNode in otherAdjacentNodes:
                    if otherAdjNode.value == color:
                        matchingColorNodes += 1
                if matchingColorNodes >= 2:
                    #print("Failed Constraint: Zig-zag pattern")
                    return False

        # All contraints pass
        return True

    def goalTest(self):
        if self.emptyNodes == 0:
            self.printPuzzle()
            return True
        else:
            return False
