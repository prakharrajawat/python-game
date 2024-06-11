# In Alien Invasion, the player controls a ship that appears at 
# the bottom center of the screen. The player can move the ship 
# right and left using the arrow keys and shoot bullets using the 
# spacebar. When the game begins, a fleet of aliens fills the sky 
# and moves across and down the screen. The player shoots and 
# destroys the aliens. If the player shoots all the aliens, a new fleet 
# appears that moves faster than the previous fleet. If any alien hits 
# the player’s ship or reaches the bottom of the screen, the player 
# loses a ship. If the player loses three ships, the game ends.

import pygame
import random
import math
from pygame import mixer
# Initializing pygame
pygame.init()

# Adding height and width
screen = pygame.display.set_mode((800,600))


# Adding icon and logo 
pygame.display.set_caption("Alien Invasion")
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)

# Adding Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)


# Player
playerImg = pygame.image.load('player1.png')
playerX=370
playerY=480
playerXChange=0
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

game_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
  score = font.render("Score :"+str(score_value),True,(255,255,255))
  screen.blit(score,(x,y))

def game_over_text():
  game_over = game_font.render("GAME OVER",True,(255,255,255))
  screen.blit(game_over,(200,250))
  
def player(x,y):
  screen.blit(playerImg,(x,y))

# Enemy
enemyImg = []
enemyX=[]
enemyY=[]
enemyXChange =[]
enemyYChange =[]
enemy_count=6

  
for i in range(enemy_count):
  enemyImg.append(pygame.image.load('retro.png'))
  enemyX.append(random.randint(0,800))
  enemyY.append(random.randint(50,150))
  enemyXChange.append(0.3)
  enemyYChange.append(60)
  
def enemy(x,y,i):
  screen.blit(enemyImg[i],(x,y))


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletXChange = 0
bulletYChange =1.2
bullet_state ="ready"

def bullet(x,y):
  global bullet_state
  bullet_state= "fire"
  screen.blit(bulletImg,(x+16,y+14))
  

# Collision of two bullets
def bullet_collision(bulletX,bulletY,enemyX,enemyY):
  distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
  if distance<27:
    return True
  else:
    return False
  
  
  
  


# Game Loop
running = True
while running:
  # RGB - (Red, Green ,Blue) 
  screen.fill((64,64,64))
  
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
  
    # Moving player on keystroke
    if event.type ==pygame.KEYDOWN:
      # For left key pressed 
      if event.key==pygame.K_LEFT:
        playerXChange=-1
      # For right key pressed
      if event.key==pygame.K_RIGHT:
        playerXChange=1
      
      if event.key==pygame.K_SPACE:
        if bullet_state == "ready":
          # Bullet Sound
          bullet_sound=mixer.Sound('laser.wav')
          bullet_sound.play()
          
          bulletX=playerX
          # print("Space entered")
          bullet(bulletX,bulletY)    
            
    if event.type==pygame.KEYUP:
      if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
        playerXChange=0
  
  # For fixing boundery of player so that it could not move outside boundries 
  playerX=playerX+playerXChange  
  if(playerX<0):
    playerX=0
  if(playerX>=736):
    playerX=736    
  
  for i in range(enemy_count):
    
    # Enemy reached to player 
    if(enemyY[i]>=480):
      for j in range(enemy_count):
          enemyY[j]=2000
      game_over_text()
      break
    enemyX[i]=enemyX[i]+enemyXChange[i]  
    if(enemyX[i]<0):
      enemyXChange[i]=0.5
    #  print("reaching x left axis")
      enemyY[i]=enemyY[i]+enemyYChange[i]
    elif enemyX[i]>=740:
    #  print("reaching x axis")
      enemyXChange[i]=-0.4
      # enemyY[i]=enemyY[i]+enemyYChange[i]
    
    collision =bullet_collision(bulletX,bulletY,enemyX[i],enemyY[i])
    if collision:
     collision_sound=mixer.Sound('explosion.wav')
     collision_sound.play()
     bulletY=480
     bullet_state='ready'
     score_value+=1
     enemyX[i]=random.randint(0,736)
     enemyY[i]=random.randint(50,150)
    enemy(enemyX[i],enemyY[i],i) 
    
  # for bullet
  if bulletY<=0:
    bulletY=480
    bullet_state="ready"
  if bullet_state =="fire":
    bullet(bulletX,bulletY)
    bulletY=bulletY-bulletYChange
    
  
  

    # print(score_value)  
    
 

  player(playerX,playerY)
  show_score(textX,textY)

  pygame.display.update()
  

