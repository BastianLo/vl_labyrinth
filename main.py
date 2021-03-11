import sys
import time

class node:
    def __init__(self, character, last_node, x, y):
        self.character = character
        self.last_node = last_node
        self.x = x
        self.y = y


def file_to_array_converter(filename):
    with open(filename) as f:
            lines = f.readlines()
    labyrinth = []
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n","")
        labyrinth.append([])
        for j in range(len(lines[i])):
            labyrinth[i].append(lines[i][j])
            if lines[i][j] == "S":
                start = node('S',None, j, i)
    try:
        return labyrinth, start
    except:
        sys.exit("No start found")

class maze:
    def __init__(self, char_array,start_node):
        self.char_array = char_array
        self.start_node = start_node

    def get_neighbors(self, base_node):
        neighbors = []
        x = base_node.x
        y = base_node.y
        
        if self.char_array[y-1][x] == "X":
            neighbors.append(node('X',base_node,x,y-1))
            return neighbors
        if self.char_array[y+1][x] == "X":
            neighbors.append(node('X',base_node,x,y+1))
            return neighbors
        if self.char_array[y][x+1] == "X":
            neighbors.append(node('X',base_node,x+1,y))
            return neighbors
        if self.char_array[y][x-1] == "X":
            neighbors.append(node('X',base_node,x-1,y))
            return neighbors

        if self.char_array[y-1][x] == " ":
            self.char_array[y-1][x] = "."
            neighbors.append(node(' ',base_node,x,y-1))
        if self.char_array[y+1][x] == " ":
            self.char_array[y+1][x] = "."
            neighbors.append(node(' ',base_node,x,y+1))
        if self.char_array[y][x+1] == " ":
            self.char_array[y][x+1] = "."
            neighbors.append(node(' ',base_node,x+1,y))
        if self.char_array[y][x-1] == " ":
            self.char_array[y][x-1] = "."
            neighbors.append(node(' ',base_node,x-1,y))
        
        return neighbors

    def draw_path_to_exit(self, exit_node):
        self.recursive_path_drawer(exit_node)
        
        
        for line in self.char_array:
            for c in line:
                print(c, end="")
            print("")
    
    def recursive_path_drawer(self, node):
        if node.character == 'S':
            return
        elif node.character != 'X':
            self.char_array[node.y][node.x] = '@'
            self.recursive_path_drawer(node.last_node)
        else:
            self.recursive_path_drawer(node.last_node)     

    def find_exit(self):
        open_nodes = [start_node]
        visited_nodes = []

        counter = 0
        while True:
            for node in open_nodes:
                open_nodes = open_nodes + self.get_neighbors(node)

                #check if exit has been found
                for n in open_nodes:
                    if n.character == 'X':
                        return n

                visited_nodes.append(node)
                open_nodes.remove(node)

            counter+=1
            if counter > 500:
                print("a problem occurred")
                return
    
if __name__ == "__main__":
    #'.' = Punkt wurde als möglicher Weg untersucht
    #'@' = Weg zum Ausgang
    start_time = time.time()

    maze_array, start_node = file_to_array_converter("labyrinth.map")
    _maze = maze(maze_array,start_node)
    _maze.draw_path_to_exit(_maze.find_exit())
    
    print("Completed in:",str(round((time.time()-start_time)*1000,3))+"ms")