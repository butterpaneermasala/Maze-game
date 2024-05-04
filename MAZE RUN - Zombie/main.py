import turtle
import random
from maze_container import level_1, level_2, level_3
from maze_sprites import *

wn = turtle.Screen()
wn.bgcolor('#ffdead')
wn.title('Maze Runner')
wn.setup(width=700, height=700)
wn.tracer(0)
grid_block_size = 24

# set up sprites
for sprite in maze_images:
    wn.register_shape(sprite)

# Create a game over screen turtle
game_over_screen = turtle.Turtle()
game_over_screen.hideturtle()
game_over_screen.penup()
game_over_screen.color("red")
game_over_screen.goto(0, 0)
game_over_screen.hideturtle()


# Create a score turtle for score display
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.color("black")
score_turtle.goto(250, 300)
score_turtle.write("Score: 0", align="right", font=("Arial", 16, "bold"))

# Create a level display turtle
level_turtle = turtle.Turtle()
level_turtle.hideturtle()
level_turtle.penup()
level_turtle.color("black")
level_turtle.goto(-250, 300)
level_turtle.write("Level: ", align="left", font=("Arial", 16, "bold"))

# classes
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color('#362020')
        self.shape("bush.gif")
        self.penup()
        self.speed(0)
        self.name = 'Wall'


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.name = 'Player'
        self.shape("p-right.gif")
        self.gold = 0

    def move_up(self):
        new_x_cor = self.xcor()
        new_y_cor = self.ycor() + 24
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(new_x_cor, new_y_cor)

    def move_down(self):
        new_x_cor = self.xcor()
        new_y_cor = self.ycor() - 24
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(self.xcor(), self.ycor() - 24)

    def move_left(self):
        new_x_cor = self.xcor() - 24
        new_y_cor = self.ycor()
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(new_x_cor, new_y_cor)
            self.shape("p-right.gif")

    def move_right(self):
        new_x_cor = self.xcor() + 24
        new_y_cor = self.ycor()
        check = check_wall_collision(new_x_cor, new_y_cor, walls)
        if check:
            self.setposition(new_x_cor, new_y_cor)
            self.shape("p-left.gif")

    def hide(self):
        hide_sprite(self)
        display_game_over()

    def update_score(self):
        score_turtle.clear()
        score_turtle.write("Score: {}".format(self.gold), align="right", font=("Arial", 16, "bold"))

    def check_win(self):
        if len(treasures) == 0:
            self.hideturtle()
            game_over_screen.clear()
            game_over_screen.goto(0, 0)
            game_over_screen.write("You have won! Score: {}".format(self.gold), align="center",
                                   font=("Arial", 24, "bold"))

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.name = 'Treasure'
        self.shape('diamond.gif')
        self.color('#D4AF37')
        self.gold = 100
        self.goto(x, y)

    def hide(self):
        global game_over_screen
        global player
        player.gold += self.gold
        self.goto(2000, 2000)  # Move treasure out of sight
        self.hideturtle()
        player.update_score()
        if len(treasures)*2 == player.gold:  # Check if all treasures are collected
            game_over_screen.clear()  # Clear any previous game over message
            game_over_screen.goto(0, 0)
            game_over_screen.write("You have won! Score: {}".format(player.gold), align="center", font=("Arial", 24, "bold"))
            # End the game by exiting the main loop
            wn.bye()

        
        


