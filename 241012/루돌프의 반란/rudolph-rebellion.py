import sys
import heapq

input = sys.stdin.readline

class Santa:
    def __init__(self, number, x, y, N):
        self.number = number
        self.x = x
        self.y = y
        self.score = 0
        self.active = True
        self.stuned = 0
        self.distance_to_rudolf = None
        self.N = N

    def __lt__(self, other):
        if self.distance_to_rudolf != other.distance_to_rudolf:
            return self.distance_to_rudolf < other.distance_to_rudolf
        if self.x != other.x:
            return self.x > other.x
        return self.y > other.y

    def move(self, rudolf_x, rudolf_y, santa_cords):
        if self.stuned or not self.active:
            return None

        dx = [-1, 0, 1, 0]  # 상, 우, 하, 좌
        dy = [0, 1, 0, -1]

        min_distance = get_distance(self.x, self.y, rudolf_x, rudolf_y)
        best_direction = None

        for d in range(4):
            nx = self.x + dx[d]
            ny = self.y + dy[d]

            if 0 <= nx < self.N and 0 <= ny < self.N and (nx, ny) not in santa_cords:
                n_distance = get_distance(nx, ny, rudolf_x, rudolf_y)
                if n_distance < min_distance:
                    min_distance = n_distance
                    best_direction = d

        if best_direction is not None:
            # 현재 위치 삭제
            del santa_cords[(self.x, self.y)]
            # 위치 업데이트
            self.x += dx[best_direction]
            self.y += dy[best_direction]
            # 새로운 위치 추가
            santa_cords[(self.x, self.y)] = self.number
            self.distance_to_rudolf = min_distance
            return best_direction
        else:
            return None

    def struggle(self, typ, move_direction, santa_cords, santa_dict):
        dx = [-1, 0, 1, 0, -1, -1, 1, 1]
        dy = [0, 1, 0, -1, -1, 1, -1, 1]

        self.score += typ
        self.stuned = 2

        push_distance = typ
        nx = self.x + dx[move_direction] * push_distance
        ny = self.y + dy[move_direction] * push_distance

        # 현재 위치 삭제
        del santa_cords[(self.x, self.y)]

        if not (0 <= nx < self.N and 0 <= ny < self.N):
            self.active = False
            return

        # 착지 위치에 다른 산타가 있는 경우 상호작용 발생
        if (nx, ny) in santa_cords:
            other_santa = santa_dict[santa_cords[(nx, ny)]]
            other_santa._interaction(move_direction, santa_cords, santa_dict)

        # 새로운 위치 추가
        self.x = nx
        self.y = ny
        santa_cords[(self.x, self.y)] = self.number

    def _interaction(self, move_direction, santa_cords, santa_dict):
        dx = [-1, 0, 1, 0, -1, -1, 1, 1]
        dy = [0, 1, 0, -1, -1, 1, -1, 1]

        nx = self.x + dx[move_direction]
        ny = self.y + dy[move_direction]

        # 현재 위치 삭제
        del santa_cords[(self.x, self.y)]

        if not (0 <= nx < self.N and 0 <= ny < self.N):
            self.active = False
            return

        # 다음 산타가 있는 경우 재귀적으로 처리
        if (nx, ny) in santa_cords:
            other_santa = santa_dict[santa_cords[(nx, ny)]]
            other_santa._interaction(move_direction, santa_cords, santa_dict)

        # 새로운 위치 추가
        self.x = nx
        self.y = ny
        santa_cords[(self.x, self.y)] = self.number

def get_distance(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def solve():
    N, M, P, C, D = map(int, input().split())
    rx, ry = map(int, input().split())
    rx -= 1
    ry -= 1
    santa_dict = {}
    santa_cords = {}
    for _ in range(P):
        i, x, y = map(int, input().split())
        santa_dict[i] = Santa(i, x - 1, y - 1, N)
        santa_cords[(x - 1, y - 1)] = i

    for turn in range(M):
        # 산타들의 기절 상태 업데이트
        for santa in santa_dict.values():
            if santa.stuned > 0:
                santa.stuned -= 1

        # 루돌프의 이동
        alive_santas = [santa for santa in santa_dict.values() if santa.active]
        if not alive_santas:
            break

        for santa in alive_santas:
            santa.distance_to_rudolf = get_distance(rx, ry, santa.x, santa.y)

        closest_santa = min(alive_santas)

        dx_r = [-1, 0, 1, 0, -1, -1, 1, 1]
        dy_r = [0, 1, 0, -1, -1, 1, -1, 1]

        min_distance = float('inf')
        best_direction = None

        for d in range(8):
            nx = rx + dx_r[d]
            ny = ry + dy_r[d]
            if 0 <= nx < N and 0 <= ny < N:
                n_distance = get_distance(nx, ny, closest_santa.x, closest_santa.y)
                if n_distance < min_distance:
                    min_distance = n_distance
                    best_direction = d

        if best_direction is not None:
            rx += dx_r[best_direction]
            ry += dy_r[best_direction]

        # 루돌프와 산타의 충돌 처리
        if (rx, ry) in santa_cords:
            collided_santa = santa_dict[santa_cords[(rx, ry)]]
            collided_santa.struggle(C, best_direction, santa_cords, santa_dict)

        # 산타들의 이동 및 충돌 처리
        for i in range(1, P + 1):
            santa = santa_dict[i]
            if not santa.active or santa.stuned > 0:
                continue

            direction = santa.move(rx, ry, santa_cords)
            if santa.x == rx and santa.y == ry:
                santa.struggle(D, (direction + 2) % 4, santa_cords, santa_dict)
        #print(rx, ry)
        #print(santa_cords)

        # 살아있는 산타들에게 점수 추가
        for santa in santa_dict.values():
            if santa.active:
                santa.score += 1

        # 모든 산타가 탈락하면 게임 종료
        if not any(santa.active for santa in santa_dict.values()):
            break

    # 최종 점수 출력
    print(' '.join(str(santa_dict[i].score) for i in range(1, P + 1)))

if __name__ == "__main__":
    solve()