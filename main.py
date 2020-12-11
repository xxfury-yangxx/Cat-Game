import random
import math
import pygame
from pygame import mixer

pygame.init()  # initialises pygame starts it
# it creates the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background2.png")
# Sound
mixer.music.load("background2.wav")
mixer.music.play(-1)
# Caption and icon
pygame.display.set_caption("Ming Yang's Cat Game")
icon = pygame.image.load("star.png")
pygame.display.set_icon(icon)

# Creation of Player
playerImage = pygame.image.load("player2.png")
playerX = 370  # starting positions of player
playerY = 480
playerX_change = 0  # value changes later to move it

# Enemy
enemyX = []
enemyY = []
enemyImage = [pygame.image.load("cat.png"),pygame.image.load("cat1.png"),pygame.image.load("cat2.png"),pygame.image.load("cat.png"),pygame.image.load("cat1.png"),pygame.image.load("enemy.png")]
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemyX.append(random.randint(0, 750))  # starting positions of enemy randomised
    enemyY.append(random.randint(25, 100))
    enemyX_change.append(4)  # value changes later to move it
    enemyY_change.append(40)

# Bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 2  # value changes later to move it
bulletY_change = 7.5
bullet_state = "ready"  # ready state means ready to fire ,fired means it is shot

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Functions for  game
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))  # put player into location


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  # Global keyword is used inside a function only when we want to change a variable
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop it makes the game run all the things inside the loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # iterates through all the inputs/events  and determines the action
        if event.type == pygame.QUIT:
            running = False  # if the exit button is pressed then game will close

        if event.type == pygame.KEYDOWN:  # when button is pressed
            if event.key == pygame.K_LEFT:  # when left button is pressed down, player will move to the left
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # can only shoot when bullet has
                    bulletSound = mixer.Sound("laser2.wav")
                    bulletSound.play()
                    bulletX = playerX  # so that bullet doesnt move horizontally tgt w/ player
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # when key is released stop moving
                playerX_change = 0

    playerX += playerX_change  # updates new player location at end of loop
    # setting boundary for where player can move
    if playerX <= 0:
        playerX = 0
    elif playerX >= 739:
        playerX = 739
    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 751:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(25, 100)
            score_value += 1
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= -20:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # updates the changes to be shown on screen based on inputs
