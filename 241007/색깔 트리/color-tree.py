import sys
sys.setrecursionlimit(10000000)

n = int(input())

orders = []

for _ in range(n):
    order = list(map(int, input().split()))
    orders.append(order)

class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        self.m_id = m_id
        self.p_id = p_id
        self.color = color
        self.max_depth = max_depth
        self.children = [] 

    def add_child(self, child_node):
        if self.max_depth > 1:
            self.children.append(child_node)

    def change_color(self, color):
        self.color = color
        for child in self.children:
            child.change_color(color)

    def get_value(self, colors):
        colors.add(self.color)
        for child in self.children:
            child.get_value(colors)

nodes = {}
roots = []

for order in orders:
    # 노드 추가
    if order[0] == 100: 
        _, m_id, p_id, color, max_depth = order
        node = Node(m_id, p_id, color, max_depth)

        if p_id == -1:
            roots.append(m_id)
            nodes[m_id] = node
        else:
            parent = nodes[p_id]
            # p_id는 항상 이미 존재하는 노드라고 가정
            if parent.max_depth > 1:
                nodes[m_id] = node
                parent.add_child(node)
                parent.max_depth -= 1

    # 색깔 변경
    elif order[0] == 200: 
        _, m_id, color = order
        nodes[m_id].change_color(color)

    # 색깔 조회
    elif order[0] == 300: 
        _, m_id = order
        print(nodes[m_id].color)

    # 점수 조회
    elif order[0] == 400: 
        value = 0

        # 모든 노드에 대해 계산
        for node in nodes.values():  # 수정: values()로 변경
            colors = set()
            node.get_value(colors)
            value += len(colors) ** 2
        
        print(value)