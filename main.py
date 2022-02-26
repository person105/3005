import json
import time
from math import radians, cos, sin, asin, sqrt
import enum


"""  
    Initialization

 """

queue = []
visited = []

viableNodes = []
path = []

algorithms = ["ucs", "aStar"]
run = 0

f = open('coord.json')
coord = json.load(f)

f = open('cost.json')
cost = json.load(f)

f = open('dist.json')
dist = json.load(f)

f = open('g.json')
G = json.load(f)


""" 
    Helper methods

 """

def getAdjList(n):

    list = []

    try:
        list = G[str(n)]
    except:
        print("Unable to get adjacent nodes.")
    
    return list

def getCoord(n):

    c = []

    try:
        c = coord[str(n)]
    except:
        print("Unable to get coordinates of node.")
    
    return c

def getDist(v,w):

    d = 0

    try:
        d = (dist["{},{}".format(v,w)])
    except:

        try:
            d = (dist["{},{}".format(w,v)]) 
        except:
            print("Unable to get distance between nodes.")
        

    return d

def getCost(v,w):
    c = 0

    try:
        c = (cost["{},{}".format(v,w)])
    except:

        try:
            c = (cost["{},{}".format(w,v)])
        except:
            print("Unable to get cost between nodes.")


    return c

def sort(queue, mode):

    if(mode == "aStar"):
        key = 'total'

    elif(mode == "ucs"):
        key = 'cost'
        
    queue.sort(key=lambda q: q.get(key))
    return queue


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def getEuclidean(v,w):
    v = getCoord(v)
    w = getCoord(w)

    return (((v[0] - w[0])**2 + (v[1] - w[1])**2)**0.5)

def getHaversine(v,w):

    """ 
        This method was adapted from stackoverflow
        https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
        answered Jul 30, 2017 at 3:00
        by: Clay

    """

    #TODO: Fix bug math err when Start: 50 End: 1 

    R = 6372.8 #Approx of Earth's radius (3959.87433 miles/6372.8 km)

    v = getCoord(v)
    w = getCoord(w)
    c = 0

    try:
       
        diffLat = radians((w[0]) - v[0])
        diffLon = radians(w[1] - v[1])
        lat1 = radians(v[0])
        lat2 = radians(w[0])

        a = sin(diffLat/2)**2 + cos(lat1)*cos(lat2)*sin(diffLon/2)**2
        c = 2*asin(sqrt(a))

    except:
        print("Unable to calculate Haversine Distance.")

    return R * c
 

def findPath(start, end):

    #TODO: Fix bug 'NoneType' object is not subscriptable
    #Probable cause tracePath not in correct order

    tracePath = build_dict(viableNodes, key="current")
    currentNode = end
    p = []

    print(tracePath)

    while (currentNode != start):
        node = tracePath.get(currentNode)
        p.append(node)
        currentNode = node['prev'] 

    p.reverse()
    return p


def getStrPath(path):

    route = "S"
    for p in path:
        route += ("->{}".format(p['current']))

    return route


def getPathDist(path):

    d = 0
    for p in path:
        d += p['dist']

    return d


""" 
    Main Methods

 """

def main():

    option = int(input("Please select option or enter '-1' to terminate program:        \
                        \n1) Task 1: Relaxed ver (TBC)                                  \
                        \n2) Task 2: UCS                                                \
                        \n3) Task 3: A* with Haversine Distance                         \
                        \n"))                                                   


    if (option == 1):
        mode = ""

    if (option == 2):
        mode = "ucs"
        print("**Task 2: UCS selected**")
    
    elif (option == 3):
        mode = "aStar"
        print("**Task 3: A* with Haversine Distance selected**")

    else:
        if (option != -1):
            print("Please enter option: '1', '2', or '3'\n")

    if (option > 0 and option < 4):
        if any(algo == mode for algo in algorithms):

            start = input("Please enter the start node: ")
            end = input("Please enter the end node: ")

            if (int(start) > 0 and int(end) < 264347):
                print("Processing...\n")

                stime = time.time()
                search(start, end, mode)
                etime = time.time()

                print("Total time elapsed: {}\n".format(etime-stime))

            else:
                print("\nPlease enter nodes between 1 and 264346.\n")


    return option

def search(start, end, mode):

    total = 0

    if (mode == 'aStar'):
        total = getHaversine(start, end)

    if (start == end):
        print("Start node and end node should not be the same.")
        return

    queue.append({
            "current": start,
            "cost": 0,
            "dist": 0,
            "total": total,
            "prev": 0
    }) 
    
    nextNode = processAdj(queue[0], end, mode)

    while (not any (node['current'] == end for node in visited)):
        
        nextNode = processAdj(nextNode, end, mode)


    path = findPath(start, end)

    #Print results
    strPath = getStrPath(path)
    pathCost = path[-1]['cost']
    pathDist = getPathDist(path)

    print(strPath, 
            "\nTotal path cost: {}".format(pathCost), 
                "\nTotal path distance: {}".format(pathDist))

def ucs(start, end, mode):
    
    if (start == end):
        print("Start node and end node should not be the same.")
        return

    queue.append({
            "current": start,
            "cost": 0,
            "dist": 0,
            "prev": 0
    }) 
    
    nextNode = processAdj(queue[0], end, mode)

    while (not any (node['current'] == end for node in visited)):
        nextNode = processAdj(nextNode, end, mode)

    path = findPath(start, end)

    #Print results
    strPath = getStrPath(path)
    pathCost = path[-1]['cost']
    pathDist = getPathDist(path)

    print(strPath, 
            "\nTotal path cost: {}".format(pathCost), 
                "\nTotal path distance: {}".format(pathDist))


def processAdj(currentNode, end, mode):

    adj = getAdjList(currentNode['current'])
    total = 0
    
    if (len(adj) > 1):
        for nextNode in adj:

            c = getCost(currentNode['current'], nextNode) + currentNode['cost']
            
            if (mode == "aStar"):
                total = c + getHaversine(nextNode, end)


            nextNodeInfo = ({
                    "current": nextNode,
                    "cost": c,
                    "dist": getDist(currentNode['current'],nextNode),
                    "total": total,
                    "prev": currentNode['current']
                }) 

            if not any (node['current'] == nextNode for node in queue) and not any(node['current'] == nextNode for node in visited):
                queue.append(nextNodeInfo)

            #TODO: else compare costs
            
                

        visited.append(queue[0]) 
        viableNodes.append(queue[0])


    elif (len(adj) == 1):
        
        #Deadend
        nextNode = adj[0]
        c = getCost(currentNode['current'], nextNode) + currentNode['cost']
        if (mode == "aStar"):
            total = c + getHaversine(nextNode, end)


        visited.append({
            "current": nextNode,
            "cost": c,
            "dist": getDist(currentNode['current'],nextNode),
            "total": total,
            "prev": currentNode['current']
        })

    queue.pop(0)
    sort(queue, mode)

    return queue[0]



""" 
    Main Program

 """
 
# Step 1: Expand adj nodes from start
# Step 2: Rank nodes by cost + euclidean distance
# Step 3: Expand adj nodes of the shortest path
# Step 3.1: If expanded node is already processed, overwrite with path that costs the least
# Step 4: Check if start and end queue has processed the same node
# Step 4.1: If both queues processed same node, proceed to generate path and end loop
# Step 4.2: Else, return to step 1

if __name__ == "__main__":
    
    while (run != -1):
        run = main()

    # Closing file
    f.close()


