from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
BLOCK_SIZE = 50
GAME_BG = 'BLACK'
SNAKE_SIZE = 3
SNAKE_COLOR = 'BLUE'
FOOD_COLOR = 'YELLOW'
GAME_SPEED = 100

class Snake:
    def __init__(self):
        self.rectangles = []
        self.coordinates = []

        for body_part in range(SNAKE_SIZE):
            self.coordinates.append((0,0))

        for x,y in self.coordinates:
            rectangle = canvas.create_rectangle(x,y,x+BLOCK_SIZE,y+BLOCK_SIZE,fill=SNAKE_COLOR,tag="snake")
            self.rectangles.append(rectangle)

class Food:
    def __init__(self):
        x = random.randint(0,(GAME_WIDTH/BLOCK_SIZE)-2)*BLOCK_SIZE
        y = random.randint(0,(GAME_HEIGHT/BLOCK_SIZE)-2)*BLOCK_SIZE

        self.coordinates = (x,y)

        canvas.create_oval(x,y,x+BLOCK_SIZE,y+BLOCK_SIZE,fill=FOOD_COLOR,tag="food")

def change_direction(new_direction):
    global direction

    if new_direction == 'down' and direction != 'up':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'left' and direction != 'right':
        direction = new_direction


def next_turn(snake, food):
    global direction
    global score

    x = snake.coordinates[0][0]
    y = snake.coordinates[0][1]

    if direction == 'down':
        y += BLOCK_SIZE
    elif direction == 'up':
        y -= BLOCK_SIZE
    elif direction == 'right':
        x += BLOCK_SIZE
    elif direction == 'left':
        x -= BLOCK_SIZE

    snake.coordinates.insert(0,(x,y))
    rectangle = canvas.create_rectangle(x,y,x+BLOCK_SIZE,y+BLOCK_SIZE,fill=SNAKE_COLOR,tag="snake")
    snake.rectangles.insert(0,rectangle)

    if food.coordinates == snake.coordinates[0]:
        score += 1
        score_label.config(text="score:"+str(score))
        canvas.delete("food")
        del food.coordinates
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.rectangles[-1])
        del snake.rectangles[-1]    #delete specific index

    if check_collision(snake):
        game_over()
    else:
        window.after(GAME_SPEED,lambda snake=snake, food=food:next_turn(snake,food))

def check_collision(snake):
    if snake.coordinates[0][0] < 0 or snake.coordinates[0][0] >= GAME_WIDTH:
        return True
    elif snake.coordinates[0][1] < 0 or snake.coordinates[0][1] >= GAME_HEIGHT:
        return True

    for i in snake.coordinates[1:]:
        if snake.coordinates[0] == i:
            return True

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       text="GAME OVER", font=('consolas', 50), fill='red', tag="gameover")


window = Tk()
window.resizable(False,False)
x = int(window.winfo_screenwidth()/2-GAME_WIDTH/2)
y = int(window.winfo_screenheight()/2-GAME_HEIGHT/2)
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y-30}")

score = 0

score_label = Label(window, text="score:"+str(score),font=("consolas",30))
score_label.pack()

canvas = Canvas(window,width=GAME_WIDTH,height=GAME_HEIGHT,bg=GAME_BG)
canvas.pack()

food = Food()
snake = Snake()

direction='down'
window.bind("<Down>", lambda event: change_direction('down')) #gotta remembet these commanmds
window.bind("<Up>", lambda event: change_direction('up'))
window.bind("<Right>", lambda event: change_direction('right'))
window.bind("<Left>", lambda event: change_direction('left'))

next_turn(snake,food)

window.mainloop()
