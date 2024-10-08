R, C, K = map(int, input().split())

spirits = list()
for _ in range(K) :
    spirits.append(list(map(int, input().split())))

world = [[0]*(C) for _ in range(R+3)]
connected = dict()

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
        connected = dict()
        
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

    connected[(spirit_r, spirit_c)] = [{(spirit_r, spirit_c)}, spirit_r+1]
    max_val = spirit_r+1
    connected_keys = {(spirit_r, spirit_c)}

    for key, value in connected.items() :
        if (spirit_r+3, spirit_c) in value[0] and direction == 2 :
            connected_keys.add(key)
            max_val = max(max_val, value[1])
        if (spirit_r+2, spirit_c+1) in value[0] and (direction == 1 or direction == 2) :
            connected_keys.add(key)
            max_val = max(max_val, value[1])
        if (spirit_r+1, spirit_c+2) in value[0] and (direction == 1 or direction == 2) :
            connected_keys.add(key)
            max_val = max(max_val, value[1])
        if (spirit_r, spirit_c+3) in value[0] and direction == 1 :
            connected_keys.add(key)
            max_val = max(max_val, value[1])
        if (spirit_r+2, spirit_c-1) in value[0] and (direction == 3 or direction == 2) :
            connected_keys.add(key)
            max_val = max(max_val, value[1])
        if (spirit_r+1, spirit_c-2) in value[0] and (direction == 3 or direction == 2) :
            connected_keys.add(key)
            max_val = max(max_val, value[1])
        if (spirit_r, spirit_c-3) in value[0] and direction == 3 :
            connected_keys.add(key)
            max_val = max(max_val, value[1])

    if len(connected_keys) > 1 :
        merged_key = connected_keys.pop()
        for connected_key in connected_keys :
            connected[merged_key][0].update(connected[connected_key][0])
            del connected[connected_key]
            connected[merged_key][1] = max_val

    sum_answer += max_val
    #print(max_val-2)

print(sum_answer)