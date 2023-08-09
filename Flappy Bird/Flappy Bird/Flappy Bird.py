#импорты
from random import randint
from pygame import *
font.init()
mixer.init()

#создаем окно
WIDTH, HEIGHT = 800, 600
FPS = 60
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Flappy Bird')
clock = time.Clock()

#шрифты
font_ = font.Font(None, 40)
text_start = font_.render('Нажми на пробел или левую кнопку мыши для старта.', 1, (255, 255, 255))
font1 = font.Font(None, 170)
text_lose = font1.render('GAME OVER', 1, (255, 0, 0))

#музыка
background_music = mixer.music.load('background_music.wav')
mixer.music.play(-1)
collide_sound = mixer.Sound('collide_sound.wav')
# картинки
bg = transform.scale(image.load('background.jpeg'), (WIDTH, HEIGHT))
imgPT = transform.scale(image.load('pipe_top.png'), (90, 280))
imgPB = transform.scale(image.load('pipe_bottom.png'), (90, 200))

lifes = 3
score = 0
timer = 30

#птица
py, sy, ay = 300, 0, 0
player = transform.scale(image.load('bird-removebg-preview (3).png'), (60, 40))
rect_player = player.get_rect()
rect_player.x = WIDTH // 3
rect_player.y = py

fill_color = (0,255,0)
pipes = []

#игровое состояние
state = 'start'

pipe_speed = 3
play = True
finish = False
while play:
    if not finish:
        for e in event.get():
            if e.type == QUIT:
                play = False

        press = mouse.get_pressed() #возвращает список значений связанных с мышью (True or False)
        keys = key.get_pressed() #возвращает список значений связанных с клавиатурой (True or False)
        click = press[0] or keys[K_SPACE]
    
        if timer > 0:
            timer -= 1

        for i in range(len(pipes)-1, -1, -1):
            pipe = pipes[i]
            if not lifes == 0: #движение труб
                pipe.x -= pipe_speed
            if pipe.x < 400 and pipe.x > 397 and state == 'play': #условие прибавления очков
                score += 1
                

            if pipe.right < 0: #удаление труб вне зоне нашей видимости
                pipes.remove(pipe)
        if state == 'start' and lifes != 0:
            if click and timer == 0 and len(pipes) == 0:
                state = 'play'

            #возвращение к первоначальному месту
            py += (HEIGHT // 2 - py) * 0.1
            rect_player.y = py
        elif state == 'play':
            if click:
                ay = -2
            else:
                ay = -0.5
            py += sy
            sy = (sy + ay + 1) * 0.98
            rect_player.y = py
        
            #создание труб
            if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 480:
                pipes.append(Rect(800, 0, 90, randint(250, 280)))
                pipes.append(Rect(800, randint(430, 550), 90, 200))
                

            #если игрок вылетел за зону игры (вверх или вниз)
            if rect_player.top < 0 or rect_player.bottom > HEIGHT:
                collide_sound.play()
                lifes -= 1
                state = 'start'
            
            #столкновения с трубами
            for pipe in pipes:
                if rect_player.colliderect(pipe):
                    collide_sound.play()
                    lifes -= 1
                    state = 'start'
            
        elif state == 'fall':
            sy, ay = 0, 0
            timer = 30
        else:
            pass
        
        window.blit(bg, (0, 0))
        if state == 'start' and lifes == 3:
            window.blit(text_start, (40, 150))
        
        for pipe in pipes:
            #тут мы определяем какая труба (верхняя или нижняя)
            if pipe.y == 0:
                rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
                window.blit(imgPT, rect)
            else:
                rect = imgPB.get_rect(topleft = pipe.topleft)
                window.blit(imgPB, rect)
        
        if lifes == 3:
            fill_color = (0, 255, 0)
        elif lifes == 2:
            fill_color = (255, 255, 0)
        else:
            fill_color = (255, 0, 0)
        
        text_score = font_.render('score:' + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 10))
        text_lifes = font_.render('lifes:' + str(lifes), 1, fill_color)
        window.blit(text_lifes, (10, 40))
        

        window.blit(player, (rect_player.x, rect_player.y))

        if lifes <= 0:
            window.blit(text_lose, (40, 250))

        display.update()
        clock.tick(FPS)