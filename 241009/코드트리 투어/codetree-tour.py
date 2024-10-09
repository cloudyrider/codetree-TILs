Q = int(input())

orders = []
for _ in range(Q) :
    orders.append(list(map(int, input().split())))

def dijkstra(deps, dests, world) :
    costs = {}

    for dep in deps :
        dests_ = dests
        temp_costs = [float('inf')] * len(world)
        temp_costs[dep] = 0
        visited = [False] * len(world)

        for _ in range(len(world)) :
            min_cost = float('inf')
            which_min = -1

            for i in range(len(world)) :
                if not visited[i] :
                    if temp_costs[i] < min_cost :
                        min_cost = temp_costs[i]
                        which_min = i
            
            if which_min == -1 :
                break
    
            visited[which_min] = True
            if which_min in dests_ :
                dests_.remove(which_min)

            if not dests_ :
                break
            
            for nei, cost in world[which_min]:
                if nei != which_min : 
                    if temp_costs[which_min] + cost < temp_costs[nei]:
                        temp_costs[nei] = temp_costs[which_min] + cost

        costs[dep] = temp_costs

    return costs

dests = []

for order in orders :
    if order[0] == 100 :
        n, m = order[1], order[2]
        world = {i:set() for i in range(n)}
        idx = 3
        for i in range(m) :
            v, u, w = order[idx], order[idx+1], order[idx+2]
            world[v].add((u, w))
            world[u].add((v, w))
            idx += 3
        break

deps = set()
deps.add(0)
dests = set()

for order in orders :
    if order[0] == 200 :
        dests.add(order[3])

    elif order[0] == 500 :
        deps.add(order[1])

costs = dijkstra(deps, dests, world)
dep = 0
packages = {}

for order in orders :

    if order[0] == 200 :
        id_, revenue, dest = order[1], order[2], order[3]
        packages[id_] = (revenue, dest)

    if order[0] == 300 :
        id_ = order[1]
        if id_ in packages :
            del packages[id_]

    if order[0] == 400 :
        costs_from_dep_to = costs[dep]
        max_income = -1
        max_id = -1

        for id_, value in packages.items() :
            revenue, dest = value
            income = revenue - costs_from_dep_to[dest]
            if income > max_income :
                max_income = income
                max_id = id_
            elif income == max_income :
                max_id = min(id_, max_id)
         
        if max_income > -1 :
            print(max_id)
            del packages[max_id]
        else :
            print(-1)

    if order[0] == 500 :
        dep = order[1]