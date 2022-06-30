class GravityObject:
    def __init__(self, x, y, length, floor):
        self.fallSpeed = 1
        self.acceleration = 0.5
        self.x = x
        self.y = y
        self.length = length
        self.floor = floor
        self.jumping = False
        self.jumpRate = 0

    def gravity(self):
        if self.jumping:
            self.y -= self.jumpRate
            if self.y <= self.length:
                self.jumpRate = 0
                self.jumping = False
                self.fallSpeed = 1
                self.y = 0
            self.jumpRate -= self.fallSpeed
            self.fallSpeed += self.acceleration
            if self.jumpRate <= 0:
                self.jumpRate = 0
                self.jumping = False
                self.fallSpeed = 1
            return False
        if self.y + self.length >= self.floor:
            self.y = self.floor - self.length
            self.fallSpeed = 1
            return False
        self.y += self.fallSpeed
        self.fallSpeed += self.acceleration

    def jump(self, speed=15):
        self.jumping = True
        self.jumpRate = speed
        self.fallSpeed = 1
