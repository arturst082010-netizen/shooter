#Создай собственный Шутер!
from random import randint
from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self):
        super().__init__('rocket.png', 200, 400, 7, 67, 67)
    def update(self):
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or  keys[K_RIGHT])  and self.rect.x < len_size - 70:
            self.rect.x += self.speed
    #     if (keys[K_w] or keys[K_UP]) and self.rect.y > 5:
    #         self.rect.y -= self.speed
    #     if (keys[K_s] or keys[K_DOWN]) and self.rect.y < width_size - 70:
    #         self.rect.y += self.speed
    def fire(self):
        keys = key.get_pressed()
        if (keys[K_SPACE]):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            fire.play()
    def set_speed(self, level):
        speeds = [5, 6, 7, 8, 67, 76]
        self.speed = speeds[level]
            

class Enemy(GameSprite):
    def __init__(self):
        super().__init__('ufo.png', randint(0, 630), 0, randint(1, 3), 70, 40) 
    def update(self):
        if self.rect.y <= width_size:
            self.rect.y += self.speed
        else:
            global miss_num
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            self.speed = randint(1, 3)
            miss_num += 1

class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__('bullet.png', x, y, 7, 5, 15)
    def update(self):
        if self.rect.y <= width_size:
            self.rect.y -= self.speed
        else:
            self.kill()



        

len_size = 700
width_size = 500
window = display.set_mode((700, 500))
display.set_caption('Шутер')
clock = time.Clock()
FPS = 67
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
ufoes = [Enemy(), Enemy(), Enemy(), Enemy(), Enemy()]
monsters = sprite.Group()
for ufo in ufoes:
    monsters.add(ufo)

bullets = sprite.Group()
font.init()
font = font.Font(None, 50)
score_num = 0
miss_num = 0



            


rocket = Player()
finish = False
game = True
level = 0
score_enemy = [50, 67, 100, 150, 167]
while game:
    score = font.render(
                'Счет: ' + str(score_num), True, (255, 255, 255)
            )
    miss = font.render(
                'Пропущено: ' + str(miss_num), True, (255, 255, 255)
            )
    levell = font.render(
                'Уровень: ' + str(level), True, (255, 255, 255)
            )
    rocket.fire()
    if not finish:
        window.blit(background, (0, 0))
        rocket.update()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        rocket.reset()
        monsters.draw(window)
        window.blit(score, (10, 20))
        window.blit(miss, (10, 50))
        window.blit(levell, (10, 80))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score_num += 1
            monsters.add(Enemy())
        colligion = sprite.spritecollideany(rocket, monsters)
        if colligion or miss_num > 3:
            lose = font.render(
                'LOSE ', True, (255, 255, 255)
            )
            window.blit(lose, (300, 250))
            finish = True
        if score_num > score_enemy[level]:
            win = font.render(
                'WIN', True, (255, 255, 255)
            )
            window.blit(win, (300, 250))
            level += 1
            score_num = 0
            rocket.set_speed(level)
            display.update()
            clock.tick(1)
            if level >= len(score_enemy):
                finish = True

    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)