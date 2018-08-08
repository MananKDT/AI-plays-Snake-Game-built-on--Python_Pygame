import pygame
import random
import pickle
pygame.init()

white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,155,0)

display_width = 800
display_height = 600

clock = pygame.time.Clock()
image = pygame.image.load("snakehead.png")
appleimg = pygame.image.load("apple.png")

block_size = 20
FPS = 10

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Death Valley')
icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon)

def pause():
    paused = True
    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue or Q to quit.",black,25)
    pygame.display.update()
        
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        clock.tick(5)

def high_score(highscore):
    text = smallfont.render("HighScore: "+str(highscore), True, black)
    gameDisplay.blit(text, (625,0))
        
def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, (0,0))

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-block_size)/block_size)*block_size
    randAppleY = round(random.randrange(0, display_height-block_size)/block_size)*block_size
    return randAppleX,randAppleY

def game_intro():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Death Valley",
                          green,
                          -100,
                          "medium")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)        
        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit",
                          black,
                          180)
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakelist, direction):

    if direction == "right":
        head = pygame.transform.rotate(image, 270)

    elif direction == "left":
        head = pygame.transform.rotate(image, 90)

    elif direction == "down":
        head = pygame.transform.rotate(image, 180)

    elif direction == "up":
        head = image
        
    gameDisplay.blit(head, [snakelist[-1][0], snakelist[-1][1]])
    for XnY in snakelist[:-1]: 
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)

    elif size == "medium":
        textSurface = medfont.render(text, True, color)

    elif size == "large":
        textSurface = largefont.render(text, True, color)
        
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    gameExit = False
    gameOver = False
    
    lead_x = display_width/2
    lead_y = display_height/2
    
    lead_x_change = block_size
    lead_y_change = 0

    randAppleX,randAppleY = randAppleGen()

    pickle_in = open("highscore.pickle","rb")
    highscore = pickle.load(pickle_in)

    snakeList = []
    snakeLength = 1
    direction = "right"
    
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game Over",
                              red,
                              y_displace=-50,
                              size="large")
            
            message_to_screen("Prees C to play again or Q to quit",
                              black,
                              50,
                              size="medium")
            pygame.display.update()

        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
                    if event.key == pygame.K_c:
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
        
        if lead_x >= display_width or lead_x<0 or lead_y >=display_height or lead_y<0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.fill(white)
        gameDisplay.blit(appleimg, (randAppleX, randAppleY)) 
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        snake(block_size, snakeList, direction)
        score(snakeLength-1)
        
        if snakeLength-1 > highscore:
            highscore = snakeLength-1
            pickle_out = open("highscore.pickle","wb")
            pickle.dump(highscore,pickle_out)
            pickle_out.close()

        high_score(highscore)
        
        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX,randAppleY = randAppleGen()
            snakeLength += 1
        clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()
gameLoop()
