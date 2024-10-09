Q = int(input())

orders = []
for _ in range(Q) :
    orders.append(list(map(int, input().split())))

dep = 0
packages = {}

def dijkstra(dep, world):
    dist = [float('inf')] * len(world)
    dist[dep] = 0
    visited = [False] * len(world)

    for _ in range(len(world)):
        min_dist = float('inf')
        min_node = -1
        for i in range(len(world)):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                min_node = i
        if min_node == -1:
            break
        visited[min_node] = True
        for nei, cost in world[min_node]:
            if dist[min_node] + cost < dist[nei]:
                dist[nei] = dist[min_node] + cost

    return dist
    
for order in orders :
    #print(order)
    if order[0] == 100 :
        n, m = order[1], order[2]
        world = {i:set() for i in range(n)}
        idx = 3
        for i in range(m) :
            v, u, w = order[idx], order[idx+1], order[idx+2]
            world[v].add((u, w))
            world[u].add((v, w))
            idx += 3
        costs = dijkstra(dep, world)

    if order[0] == 200 :
        id_, revenue, dest = order[1], order[2], order[3]
        packages[id_] = (revenue, dest)

    if order[0] == 300 :
        id_ = order[1]
        if id_ in packages :
            del packages[id_]

    if order[0] == 400 :
        max_income = -1
        that_id = 0
        for id_, value in packages.items() :
            revenue, dest = value
            if costs[dest] == float('inf') :
                continue
            if revenue - costs[dest] > max_income :
                max_income = revenue - costs[dest]
                that_id = id_
            elif revenue - costs[dest] == max_income :
                if that_id > id_ :
                    that_id = id_

        if max_income > -1 :
            print(that_id)
            del packages[that_id]
        else :
            print(-1)

    if order[0] == 500 :
        s = order[1]
        dep = s
        costs = dijkstra(dep, world)