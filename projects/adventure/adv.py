from room import Room
from player import Player
from world import World
from util import Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = r"C:\Users\joelc\desktop\lambda-cs\graphs\projects\adventure\maps\test_line.txt"
# map_file = "maps/test_cross.txt"
#map_file = r"C:\Users\joelc\desktop\lambda-cs\graphs\projects\adventure\maps\test_loop.txt"
#map_file = r"C:\Users\joelc\desktop\lambda-cs\graphs\projects\adventure\maps\test_loop_fork.txt"
#map_file = r"C:\Users\joelc\desktop\lambda-cs\graphs\projects\adventure\maps\test_cross.txt"
map_file = r"C:\Users\joelc\desktop\lambda-cs\graphs\projects\adventure\maps\main_maze.txt"
# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
print(len(room_graph))
# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_graph = {}


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
def bfs(start , grph = traversal_graph):
    q = Queue()
    vstd = set()
    q.enqueue([start])
    q2 = Queue()

    while q.size() > 0:
       
        current = q.dequeue()
        last_node = current[-1] 
        #print(current)
        for neighbor in grph[last_node]:
            #print(neighbor, 'neighbor')
            if grph[last_node][neighbor] not in vstd:
                #print(grph[last_node][neighbor], 'swee')
                new_path = current + [grph[last_node][neighbor]]
                if grph[last_node][neighbor] == '?':
                    return current
                q.enqueue(new_path)
        vstd.add(last_node)
def cnvert(arr, grph = traversal_graph):
    r = []
    for i in range(0,len(arr)-1):
        trgt = arr[i+1]
        for neighbor in grph[arr[i]]:
            if grph[arr[i]][neighbor] == trgt:
                r.append(neighbor)
             
    return [r,arr[-1]]
opposite = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}
last_move = None
previous_room = None 
h = 0
for i in range(0,len(room_graph)*2):
    if h > len(room_graph) * 2:
        break
    room = player.current_room
    print(room.id)
    #enter current room into the traversal graph if it isn't in there
    if room.id not in traversal_graph:
        #print(len(traversal_graph), len(room_graph))
        if len(traversal_graph) == (len(room_graph) -1):
            break
        traversal_graph[room.id] = {}
        exits = room.get_exits()
        
        for e in exits:
            traversal_graph[room.id][e] = "?"
        if last_move is not None:
            traversal_graph[previous_room.id][last_move] = room.id
            traversal_graph[room.id][opposite[last_move]] = previous_room.id
    
    #fill in the connections between this room and the last if missing

    #print(traversal_graph[room.id][opposite[last_move]])
    elif traversal_graph[room.id][opposite[last_move]] == '?':
        traversal_graph[previous_room.id][last_move] = room.id
        traversal_graph[room.id][opposite[last_move]] = previous_room.id

    if len(traversal_graph) == (len(room_graph)):
        break
    #check for unexplored paths
    for k in traversal_graph[room.id].keys():
        if traversal_graph[room.id][k] == "?":
            previous_room = room
            last_move = k
            player.travel(k)
            print("moving", k)
            traversal_path.append(k)
            break

    #if an unexplored branch was found
    #skip the dead end code
    if room == previous_room:
        continue

    #if the above code didn't find anything we are at a dead end
    # perform a bfs to find closest node with an unexplored path
    else:
        bfs_result = cnvert(bfs(room.id))
        for m in bfs_result[0]:
            print('backtracking')
            traversal_path.append(m)
            player.travel(m)
            print('moving', m)
        last_move = bfs_result[0][-1]

test = {0: {'n': 1, 's': '?', 'w': '?', 'e': '?'}, 1: {'n': 2, 's': 0}, 2: {'s': 1}}





#print(x,convert(x))
#print(convert(bfs(2, test)))
        
player.current_room = world.starting_room

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
"""
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""




#__________________psuedo code_____________________
"""

Enter with a starting room

check to see which directions you can move
    if there is only 1 and it's unvisited,
        move in that direction and repeat
    if there are multiple unexplored directions, pick one and move there

to handle backtracking:
easier method:
    if you hit a dead end, use a bfs to find the shortest path to an unexplored room
cooler method:
{probably not feasable} 
    outer stack is just the call stack
    if you hit a crossroads of multiple unexplored paths
    pick a path and move down it
    start a stack with opposite moves in it
    if you hit another crossroads start another stack and repeat
    if you hit a dead end, add the top stack to the commands and move in an available direction

"""