#coding:utf-8

class MyGO(object):
    def __init__(self):
        self.stones = []
        self.groups = []
        self.next_color = 'BLACK'

    def add_stone(self, point):
        # 若该位置已经有棋子
        for stone in self.stones:
            if point == stone.point:
                return False
        # 落子
        stone = Stone(point, color)

        # 更新棋盘groups，将新子加入一个group或者将几个group合并，提去死子
        new_groups = self.update_groups(stone)

        # 判断新子是否存活
        if self.is_alive(stone, new_groups) == False:
            return False
        else:
            self.stones.append(stone)
            self.groups = new_groups

    def is_alive(self, stone, new_groups):
        for group in new_groups:
            for st in group.stones:
                if stone.point == st.point:
                    return True
        return False

    def search(self, point, groups):
        for group in groups:
            for stone in group.stones:
                if stone.point == point:
                    return True
        return False

    def update_groups(self, stone):
        new_groups = []
        connected_groups = []
        for group in self.groups:
            for st in group:
                if st.point in stone.find_neighbor() and st.color == stone.color:
                    connected_groups.append(group)
                    break
            new_groups.append(group)

        if len(connected_groups) > 0:
            merge_group = Group()
            for group in connected_groups:
                for st in group.stones:
                    merge_group.stones.append(st)
            merge_group.stones.append(stone)
            new_groups.append(merge_group)
        else:
            merge_group = Group()
            merge_group.stones.append(stone)
            new_groups.append(merge_group)

        ret_group = []
        for group in new_groups:
            chis = []
            if stone not in group:
                for xx in stone.find_neighbor():
                    if self.search(xx, new_groups) == False:
                        chis.append(xx)


    def turn(self):
        if self.next_color == 'BLACK':
            self.next_color = 'WHITE'
            return 'BLACK'
        else:
            self.next_color = 'BLACK'
            return 'WHITE'

class Group(object):
    def __init__(self):
        self.stones = []
        self.chis = []

    def add_stone(self):
        pass

    def update_chi(self):
        pass

class Stone(object):
    def __init__(self, point, color):
        self.point = point
        self.color = color

    def find_neighbor(self):
        neighboring = [(self.point[0] - 1, self.point[1]),
                       (self.point[0] + 1, self.point[1]),
                       (self.point[0], self.point[1] - 1),
                       (self.point[0], self.point[1] + 1)]
        for point in neighboring:
            if not 0 <= point[0] < 19 or not 0 <= point[1] < 19:
                neighboring.remove(point)
        return neighboring