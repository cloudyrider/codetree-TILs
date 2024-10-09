#33번 오류


#정답 : 21671
#내 답 : 21697


R, C, K = map(int, input().split())

spirits = list()
for _ in range(K) :
    spirits.append(list(map(int, input().split())))

world = [[0]*(C) for _ in range(R+3)] #골렘 크기 3을 감안하여 숲 지도 행을 3 늘림
directions = dict()

answer = 0
#정령이 골렘을 타고 내려옴
for c, d in spirits :
    spirit_r = 2
    spirit_c = c-1
    direction = d

    while True :
        down_available = (spirit_r < R+1 and 0 < spirit_c < C-1 and
                        world[spirit_r+2][spirit_c] == 0 and 
                        world[spirit_r+1][spirit_c-1] == 0 and 
                        world[spirit_r+1][spirit_c+1] == 0)

        if down_available : 
            spirit_r += 1
            continue

        left_available = (spirit_r < R+1 and 1 < spirit_c < C-1 and
                        world[spirit_r-1][spirit_c-1] == 0 and 
                        world[spirit_r+1][spirit_c-1] == 0 and 
                        world[spirit_r+2][spirit_c-1] == 0 and
                        world[spirit_r][spirit_c-2] == 0 and
                        world[spirit_r+1][spirit_c-2] == 0)

        if left_available :
            spirit_r += 1
            spirit_c -= 1
            direction -= 1
            direction %= 4
            continue

        right_available = (spirit_r < R+1 and 0 < spirit_c < C-2 and
                        world[spirit_r-1][spirit_c+1] == 0 and 
                        world[spirit_r+1][spirit_c+1] == 0 and 
                        world[spirit_r+2][spirit_c+1] == 0 and
                        world[spirit_r][spirit_c+2] == 0 and
                        world[spirit_r+1][spirit_c+2] == 0)

        if right_available :
            spirit_r += 1
            spirit_c += 1
            direction += 1
            direction %= 4
            continue

        break

    #print(spirit_r-2, spirit_c+1, direction)

    if spirit_r < 4 :
        #골렘이 숲 내 안착 실패 시 숲 초기화
        world = [[0]*(C) for _ in range(R+3)]
        directions = dict()
        
        continue

    world[spirit_r][spirit_c] = 1
    world[spirit_r+1][spirit_c] = 1
    world[spirit_r-1][spirit_c] = 1
    world[spirit_r][spirit_c+1] = 1
    world[spirit_r][spirit_c-1] = 1

    """
       0
       |
  3 ___|___ 1
       |
       2
    """

    directions[(spirit_r, spirit_c)] = direction
    queue = [(spirit_r, spirit_c, direction)]
    max_r = 0
    seen = set()
    seen.add((spirit_r, spirit_c))

    while queue :
        #print(queue)
        r, c, d = queue.pop(0)
        max_r = max(max_r, r+1)

        if d == 0 :
            for nr, nc in [(r-3, c), (r-2, c+1), (r-2, c-1), (r-1, c-2), (r-1, c+2)] :
                if (nr, nc) in directions and (nr, nc) not in seen :
                    queue.append((nr, nc, directions[(nr, nc)]))
                    seen.add((nr, nc))

        elif d == 1 :
            for nr, nc in [(r-2, c+1), (r-1, c+2), (r, c+3), (r+1, c+2), (r+2, c+1)] :
                if (nr, nc) in directions and (nr, nc) not in seen :
                    queue.append((nr, nc, directions[(nr, nc)]))
                    seen.add((nr, nc))

        elif d == 2 :
            for nr, nc in [(r+3, c), (r+2, c+1), (r+2, c-1), (r+1, c-2), (r+1, c+2)] :
                if (nr, nc) in directions and (nr, nc) not in seen :
                    queue.append((nr, nc, directions[(nr, nc)]))
                    seen.add((nr, nc))

        elif d == 4 :
            for nr, nc in [(r-2, c-1), (r-1, c-2), (r, c-3), (r+1, c-2), (r+2, c-1)] :
                if (nr, nc) in directions and (nr, nc) not in seen :
                    queue.append((nr, nc, directions[(nr, nc)]))
                    seen.add((nr, nc))

    answer += max_r-2
    #print(max_r)

print(answer)