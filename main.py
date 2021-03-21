import pygame
import time
import random
import config

# 常數變量
white = config.white
yellow = config.yellow
black = config.black
snake_color = config.white
bg_color = config.black
food_color = config.yellow

fps = config.fps
block_size = config.block_size
window_width = config.window_width
window_height = config.window_height
x_block_num = round(window_width / block_size)
y_block_num = round(window_height / block_size)

pygame.init()
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 24)
pygame.display.set_caption('貪食蛇')

# 繪畫貪食蛇
def draw_snake(window, snake):
	for coord in snake:
		[x, y] = coord
		pygame.draw.rect(window, snake_color, [x * block_size, y * block_size, block_size, block_size])

# 繪畫food
def draw_food(window, food):
	if food:
		[x, y] = food
		pygame.draw.rect(window, food_color, [x * block_size, y * block_size, block_size, block_size])

# 計算新food的坐標，成功則返回food的坐標，否則返回空白list
def get_new_food(window, snake):
	food_x = round(random.randrange(0, x_block_num))
	food_y = round(random.randrange(0, y_block_num))
	if [food_x, food_y] in snake:
		return []
	else:
		return [food_x, food_y]

# 在window上打印字句
def toast(window, message, color):
	msg = font_style.render(message, True, color)
	window.blit(msg, [window_width / 10, window_height / 10])

# 貪食蛇的位移矢量，初始為零，即貪食蛇不會移動，直到玩家按下第一個方向鍵
x_v = 0
y_v = 0
# 貪食蛇頭部的初始位置
x = 10
y = 10
# 貪食蛇的坐標list，第一個元素為初始位置
snake = [[x, y]]
# food的初始坐標
food = []
# 貪食蛇的行走方向，只有初始時為stop
snake_direction = 'stop'
# 離開遊戲的flag
game_quit = False
# 每局遊戲完結的flag
game_over = False

while not game_quit:
	# 當Game Over時，打印分數
	while game_over:
		window.fill(bg_color)
		message = 'You Lost! Your score: {score}. Press Q to quit game'.format(score = len(snake) - 1)
		toast(window, message, snake_color)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				# 按Q離開遊戲
				if event.key == pygame.K_q:
					game_quit = True
					game_over = False
	# 每當有按鍵被觸發時
	for event in pygame.event.get():
		# 按了X離開遊戲
		if event.type == pygame.QUIT:
			game_quit = True
		# 處理上下左右按鍵，並依方向更新貪食蛇的矢量，禁止直接轉換相反方向
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and snake_direction != 'down':
				x_v = 0
				y_v = -1
				snake_direction = 'up'
			elif event.key == pygame.K_DOWN and snake_direction != 'up':
				x_v = 0
				y_v = 1
				snake_direction = 'down'
			elif event.key == pygame.K_LEFT and snake_direction != 'right':
				x_v = -1
				y_v = 0
				snake_direction = 'left'
			elif event.key == pygame.K_RIGHT and snake_direction != 'left':
				x_v = 1
				y_v = 0
				snake_direction = 'right'
	# 更新window，清除上一幀的畫面
	window.fill(black)

	# 更新貪食蛇頭部位置
	x = x + x_v
	y = y + y_v

	# 檢查有沒有出界
	if x > x_block_num or x < 0:
		game_over = True
		continue
	if y > y_block_num or y < 0:
		game_over = True
		continue

	# 檢查有沒有咬到自己
	if [x, y] in snake[1:]:
		game_over = True
		continue

	# 檢查有沒有吃到食物
	if food in snake:
		food = []
	else:
		# 清除最尾的block
		snake.pop(0)

	# append貪食蛇頭部位置到snake
	snake.append([x, y])

	# 更新food的位置
	if not food:
		food = get_new_food(window, snake)

	# 繪畫貪食蛇
	draw_snake(window, snake)
	# 繪畫food
	draw_food(window, food)

	# 呼叫update()，更新window
	pygame.display.update()
	clock.tick(fps)

pygame.quit()
quit()
