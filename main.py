from pygame import *
from assets_table import *
from classes import *
from langs import *

lang = "UKR"
need_to_win = 50
need_to_lose = 20

game_run, game_finish = True, False

display.set_caption(languages[lang]["GAMENAME"])

clock = time.Clock()

background = MakeImage(sprites["BACKGROUND"], win_width, win_height)

player = Player(sprites["PLAYER"], 5, win_height - 100, 100, 120, 9)

monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

mixer.init()
mixer.music.load(sounds["MUSIC"])
mixer.music.play()

fire = mixer.Sound(sounds["FIRE"])

font.init()
font_main = font.Font(None, 48)

font_screens = font.Font(None, 92)

delay = 50
spawnrate = delay
delay2 = 100
spawnrate2 = delay2 

while game_run:
    for e in event.get():
        if e.type == QUIT:
            game_run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                player.fire()

    if not game_finish:
        if spawnrate <= 0:
            monster = Enemy(sprites["ENEMY"], randint(
                80, win_width - 80), -50, 80, 90, randint(3, 5))
            monsters.add(monster)
            delay -= 2
            spawnrate = delay
            if delay <= 16:
                delay += 2
        else:
            spawnrate -= 1    
        window.blit(background, (0, 0))
        
        if spawnrate2 <= 0:
            asteroid = Enemy2(sprites["ASTEROID"], randint(
                80, win_width - 80), -50, 80, 90, 2)
            asteroids.add(asteroid) 
            delay2 -= 1
            spawnrate2 = delay2
            if delay2 <= 5:
                delay2 += 1
        else:
            spawnrate2 -= 1
            
        kills_text = font_main.render(
            languages[lang]["SCORE_KILLS"] + str(player.kills), True, (255, 255, 255))
        window.blit(kills_text, (10, 10))

        losts_text = font_main.render(
            languages[lang]["SCORE_MISSES"] + str(player.losts), True, (255, 255, 255))
        window.blit(losts_text, (10, 60))

        player.reset()  # отрисовка
        player.update()  # управление

        player.bullets.draw(window)
        player.bullets.update()

        monsters.draw(window)
        monsters.update()
        
        asteroids.draw(window)
        asteroids.update()
        
        if player.kills >= need_to_win:
            win_screen = font_screens.render(
                languages[lang]["WIN_TEXT"], True, (50, 255, 0))
            window.blit(win_screen, (225, 225))
            game_finish = True

        if player.losts >= need_to_lose:
            lose_screen = font_screens.render(
                languages[lang]["LOSE_TEXT"], True, (225, 0, 0))
            window.blit(lose_screen, (225, 225))
            game_finish = True

        if sprite.groupcollide(monsters, player.bullets, True, True):
            player.kills += 1
            
        
        if sprite.spritecollide(player, monsters, False):
            lose_screen = font_screens.render(
                languages[lang]["LOSE_TEXT"], True, (225, 0, 0))
            window.blit(lose_screen, (225, 225))
            game_finish = True
        
        if sprite.spritecollide(player, asteroids, False):
            lose_screen = font_screens.render(
                languages[lang]["LOSE_TEXT"], True, (225, 0, 0))
            window.blit(lose_screen, (225, 225))
            game_finish = True
        display.update()

    clock.tick(60)
