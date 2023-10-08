import sys


class Node:
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self,node):
        self.frontier.append(node)

    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        node = self.frontier.pop()
        return node

class Solver:
    def __init__(self,filename):
        with open(filename) as file:
            content = file.read()

        if content.count("A") != 1:
            raise Exception("No start point")
        elif content.count("B") != 1:
            raise Exception("No end point")

        #height and width of maze
        lines = content.splitlines()
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
            
        self.walls = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                try:
                    if lines[h][w] == "A":
                        self.start = (h,w)
                        row.append(False)
                    elif lines[h][w] == "B":
                        self.end = (h,w)
                        row.append(False)
                    elif lines[h][w] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        
    def print_maze(self):
        solution = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("▮", end="")
                elif (i,j) == self.start:
                    print("A", end="")
                elif (i,j) == self.end:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()

    def neighbours(self,state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (row, col) in candidates:
            if 0 <= row < self.height and 0 <= col < self.width and not self.walls[row][col]:
                result.append((action, (row, col)))
        return result

    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        self.explored = set()

        while True:

            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.end:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


maze = Solver(sys.argv[1])
maze.print_maze()
maze.solve()
maze.print_maze()
print(maze.num_explored)


            
            

            
            

             

            
                
                
        
