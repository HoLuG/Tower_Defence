import math


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        # define menu and buttons

        self.tower_imgs = []
        self.damage = 1

        self.place_color = (0, 0, 255, 100)

    def draw(self, win):
        img = self.tower_imgs[self.level - 1]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

    def click(self, x, y):
        img = self.tower_imgs[self.level - 1]
        if x <= self.x - img.get_width()//2 + self.width and x >= self.x - img.get_width()//2:
            if y <= self.y + self.height - img.get_height()//2 and y >= self.y - img.get_height()//2:
                return True
        return False

    def sell(self):
        return self.sell_price[self.level-1]

    def move(self, x, y):
        self.x = x
        self.y = y

    def collide(self, othertower):
        x2 = othertower.x
        y2 = othertower.y
        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        if dis >= 100:
            return False
        else:
            return True