class Zombie(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.gold = 50
        self.name = 'Zombie'
        self.shape('zombie-right.gif')
        self.setposition(x, y)
        self.direction = set_direction()

    def change_direction(self):
        if self.direction == 'up':
            dx = 0
            dy = 24
        elif self.direction == 'down':
            dx = 0
            dy = -24
        elif self.direction == 'left':
            dx = -24
            dy = 0
            self.shape('zombie-left.gif')
        elif self.direction == 'right':
            dx = 24
            dy = 0
            self.shape('zombie-right.gif')

        # check if player is near
        if self.distance(player) < (difficulty * 100):
            if player.xcor() < self.xcor():
                self.direction = 'left'

            elif player.xcor() > self.xcor():
                self.direction = 'right'

            elif player.ycor() < self.ycor():
                self.direction = 'down'

            elif player.ycor() > self.ycor():
                self.direction = 'up'

        # move enemy
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # check for collisions
        check = check_wall_collision(move_to_x, move_to_y, walls)
        if check:
            self.setposition(move_to_x, move_to_y)
        else:
            # choose a different direction
            self.direction = set_direction()

        # reposition enemies after a certain time has passed
        wn.ontimer(self.change_direction, t=random.randint(100, 300))

    def hide(self):
        hide_sprite(self)


# game status
levelsList = []
walls = []
treasures = []
enemies = []
difficulty = 1

# levels
levelsList.append(level_1)
levelsList.append(level_2)
levelsList.append(level_3)

# functions
def setup_maze(level):
    # for number the given number of rows
    for y in range(len(level)):
        # for number of 'X's in a given row
        for x in range(len(level[y])):
            character = level[y][x]
            # position blocks
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            # mark squares in the position of 'X's in the rows
            if character == 'X':
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == 'P':
                player.setposition(screen_x, screen_y)

            if character == 'T':
                treasures.append(Treasure(screen_x, screen_y))

            if character == 'E':
                enemies.append(Zombie(screen_x, screen_y))


def collision_check(sprite1, sprite2, block_size):
    global difficulty
    if sprite2.distance(sprite1) < block_size:
        if sprite2.name == 'Treasure':
            sprite1.gold += sprite2.gold
            sprite2.hide()
            difficulty += 1
            treasures.remove(sprite2)
        if sprite2.name == 'Zombie':
            sprite1.hide()
            print("Player with {} Diamond was killed by a Zombie! GAME OVER!".format(player.gold))


def start_enemies_moving(t):
    for enemy in enemies:
        wn.ontimer(enemy.change_direction, t=t)


def set_direction():
    return random.choice(['up', 'down', 'left', 'right'])


def hide_sprite(sprite):
    sprite.setposition(2000, 2000)
    sprite.hideturtle()

def display_game_over():
    game_over_screen.clear()
    game_over_screen.write("Game Over! Score: {}".format(player.gold), align="center", font=("Arial", 24, "bold"))

def check_wall_collision(next_x, next_y, object_list):
    if (next_x, next_y) not in object_list:
        return True
    else:
        return False


# Create a main menu screen
menu_turtle = turtle.Turtle()
menu_turtle.hideturtle()
menu_turtle.penup()
menu_turtle.color("black")
menu_turtle.goto(0, 100)
menu_turtle.write("Select Level:", align="center", font=("Arial", 24, "bold"))
menu_turtle.goto(0, 50)
menu_turtle.write("1. Easy", align="center", font=("Arial", 16, "normal"))
menu_turtle.goto(0, 0)
menu_turtle.write("2. Medium", align="center", font=("Arial", 16, "normal"))
menu_turtle.goto(0, -50)
menu_turtle.write("3. Hard", align="center", font=("Arial", 16, "normal"))

# Set up levels
levelsList = [level_1, level_2, level_3]
selected_level = None

# Function to select level
def select_level(level):
    global selected_level
    selected_level = level
    menu_turtle.clear()
    menu_turtle.goto(0, 100)
    menu_turtle.write("Level {} selected!".format(level + 1), align="center", font=("Arial", 24, "bold"))

# Bindings for level selection
wn.listen()
wn.onkeypress(lambda: select_level(0), "1")
wn.onkeypress(lambda: select_level(1), "2")
wn.onkeypress(lambda: select_level(2), "3")

# class instances
pen = Pen()
player = Player()

def select_level(level):
    global selected_level
    selected_level = level
    menu_turtle.clear()
    menu_turtle.goto(0, 100)
    # Start the game after level selection
    start_game()

# Function to start the game
def start_game():
    global selected_level
    # Clear existing maze and setup the selected level
    walls.clear()
    treasures.clear()
    enemies.clear()
    pen.clear()
    setup_maze(levelsList[selected_level])
    # Update level display
    level_turtle.clear()
    level_turtle.goto(-250, 300)
    level_turtle.write("Level: {}".format(selected_level + 1), align="left", font=("Arial", 16, "bold"))
    # Start enemies moving after a given timer
    start_enemies_moving(250)
    # Set up keyboard bindings
    wn.listen()
    wn.onkeypress(player.move_up, "Up")
    wn.onkeypress(player.move_down, "Down")
    wn.onkeypress(player.move_left, "Left")
    wn.onkeypress(player.move_right, "Right")
    # Main loop
    while True:
        # Check player and treasure collision
        for treasure in treasures:
            collision_check(player, treasure, grid_block_size)
        # Check player and enemy collision
        for enemy in enemies:
            collision_check(player, enemy, grid_block_size)
        # Update screen
        wn.update()

# Bindings for level selection
wn.listen()
wn.onkeypress(lambda: select_level(0), "1")
wn.onkeypress(lambda: select_level(1), "2")
wn.onkeypress(lambda: select_level(2), "3")

# Run the main loop
wn.mainloop()