import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Colors
black = '#000000'
white = '#FFFFFF'
red = '#FF0000'
green = '#00FF00'
snake_color = '#FE2C55'  # 蛇的颜色
food_color = '#FDBC2E'  # 食物的颜色，这是金色

# Snake and food
snake_block = 20
snake_speed = 15

# Initialize clock
clock = pygame.time.Clock()

# 修改字体初始化
title_font = pygame.font.SysFont(None, 50)
subtitle_font = pygame.font.SysFont(None, 25)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, pygame.Color(snake_color), [x[0], x[1], snake_block, snake_block])

def message(title, subtitle, length, color):
    # 渲染标题
    title_surface = title_font.render(title, True, color)
    title_rect = title_surface.get_rect()
    title_rect.center = (width // 2, height // 2 - 50)

    # 渲染长度
    length_surface = subtitle_font.render(f"Length: {length}", True, color)
    length_rect = length_surface.get_rect()
    length_rect.center = (width // 2, height // 2)

    # 渲染副标题
    subtitle_surface = subtitle_font.render(subtitle, True, color)
    subtitle_rect = subtitle_surface.get_rect()
    subtitle_rect.center = (width // 2, height // 2 + 50)

    # 绘制文本
    display.blit(title_surface, title_rect)
    display.blit(length_surface, length_rect)
    display.blit(subtitle_surface, subtitle_rect)

def get_speed_multiplier(score):
    if score <= 10:
        return 0.5
    elif score <= 20:
        return 0.75
    elif score <= 30:
        return 1.0
    elif score <= 40:
        return 1.25
    elif score <= 50:
        return 1.5
    else:
        return 2.0

# 添加一个新的函数来显示长度
def show_length(length):
    length_font = pygame.font.SysFont(None, 35)
    length_surface = length_font.render(f'Length: {length}', True, white)
    length_rect = length_surface.get_rect()
    length_rect.topright = (width - 10, 10)  # 放置在右上角
    display.blit(length_surface, length_rect)

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    # 添加一个变量来跟踪当前方向
    current_direction = "RIGHT"

    while not game_over:

        while game_close:
            display.fill(black)
            message("You Lost!", "Press Q to Quit or C to Play Again", Length_of_snake, white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return gameLoop()  # 直接返回新的游戏循环

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    current_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    current_direction = "RIGHT"
                elif event.key == pygame.K_UP and current_direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    current_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    current_direction = "DOWN"

        # 修改这部分代码来实现无边界
        x1 += x1_change
        y1 += y1_change

        # 如果蛇超出边界,从另一侧出现
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - snake_block

        display.fill(black)
        pygame.draw.rect(display, pygame.Color(food_color), [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 修改碰撞检测逻辑，只检查头部是否碰到身体
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                break

        our_snake(snake_block, snake_List)
        
        # 显示长度
        show_length(Length_of_snake)

        pygame.display.update()

        # 计算当前速度
        current_length = Length_of_snake
        speed_multiplier = get_speed_multiplier(current_length - 1)
        current_speed = snake_speed * speed_multiplier

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(current_speed)

    pygame.quit()

# 主游戏循环
while True:
    gameLoop()
    break  # 如果gameLoop返回，则退出主循环
