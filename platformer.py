import pygame as pg
import time
from gravity import GravityObject

class Block:
    def __init__(self, x, y, width, height, movementDir, movementSpd, movementEnd=(-1, -1), isLava=False, isTrampoline=False):
        self.isLava = isLava
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movementDir = movementDir
        self.movementSpd = movementSpd
        self.movementStart = (x, y)
        self.movementEnd = movementEnd
        self.isTrampoline = isTrampoline

    def move(self):
        if self.movementEnd == (-1, -1):
            return False
        if self.movementDir == 'ud':
            self.y += self.movementSpd
            if self.y < self.movementEnd[1]:
                self.y = self.movementEnd[1]
                self.movementSpd *= -1
            if self.y > self.movementStart[1]:
                self.y = self.movementStart[1]
                self.movementSpd *= -1
        if self.movementDir == 'lr':
            self.x += self.movementSpd
            if self.x > self.movementEnd[0]:
                self.x = self.movementEnd[0]
                self.movementSpd *= -1
            if self.x < self.movementStart[0]:
                self.x = self.movementStart[0]
                self.movementSpd *= -1


def main():
    start = time.time()
    screen = pg.display.set_mode((800, 800))
    running = True
    pg.display.set_caption('Platformer')
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    clock = pg.time.Clock()
    p = GravityObject(10, 770, 10, 800)
    blocks = [Block(0, 780, 50, 20, 'ud', 0),Block(50, 790, 750, 100, 'lr', 0, (-1, -1), True), Block(75, 780, 50, 10, 'lr', 3, (730, 780)),
              Block(300, 750, 10, 11, 'lr', 0, (-1,-1), True), Block(600, 750, 50, 30, 'lr', 0), Block(780, 130, 20, 700, 'lr', 0, (-1,-1), True),
              Block(525, 740, 45, 15, 'ud', 3.2, (525, 420)), Block(430, 420, 50, 15, 'ud', 0), Block(180, 350, 250, 15, 'ud', 0, (-1,-1),True),
              Block(150, 600, 60, 15, 'lr', -2.8, (370, 600)),Block(50, 600, 50, 40, 'lr', 0, (370, 600)), Block(0, 600, 50, 40, 'lr', 0, (370, 600), False, True),
              Block(180, 330, 50, 20, 'lr', 0, (370, 600)),Block(180, 0, 250, 15, 'ud', 0, (-1,-1),True),Block(230, 330, 150, 20, 'lr', 0, (370, 600), False, True),
              Block(380, 330, 50, 20, 'lr', 0, (370, 600)), Block(480, 330, 75, 20, 'ud', 3, (480, 50)), Block(650, 420, 50, 30, 'lr', 0, (370, 600), False, True)]
    lastTime = False
    deaths = 0
    while running:
        floorBlock = 0
        currentFloor = 800
        floorIsLava = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        pg.draw.circle(screen, 'green', (p.x, p.y), 10)
        for block in blocks:
            if block.isLava:
                pg.draw.rect(screen, 'red', (block.x, block.y, block.width, block.height))
            elif block.isTrampoline:
                pg.draw.rect(screen, 'blue', (block.x, block.y, block.width, block.height))
            else:
                pg.draw.rect(screen, 'gray', (block.x, block.y, block.width, block.height))
            if block.x < p.x < block.x + block.width and block.y > p.y:
                if block.y < currentFloor:
                    floorBlock = blocks.index(block)
                    if block.isLava:
                        floorIsLava = True
                    else:
                        floorIsLava = False
                    currentFloor = block.y
            block.move()
        p.floor = currentFloor
        if pg.key.get_pressed()[pg.K_UP] or pg.key.get_pressed()[pg.K_w]:
            if p.y == p.floor - p.length:
                if blocks[floorBlock].isTrampoline:
                    if blocks[floorBlock].height == 20:
                        p.jump(38)
                    elif blocks[floorBlock].height == 30:
                        p.jump(45.6)
                    else:
                        p.jump(56)
                else:
                    p.jump()
        p.gravity()
        if pg.key.get_pressed()[pg.K_LEFT] or pg.key.get_pressed()[pg.K_a]:
            p.x -= 3
            if p.x < 10:
                p.x = 10
            if p.y + p.length >= p.floor:
                p.y = p.floor - p.length
                p.fallSpeed = 1
            for block in blocks:
                if block.x - 10 < p.x < block.x + block.width + 10 and block.y - 10 < p.y < block.y + block.height + 10:
                    if block.isLava:
                        p.x = 10
                        p.y = 770
                        deaths += 1
                        p.jumping = False
                    else:
                        if block.x > p.x - 10:
                            p.x = block.x - 10
                        if block.x + block.width < p.x + 10:
                            p.x = block.x + block.width + 10
                        if block.y > p.y - 10:
                            p.y = block.y - 10
                            p.jumping = False
                        if block.y + block.height < p.y + 10:
                            p.y = block.y + block.height + 10

        elif pg.key.get_pressed()[pg.K_RIGHT] or pg.key.get_pressed()[pg.K_d]:
            p.x += 3
            if p.x > 790:
                p.x = 790
                break

            for block in blocks:
                if block.x - 10 < p.x < block.x + block.width + 10 and block.y - 10 < p.y < block.y + block.height + 10:
                    if block.isLava:
                        p.x = 10
                        p.y = 770
                        deaths += 1
                        p.jumping = False
                    else:
                        if block.x > p.x - 10:
                            p.x = block.x - 10
                        if block.x + block.width < p.x + 10:
                            p.x = block.x + block.width + 10
                        if block.y > p.y - 10:
                            p.y = block.y - 10
                            p.jumping = False
                        if block.y + block.height < p.y + 10:
                            p.y = block.y + block.height + 10
        elif pg.key.get_pressed()[pg.K_DOWN] or pg.key.get_pressed()[pg.K_s]:
            if not lastTime:
                p.jumping = False
                lastTime = True
        else:
            lastTime = False
            p.acceleration = 0.4
        if p.floor <= p.y + 10 <= p.floor + blocks[floorBlock].height and floorIsLava:
            p.x = 10
            deaths += 1
            p.y = 770
            p.jumping = False
        for block in blocks:
            if block.x - 10 < p.x < block.x + block.width + 10 and block.y - 10 < p.y < block.y + block.height + 10:
                if block.isLava:
                    p.jumping = False
                    p.x = 10
                    p.y = 770
                    deaths += 1

                else:
                    if block.x > p.x-10:
                        p.x = block.x - 10
                    if block.x + block.width < p.x + 10:
                        p.x = block.x + block.width + 10
                    if block.y > p.y - 10:
                        p.jumping = False
                        p.y = block.y - 10
                    if block.y + block.height < p.y - 10:
                        p.y = block.y + block.height + 10
        if p.y + 10 == p.floor:
            if p.y + p.length >= p.floor:
                p.y = p.floor - p.length
                p.fallSpeed = 1
                if blocks[floorBlock].isTrampoline:
                    if blocks[floorBlock].height == 20:
                        p.jump(38)
                    else:
                        p.jump(56)
            if blocks[floorBlock].movementDir == 'ud':
                p.y += blocks[floorBlock].movementSpd
            else:
                p.x += blocks[floorBlock].movementSpd
        pg.display.update()
        clock.tick(60)
        screen.fill('white')
        if p.x == 10 and p.y == 790:
            p.y = 780
    pg.font.init()
    image = pg.image.load(r'prize.png')
    font = pg.font.SysFont('Arial', 30)
    pg.display.set_caption('You Win!')
    end = time.time()
    totalTime = int(end - start)
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        text_surface1 = font.render('You Win!', True, (10, 245, 143))
        text_rect = text_surface1.get_rect(center=(400, 300))
        screen.blit(text_surface1, text_rect)
        text_surface2 = font.render(f'Your final time is {totalTime // 3600} hours, {totalTime // 60} minutes, and {totalTime % 60} seconds.', True, (10, 245, 143))
        if pg.key.get_pressed()[pg.K_c]:
            break
        text_rect = text_surface2.get_rect(center=(400, 400))
        screen.blit(text_surface2, text_rect)
        text_surface3 = font.render(f'You died {deaths} times.', True, (10, 245, 143))
        text_rect = text_surface3.get_rect(center=(400, 500))
        screen.blit(text_surface3, text_rect)
        text_surface4 = font.render('Press C to claim your prize.',True, (10, 245, 143))
        text_rect = text_surface4.get_rect(center=(400, 600))
        screen.blit(text_surface4, text_rect)
        pg.display.update()
        clock.tick(60)
        screen.fill('orange')
    screen = pg.display.set_mode((1121, 632))
    pg.display.set_caption('Hecker has hacked your pc')
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(image, (0, 0))
        pg.display.update()
        clock.tick(60)
        screen.fill('white')

main()
