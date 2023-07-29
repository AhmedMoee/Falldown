

import uvage
import random

# prep work: make the gameboxes to be used later
block = uvage.from_color(100, 100, "purple", 30, 30)
game_over = False
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
score = 0
height_change = 130
floors_left = []
floors_right = []
camera = uvage.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


def wall_environment():
    """

    :return: The walls on the side, Random gap in the floor, Multiple floors
    """
    global height_change, floors_right, floors_left
    walls = [uvage.from_color(0, SCREEN_HEIGHT / 2, "green", 10, SCREEN_HEIGHT),
             uvage.from_color(SCREEN_WIDTH, SCREEN_HEIGHT / 2, "green", 10, SCREEN_HEIGHT)]
    for wall in walls:
        camera.draw(wall)

    lefts = random.randint(60, 700)
    rights = 740 - lefts
    height_change += 100
    if len(floors_left) <= 1000:
        floors_left.append(uvage.from_color(0, height_change, 'black', lefts, 30))
        floors_right.append((uvage.from_color(800, height_change, 'black', rights, 30)))
    for floor in floors_left:
        floor.left = 0
        camera.draw(floor)
        block.move_to_stop_overlapping(floor)
        if game_over:
            floor.speedy = 0
        else:
            floor.speedy -= 0.015
        floor.move_speed()
    for floor in floors_right:
        floor.right = SCREEN_WIDTH
        camera.draw(floor)
        block.move_to_stop_overlapping(floor)
        if game_over:
            floor.speedy = 0
        else:
            floor.speedy -= 0.015
        floor.move_speed()


def movement():
    """

    :return: Movement of the block with arrow keys
    """
    global block, game_over
    block.speedy += 2.8
    if uvage.is_pressing('left arrow'):
        block.x -= 10
    if uvage.is_pressing('right arrow'):
        block.x += 10
    if block.x >= SCREEN_WIDTH:
        block.x = SCREEN_WIDTH
    elif block.x <= 0:
        block.x = 0
    if block.y >= SCREEN_HEIGHT - 14:
        block.speedy = 0.001
        block.y = SCREEN_HEIGHT - 14
    block.move_speed()


def check_stats():
    """

    :return: Score in the top left corner increasing with time
    """
    global score
    if not game_over:
        score += 0.05
    camera.draw("Score:" + str(int(score)), 36, "red", 65, 30)


def tick():
    """

    :return: Combine all helper functions of movement, block, floors, and restart with game over
    """
    global score, camera, game_over, floors_left, floors_right
    camera.clear('white')
    wall_environment()
    movement()
    camera.draw(block)
    check_stats()
    if block.y < -40:
        game_over = True
    if game_over:
        camera.draw(uvage.from_text(400, 200, "GAME OVER!", 50, "Red", bold=False))
        camera.draw(uvage.from_text(400, 300, "(press space to restart)", 25, "Red", bold=False))
        if uvage.is_pressing('space'):
            game_over = False
            block.x = 100
            block.y = 10
            block.speedy = 1
            score = 0
            wall_environment()
    camera.display()  # you almost always want to end this method with this line


uvage.timer_loop(30, tick)
# this line of code will not be reached until after the window is closed
