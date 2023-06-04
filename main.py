from pygame import *
from random import randint


from pygame.sprite import Group
 
# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
# шрифти і написи
font.init()
font2 = font.SysFont("Arail", 36)
 
# нам потрібні такі картинки:
img_back = "galaxy.jpeg"  # фон гри
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # ворог
 
score = 0  # збито кораблів
lost = 0  # пропущено кораблів


class Button(sprite.Sprite):
    def __init__(self, x, y, width, height, color, text):
        super().__init__()
        self.text = font2.render(text, 1, (0, 0, 0))

        self.image = Surface((self.text.get_width(), self.text.get_height()))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.text, (self.rect.x, self.rect.y))

    def on_click(self):
        is_clicked = mouse.get_pressed()[0]
        if is_clicked:
            x, y = mouse.get_pos()
            if self.rect.collidepoint(x, y):
                global finish, lost, score
                finish = False
                lost = score = 0
                
                for m in monsters:
                    m.respawn()
 
# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()
            fire_sound.play()
 
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
 
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.respawn()
            lost += 1

    def respawn(self):
        self.rect.x = randint(80, win_width - 80)
        self.rect.y = -self.rect.height
   
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
 
# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


bullets = sprite.Group()
monsters = sprite.Group()
for i in range(6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
 
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна


btn = Button(250, 250, 100, 80, (255, 255, 255), "Почати гру")


while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
 
    if not finish:
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for _ in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        # оновлюємо фон
        window.blit(background, (0, 0))


        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()


        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        if sprite.spritecollide(ship, monsters, False) or lost >= 5:
            finish = True


        if score >= 10:
            finish = True
           
        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
    else:
        btn.draw()
        btn.on_click()
        if score >= 10:
            text_win = font2.render("Ви даун", 1, (255, 255, 255))
            window.blit(text_win, (200, 200))
        else:
            text_loose = font2.render("Ви даун", 1, (255, 255, 255))
            window.blit(text_loose, (200, 200))


   


    display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)


