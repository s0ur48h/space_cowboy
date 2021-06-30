#This is space invader game
import random
import math
import pygame

from pygame import mixer



# intialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800,600))

#background image
background = pygame.image.load("background.png")
running = True


# background sound 
mixer.music.load("background.wav")
mixer.music.play(-1)
# title and icon 
pygame.display.set_caption("Space cowboy")
icon_var = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon_var)

#player image
playerImg = pygame.image.load("space-invaders.png")
playerX = 380
playerY = 520

# chaging postion of player
playerX_change = 0
playerY_change = 0


# Enemies image
#player image
enemyImg = []
enemyX = []
enemyY= []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 700))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)
   
# bullet Image 
# bullet state = "ready",you can't see the bullet 
# bullet state = "fire", bullet is moving
bulletImg = pygame.image.load("bullets.png")
bulletX = 0
bulletY = 480
bulletX_change =0
bulletY_change = 10

bullet_state = "ready"


#scoreboard 
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# game over text

over_font = pygame.font.Font("freesansbold.ttf", 70)

def show_score(x, y):
    score = font.render("Score:" + str(score_value),True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_test():
    over_text = over_font.render("GAME OVER",True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False



# Game loop


while running:

    #  RGB = red, green, blue
    screen.fill((0, 0, 0))
    # persistant background image
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running= False
# if  keystroke is pressed check weather its RIGHT or LEFT or UP or DOWN 
        if event.type == pygame.KEYDOWN:
            #print("a key stroke is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            #    print("Left arrow is pressed")
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            #    print("Right arrow is pressed")
            elif event.key == pygame.K_UP:
                playerY_change = -5
             #   print("UP arrow is pressed")
            elif event.key == pygame.K_DOWN:
                playerY_change = 5
            #    print("DOWN arrow is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                fire_bullet(bulletX,bulletY)
             #   print("space bar is print initiate bulllet fire animation")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
             #   print("Key stroke has been released")
                playerX_change = 0
                playerY_change = 0

    # player boundries limit
    # X axis
    playerX  += playerX_change
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 740:
        playerX = 740

    # y axis
    playerY  += playerY_change
    if playerY <=0 :
        playerY = 0
    elif playerY >= 540:
        playerY = 540
    
    # enemy bounderies 
    # x axis
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_test()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 :
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 740:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i] 
        #collisoin    
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 700)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    
    # bullet movement
    if bulletY <= 0 :
        bulletY =480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    

    player(playerX,playerY)

    show_score(textX, textY)
    
    # update method  allows me to constantly update whatever is in the game 
    pygame.display.update()
