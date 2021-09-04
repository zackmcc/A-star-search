'''
Zackary McClamma
CPS 580 - Artificial Intelligence
16 June 2020
'''

from operator import attrgetter
import time
#This is the only file you need to work on. You do NOT need to modify other files

# Below are the functions you need to implement. For the first project, you only need to finish implementing bfs() and dfs()

from queue import Queue
from game.Node import Node
from collections import deque #This allows for a list to be used as a queue
import copy # This was so I could make a copy of a node instead of passing references (Python default)
import sys

#here you need to implement the Breadth First Search Method

def bfs(puzzle):
    path = []
    index = 0
    #puzzle = [0, 5, 6, 4, 2, 1, 3, 7, 8]
    # 10 moves
    #puzzle = [8, 1, 2, 0, 6, 4, 7, 3, 5]

    # 20 moves
    #puzzle = [6, 0, 1, 5, 8, 7, 2, 3, 4]
    current = Node(0, puzzle, 0)
    checked = []

    # If the game starts in the goal state return the path with no moves
    if checkGoalState(current.puzzle):
        return path

    checked.append(current.puzzle)
    q = deque()
    q.append(current)

    finished = 0
    start = time.time()
    while q.__len__() > 0 | finished:

        # pull the node off the queue
        current = q.popleft()
        if checkGoalState(current.puzzle):
            break

        new_pos = getNewPositions(current.puzzle)
        for i in range(1, new_pos.__len__()):
            if new_pos[i] >= 0:
                temp = moveSpace(current, new_pos[i], new_pos[0])
                if ~checkForDuplicateState(temp.puzzle, checked):
                    finished = checkGoalState(temp.puzzle)
                    q.append(temp)
                    checked.append(temp.puzzle)
                    if finished:
                        break

    while current.parent != 0:
        path.append(current.cost)
        current = current.parent

    end = time.time()
    elapsed_time = (end - start) * 1000
    print("BFS elapsed time: " + elapsed_time.__str__() + " ms")
    print(path[::-1])
    return path[::-1]


#here you need to implement the Depth First Search Method
def dfs(puzzle):
    path = []
    start = Node(0, puzzle, 0)
    end = dfsHelper(start)
    while end.parent != 0:
        path.append(end.cost)
        end = end.parent
    print(path[::-1])
    return path[::-1]


#This will be for next project
def astar(puzzle):
    #puzzle = [8, 7, 6, 5, 4, 3, 2, 1, 0]
    #puzzle = [0, 5, 6, 4, 2, 1, 3, 7, 8]
    #puzzle = [0, 1, 2, 8, 3, 4, 6, 7, 5]
    # 10 moves
    #puzzle = [8, 1, 2, 0, 6, 4, 7, 3, 5]

    # 20 moves
    #puzzle = [6, 0, 1, 5, 8, 7, 2, 3, 4]

    #50 moves
    #puzzle = [3, 0, 8, 7, 1, 2, 4, 5, 6]

    #100 moves
    puzzle = [6, 2, 7, 4, 5, 1, 0, 3, 8]
    path = []
    expanded = []
    unexpanded = []

    # Initialize first node
    current = Node(0, puzzle, 0)
    unexpanded.append(current)

    #Check if puzzle starts in goal state
    if checkGoalState(puzzle):
        return path

    start = time.time()
    # Expand state
    while unexpanded.__len__() > 0:
        # Check if goal state has been reached
        if checkGoalState(current.puzzle):
            break
        new_pos = getNewPositions(current.puzzle)
        # Remove node from unexpanded list
        unexpanded.remove(current)
        # Add current node to expanded list
        expanded.append(current)
        for i in range(1, new_pos.__len__()):
            if new_pos[i] >= 0:
                temp = moveSpace(current, new_pos[i], new_pos[0])
                current.children.append(temp)

                if next((x for x in expanded if x.puzzle == temp.puzzle), 1) == 1:
                    temp.cost = f(temp)
                    unexpanded.append(temp)


        # Set current to node with the lowest cost
        current = min(unexpanded, key=attrgetter("cost"))

    while current.parent != 0:
        path.append(current.puzzle.index(8))
        current = current.parent

    end = time.time()
    elapsed_time = (end - start) * 1000
    print("A* search elapsed time: " + elapsed_time.__str__() + " ms")
    print(path[::-1])
    return path[::-1]



'''
This function returns 1 if the puzzle passed in is equal to the goal state otherwise it returns zero
'''
def checkGoalState(puzzle):
    if puzzle == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        return 1
    else:
        return 0

