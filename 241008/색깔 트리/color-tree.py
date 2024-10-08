n = int(input())
orders = []
nodes = {}

for _ in range(n) :
    orders.append(list(map(int, input().split())))

class Node :
    def __init__(self, m_id, p_id, color, max_depth) :
        self.m_id = m_id            # int로 저장함
        self.p_id = p_id            # int로 저장함
        self.color = color          # int로 저장함
        self.max_depth = max_depth  # int로 저장함
        self.children = []          # index로 저장함 - 객체 저장 X

    def _is_addable(self) :
        p_id = self.p_id
        if p_id == -1 :  
            return True
        standard = 2
        while p_id != -1 :
            p_node = nodes[p_id]
            if p_node.max_depth >= standard :
                p_id = p_node.p_id
                standard += 1
            else :
                return False
        return True

    def add(self) :
        if self.p_id == -1:  
            nodes[self.m_id] = self
        elif self._is_addable(): 
            p_node = nodes[self.p_id]
            p_node.children.append(self.m_id) 
            nodes[self.m_id] = self 

    def change_color(self, new_color) :
        self.color = new_color
        for child_idx in self.children :
            child = nodes[child_idx]
            child.change_color(new_color)

    def get_color(self) :
        return self.color

    def get_value(self, color_set=None) :
        if color_set is None:  
            color_set = set()
        color_set.add(self.color)
        for child_idx in self.children :
            child = nodes[child_idx]
            child.get_value(color_set)
        return len(color_set)

for order in orders :
    if order[0] == 100 :
        _, m_id, p_id, color, max_depth = order
        new_node = Node(m_id, p_id, color, max_depth)
        new_node.add()

    elif order[0] == 200 :
        _, m_id, color = order
        nodes[m_id].change_color(color)

    elif order[0] == 300 :
        _, m_id = order
        print(nodes[m_id].get_color())

    elif order[0] == 400 :
        total_value = 0
        for node in nodes.values() :
            total_value += node.get_value() ** 2
        print(total_value)