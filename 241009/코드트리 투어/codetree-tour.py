import heapq
from collections import defaultdict
import sys
input = sys.stdin.readline

INF = float('inf')

class Package:
    def __init__(self, id_, revenue, dest, profit):
        self.id_ = id_
        self.revenue = revenue
        self.dest = dest
        self.profit = profit
    
    def __lt__(self, other):  # min heap에서 self가 other보다 우선시되려면:
        if self.profit == other.profit:
            return self.id_ < other.id_ 
        return self.profit > other.profit 

def dijkstra(s, graph):
    n = len(graph) 
    dist = [INF] * n
    dist[s] = 0
    visited = [False] * n

    for _ in range(n):
        node = -1
        min_dist = INF
        for j in range(n):
            if not visited[j] and min_dist > dist[j]:
                min_dist = dist[j]
                node = j
        if node == -1:
            break
        visited[node] = True
        for j in range(n):
            if graph[node][j] != INF and dist[j] > dist[node] + graph[node][j]:
                dist[j] = dist[node] + graph[node][j]

    return dist

Q = int(input())

queue = []
id_exist = defaultdict(bool)
dep = 0
started = True

for _ in range(Q):
    order = list(map(int, input().split()))

    if order[0] == 100:
        n = order[1]
        m = order[2]
        graph = [[INF] * n for _ in range(n)]
        for i in range(n):
            graph[i][i] = 0
        for i in range(1, m + 1):
            u, v, w = order[3 * i], order[3 * i + 1], order[3 * i + 2]
            val = min(w, graph[u][v], graph[v][u])
            graph[u][v] = val
            graph[v][u] = val
    
    elif order[0] == 200:
        if started:
            dist = dijkstra(dep, graph) 
            started = False
        _, id_, revenue, dest = order
        if not id_exist[id_]:  # 중복된 ID 방지
            id_exist[id_] = True
            profit = revenue - dist[dest]
            package = Package(id_, revenue, dest, profit)
            heapq.heappush(queue, package)

    elif order[0] == 300:
        id_ = order[1]
        id_exist[id_] = False  # 해당 ID의 패키지를 비활성화
        # queue에는 패키지를 남겨두지만, 출력 시 체크하여 제외
        
    elif order[0] == 400:
        #print([(package.id_, package.profit) for package in queue])
        while queue:
            priority = queue[0]
            if priority.profit < 0:
                print(-1)
                break
            heapq.heappop(queue)
            id_ = priority.id_
            if id_exist[id_]:
                print(id_)
                break
        else: 
            print(-1)
    
    elif order[0] == 500:
        dep = order[1]
        dist = dijkstra(dep, graph) 

        for package in queue:
            if id_exist[package.id_]:  # 활성화된 패키지만 업데이트
                package.profit = package.revenue - dist[package.dest]
        heapq.heapify(queue)  # 다시 힙 정