'''
This function creates a copy of the node passed in and moves the empty space to the position provided, it also sets the
newly created node's parent to the node passed in. For the DFS and BFS algorithms I used the cost function to hold the
value of the space that the node moved the empty space to (from the original parent node) since the cost value was not
needed for these two algorithms
'''
def moveSpace(current_node, swap_pos, current_pos):
    #temp = copy.deepcopy(current_node)
    temp = Node(current_node, copy.deepcopy(current_node.puzzle), 0)
    temp.parent = current_node
    temp.children = []
    temp.puzzle[swap_pos], temp.puzzle[current_pos] = temp.puzzle[current_pos], temp.puzzle[swap_pos]
    temp.cost = swap_pos
    return temp

'''
This function checks if the given puzzle configuration exists in the set that is passed into the function via the check
variable.
'''
def checkForDuplicateState(puzzle, check):
    if puzzle in check:
        return 1
    return 0

'''
This function returns the current position of the empty space in the puzzle and the spaces that it can move to. If the
empty space is not in the center the next position values that are unused are set to -1
'''
def getNewPositions(puzzle):
    pos = 0
    # Initialize new position variables to -1 so the
    # function can know if the new pos_variable is needed
    new_pos_1 = -1
    new_pos_2 = -1
    new_pos_3 = -1
    new_pos_4 = -1
    for i in range(9):
        if puzzle[i] == 8:
            pos = i
            break

    if pos == 0:
        new_pos_1 = 1
        new_pos_2 = 3
    if pos == 1:
        new_pos_1 = 0
        new_pos_2 = 2
        new_pos_3 = 4
    if pos == 2:
        new_pos_1 = 1
        new_pos_2 = 5
    if pos == 3:
        new_pos_1 = 0
        new_pos_2 = 4
        new_pos_3 = 6
    if pos == 4:
        new_pos_1 = 1
        new_pos_2 = 3
        new_pos_3 = 5
        new_pos_4 = 7
    if pos == 5:
        new_pos_1 = 2
        new_pos_2 = 4
        new_pos_3 = 8
    if pos == 6:
        new_pos_1 = 3
        new_pos_2 = 7
    if pos == 7:
        new_pos_1 = 6
        new_pos_2 = 4
        new_pos_3 = 8
    if pos == 8:
        new_pos_1 = 7
        new_pos_2 = 5

    return pos, new_pos_1, new_pos_2, new_pos_3, new_pos_4

'''
This function runs the DFS algorithm, I put it in a helper function because I initially tried to run the recursive
version of the algorithm but because of the way that python handles its stack I kept getting a recursion error. I
switched to an iterative approach because the graph can get really deep, which is why I still had to increase the 
recursion limit because of the deepcopy used in the moveSpace function. Even with increasing the recursion limit
sometimes I will get a stack overflow error on this function, the majority of the time it works without error
but sometimes the depth of the graph is too much for even the iterative function to handle because of the limited
size of the call stack and because python does not use tail recursion.
'''
def dfsHelper(node):
    stack = []
    visited =[]
    sys.setrecursionlimit(0x100000)

    stack.append(node)

    while stack:
        current = stack.pop()
        #get neighbors
        visited.append(current.puzzle)
        new_pos = getNewPositions(current.puzzle)
        for i in range(1, new_pos.__len__()):
            if new_pos[i] >= 0:
                temp = moveSpace(current, new_pos[i], new_pos[0])
                #current.children.append(temp)
                if not checkForDuplicateState(temp.puzzle, visited) and not checkForDuplicateState(temp.puzzle, stack):
                    stack.append(temp)
                    visited.append(temp.puzzle)
                if checkGoalState(temp.puzzle):
                    return stack.pop()


''' This function calculates h(x) which in this problem is the number of 
    misplaced tiles in the current configuration of the puzzle'''
def h(puzzle):
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    diff_count = 0
    for i in range(0, puzzle.__len__()):
        if goal_state[i] != puzzle[i]:
            diff_count += 1
    return diff_count

''' This counts the number of hops taken to get to the given node which provides
    the g(x) value for this particular problem'''
def g(node):
    g_score = 0
    while node.parent != 0:
        g_score += 1
        node = node.parent
    return g_score

''' This function adds the h(x) and g(x) scores to get the f(x) score'''
def f(node):
    f_score = h(node.puzzle) + g(node)
    return f_score



