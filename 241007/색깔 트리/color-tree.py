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

    def get_value(self, colors) :
        colors.add(self.color)
        for child in self.children :
            child.get_value(colors)

nodes = {}
roots = []

for order in orders :
    #노드추가
    #100 m_id p_id color max_depth
    if order[0] == 100 : 
        _, m_id, p_id, color, max_depth = order

        node = Node(m_id, p_id, color, max_depth)

        if p_id == -1 :
            roots.append(m_id)
            nodes[m_id] = node
        else :
            parent = nodes[p_id]
            # 문제조건 : m_id 는 새로 추가되는 노드 번호로 항상 새로운 값이 주어지며, p_id는 −1 이 아닌 이상 항상 이미 주어진 노드 번호가 주어짐을 가정해도 좋습니다.

            if parent.max_depth > 1 :
                nodes[m_id] = node
                parent.add_child(node)
                parent.max_depth -= 1

    #색깔 변경
    #200 m_id color
    elif order[0] == 200 : 
        _, m_id, color = order
        nodes[m_id].change_color(color)

    #색깔 조회
    #300 m_id
    elif order[0] == 300 : 
        _, m_id = order
        print(nodes[m_id].color)

    #점수 조회
    #이 경우 모든 노드의 가치를 계산하여, 가치 제곱의 합을 출력합니다.
    #각 노드의 가치는 해당 노드를 루트로 하는 서브트리 내 서로 다른 색깔의 수로 정의됩니다.
    elif order[0] == 400 : 
        value = 0

        for node in nodes.valus()
            colors = set()
            node.get_value(colors)
            value += len(colors)**2
        
        print(value)