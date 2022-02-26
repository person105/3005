import json
import time

"""  
    Initialization

 """

queue = []
# end_queue = []

visited = []
# end_visited = []

viableNodes = []
path = []


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

def sort(queue):
    queue.sort(key=lambda q: q.get('total'))
    return queue


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def getEuclidean(v,w):
    v = getCoord(v)
    w = getCoord(w)

    return (((v[0] - w[0])**2 + (v[1] - w[1])**2)**0.5) 

def findPath(start, end):

    tracePath = build_dict(viableNodes, key="current")
    currentNode = end
    p = []

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

def aStar(start, end):

    if (start == end):
        print("Start node and end node should not be the same.")
        return

    queue.append({
            "current": start,
            "cost": 0,
            "dist": 0,
            "total": getEuclidean(start, end),
            "prev": 0
    }) 
    
    nextNode = processAdj(queue[0])

    while (not any (node['current'] == end for node in visited)):
        
        nextNode = processAdj(nextNode)


    path = findPath(start, visited[-1]['current'])

    #Print results
    strPath = getStrPath(path)
    pathCost = path[-1]['cost']
    pathDist = getPathDist(path)

    print(strPath, 
            "\nTotal path cost: {}".format(pathCost), 
                "\nTotal path distance: {}".format(pathDist))


def processAdj(currentNode):

    adj = getAdjList(currentNode['current'])
    
    if (len(adj) > 1):
        for nextNode in adj:

            c = getCost(currentNode['current'], nextNode) + currentNode['cost']
            total = c + getEuclidean(nextNode, end)

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
        total = c + getEuclidean(nextNode, end)

        visited.append({
            "current": nextNode,
            "cost": c,
            "dist": getDist(currentNode['current'],nextNode),
            "total": total,
            "prev": currentNode['current']
        })

    queue.pop(0)
    sort(queue)

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

    start = input("Please enter the start node: ")
    end = input("Please enter the end node: ")
    # budget = input("Please enter energy budget: ")

    stime = time.time()

    aStar(start, end)

    etime = time.time()

    print("Total time elapsed: {}".format(etime-stime))


    # Closing file
    f.close()


