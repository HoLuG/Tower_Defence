class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.tower_imgs = []

    def draw(self, win):
        img = self.tower_imgs[0]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))
