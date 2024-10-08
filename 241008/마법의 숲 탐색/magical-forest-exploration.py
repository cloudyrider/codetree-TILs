R, C, K = map(int, input().split())

spirits = list()
for _ in range(K) :
    spirits.append(list(map(int, input().split())))

world = [[0]*(C) for _ in range(R+3)]
settled_spirits = dict()

sum_answer = 0
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
        #world reset
        world = [[0]*(C) for _ in range(R+3)]
        settled_spirits = dict()
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
    candidates = [spirit_r+1]

    if (spirit_r+3, spirit_c) in settled_spirits and direction == 2 :
        candidates.append(settled_spirits[(spirit_r+3, spirit_c)])

    if (spirit_r+2, spirit_c+1) in settled_spirits and (direction == 1 or direction == 2) :
        candidates.append(settled_spirits[(spirit_r+2, spirit_c+1)])
    if (spirit_r+1, spirit_c+2) in settled_spirits and (direction == 1 or direction == 2) :
        candidates.append(settled_spirits[(spirit_r+1, spirit_c+2)])
    if (spirit_r, spirit_c+3) in settled_spirits and direction == 1 :
        candidates.append(settled_spirits[(spirit_r, spirit_c+3)])

    if (spirit_r+2, spirit_c-1) in settled_spirits and (direction == 3 or direction == 2) :
        candidates.append(settled_spirits[(spirit_r+2, spirit_c-1)])
    if (spirit_r+1, spirit_c-2) in settled_spirits and (direction == 3 or direction == 2) :
        candidates.append(settled_spirits[(spirit_r+1, spirit_c-2)])
    if (spirit_r, spirit_c-3) in settled_spirits and direction == 3 :
        candidates.append(settled_spirits[(spirit_r, spirit_c-3)])

    answer = max(candidates)
    settled_spirits[(spirit_r, spirit_c)] = answer
    #print(settled_spirits)
    sum_answer += answer-2
    #print(answer-2)

print(sum_answer)