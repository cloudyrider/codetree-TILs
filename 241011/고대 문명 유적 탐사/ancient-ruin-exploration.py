from collections import deque
import heapq
from copy import deepcopy
import sys

class Candidate:
    def __init__(self, x, y, graph, rotation):
        self.x = x
        self.y = y
        self.graph = deepcopy(graph)  
        self.rotation = rotation
        self.value = 0
        self.replace_coor = set()

    def __lt__(self, other):
        if self.value != other.value:
            return self.value > other.value
        if self.rotation != other.rotation:
            return self.rotation < other.rotation
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def rotate(self):
        if self.x is None or self.y is None or self.rotation is None :
            self.value = self._get_value()
            return 
        
        rotated_matrix = self._rotate(self.rotation)
        for i in range(3):
            for j in range(3):
                self.graph[self.x + i][self.y + j] = rotated_matrix[i][j]
        self.value = self._get_value()

    def _rotate(self, angle):
        matrix = [row[self.y:self.y+3] for row in self.graph[self.x:self.x+3]]
        if angle == 90:
            return [list(row[::-1]) for row in zip(*matrix)]
        elif angle == 180:
            return [row[::-1] for row in matrix[::-1]]
        elif angle == 270:
            return list(row for row in zip(*matrix))[::-1]
        return matrix

    def _get_value(self):
        value = 0
        for i in range(1, 8):
            value += self._bfs(i)
        return value

    def _bfs(self, target):
        seen = [[False] * 5 for _ in range(5)]  # 5x5 전체를 탐색
        dx = [0, 0, -1, 1]
        dy = [1, -1, 0, 0]
        valuable = 0

        for x in range(5):
            for y in range(5):
                if self.graph[x][y] == target and not seen[x][y]:
                    queue = deque([(x, y)])
                    seen[x][y] = True
                    group_size = 1  

                    while queue:
                        cx, cy = queue.popleft()
                        for d in range(4):
                            nx, ny = cx + dx[d], cy + dy[d]
                            if 0 <= nx < 5 and 0 <= ny < 5 and self.graph[nx][ny] == target and not seen[nx][ny]:
                                seen[nx][ny] = True
                                queue.append((nx, ny))
                                group_size += 1
                                self.replace_coor.add((cy, -cx))  
                                self.replace_coor.add((ny, -nx))  

                    if group_size > 2:
                        valuable += group_size 

        return valuable


def solve():
    K, M = map(int, input().split())
    graph = [list(map(int, input().split())) for _ in range(5)]
    wall_numbers = deque(map(int, input().split()))

    for _ in range(K):
        candidates = []

        # 90도, 180도, 270도 회전 후보자 생성
        for x in range(3):
            for y in range(3):
                for rotation in [90, 180, 270]:
                    candidate = Candidate(x, y, graph, rotation)
                    candidate.rotate()
                    heapq.heappush(candidates, candidate)
                    
        nominee = heapq.heappop(candidates)
        graph = nominee.graph
        value = nominee.value
        replace_coor = sorted(nominee.replace_coor)

        if value == 0:  # 종료 조건
            break

        for ey, ex in replace_coor:
            graph[-ex][ey] = wall_numbers.popleft()

        while True:  # 연속 제거와 채우기 처리
            new_candidate = Candidate(None, None, graph, None)
            new_candidate.rotate()
            replace_coor = sorted(new_candidate.replace_coor)
            if not replace_coor:
                break
            for ey, ex in replace_coor:
                graph[-ex][ey] = wall_numbers.popleft()
            value += new_candidate.value
        print(value)

if __name__ == "__main__":
    solve()