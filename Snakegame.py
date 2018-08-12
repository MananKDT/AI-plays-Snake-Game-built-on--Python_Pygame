import pygame
import random
import pickle
import numpy as np
import math

if __name__ == '__main__':
##    from Snakegame_nn import SnakeNN
##    gg = SnakeNN()
##    model = gg.model()
##    model.load('snake_nn.tflearn')
    pygame.init()

    white=(255,255,255)
    black=(0,0,0)
    red=(255,0,0)
    green=(0,155,0)
    FPS = 10

    clock = pygame.time.Clock()
    image = pygame.image.load("snakehead.png")
    appleimg = pygame.image.load("apple.png")

    smallfont = pygame.font.SysFont("comicsansms", 25)
    medfont = pygame.font.SysFont("comicsansms", 50)
    largefont = pygame.font.SysFont("comicsansms", 80)

    pygame.display.set_caption('Death Valley')
    icon = pygame.image.load("apple.png")
    pygame.display.set_icon(icon)

class snakegame:
    def __init__(self, display_width = 800, display_height = 600, block_size = 20, gameOver = False, steps = math.inf ):
        self.display_width = display_width
        self.display_height = display_height
        self.block_size = block_size
        self.steps = steps
        self.gameOver = gameOver

    def start(self):
        self.snakeList = np.array([[self.display_width/2,self.display_height/2],[self.display_width/2+self.block_size,self.display_height/2]])
        self.randAppleGen()
        self.snakeLength = 2
        self.score = 0
        return self.generate_observations()
    
    def pause(self):
        paused = True
        self.message_to_screen("Paused",black,-100,size="large")
        self.message_to_screen("Press C to continue or Q to quit.",black,25)
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
            
            clock.tick(15)

    def high_score(self, highscore):
        if self.snakeLength-1 > highscore:
            highscore = snakeLength-1
            pickle_out = open("highscore.pickle","wb")
            pickle.dump(highscore,pickle_out)
            pickle_out.close()
    
        text = smallfont.render("HighScore: "+str(highscore), True, black)
        gameDisplay.blit(text, (self.display_width-175,0))
            
    def show_score(self):
        text = smallfont.render("Score: "+str(self.score), True, black)
        gameDisplay.blit(text, (0,0))

    def randAppleGen(self):
        self.Apple = []
        self.Apple.append(round(random.randrange(0, self.display_width-self.block_size)/self.block_size)*self.block_size)
        self.Apple.append(round(random.randrange(0, self.display_height-self.block_size)/self.block_size)*self.block_size)
        for eachsegment in self.snakeList:
            if self.Apple[0] == eachsegment[0] and self.Apple[1] == eachsegment[1]:
                self.randAppleGen()

    def game_intro(self):
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
            self.message_to_screen("Welcome to Death Valley",
                              green,
                              -100,
                              "medium")
            self.message_to_screen("The objective of the game is to eat red apples",
                              black,
                              -30)
            self.message_to_screen("The more apples you eat, the longer you get",
                              black,
                              10)        
            self.message_to_screen("If you run into yourself, or the edges, you die!",
                              black,
                              50)
            self.message_to_screen("Press C to play, P to pause or Q to quit",
                              black,
                              180)
            pygame.display.update()
            clock.tick(15)

    def snake(self):
        direction = (self.snakeList[-1]-self.snakeList[-2])/self.block_size
        if not any(direction - [1,0]):
            head = pygame.transform.rotate(image, 270)

        elif not any(direction - [-1,0]):
            head = pygame.transform.rotate(image, 90)

        elif not any(direction - [0,1]):
            head = pygame.transform.rotate(image, 180)

        else :
            head = image
            
        gameDisplay.blit(head, [self.snakeList[-1][0], self.snakeList[-1][1]])
        for XnY in self.snakeList[:-1]: 
            pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],self.block_size,self.block_size])

    def text_objects(self, text, color, size):
        if size == "small":
            textSurface = smallfont.render(text, True, color)

        elif size == "medium":
            textSurface = medfont.render(text, True, color)

        elif size == "large":
            textSurface = largefont.render(text, True, color)
            
        return textSurface, textSurface.get_rect()

    def message_to_screen(self, msg, color, y_displace = 0, size = "small"):
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = (self.display_width/2), (self.display_height/2)+y_displace
        gameDisplay.blit(textSurf, textRect)

    def move_from_keyboard(self):
        direction = (self.snakeList[-1]-self.snakeList[-2])/self.block_size
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause()
                elif (direction == [0,1]).all():
                    if event.key == pygame.K_LEFT:
                        return self.step(3)
                    elif event.key == pygame.K_RIGHT:
                        return self.step(1)
                elif not any(direction - [1,0]):
                    if event.key == pygame.K_UP:
                        return self.step(0)
                    elif event.key == pygame.K_DOWN:
                        return self.step(2)
                elif not any(direction - [0,-1]):
                    if event.key == pygame.K_LEFT:
                        return self.step(3)
                    elif event.key == pygame.K_RIGHT:
                        return self.step(1)
                elif not any(direction - [-1,0]):
                    if event.key == pygame.K_UP:
                        return self.step(0)
                    elif event.key == pygame.K_DOWN:
                        return self.step(2)
        
        if (direction == [0,1]).all():
            return self.step(2)
        elif (direction == [0,-1]).all():
            return self.step(0)
        elif (direction == [1,0]).all():
            return self.step(1)
        elif (direction == [-1,0]).all():
            return self.step(3)

    def step(self,action):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        
        if action == 0 :
            self.snakeList = np.append(self.snakeList,[[self.snakeList[-1][0],self.snakeList[-1][1]-self.block_size]],axis=0)
        elif action == 1:
            self.snakeList = np.append(self.snakeList,[[self.snakeList[-1][0]+self.block_size,self.snakeList[-1][1]]],axis=0)
        elif action == 2:
            self.snakeList = np.append(self.snakeList,[[self.snakeList[-1][0],self.snakeList[-1][1]+self.block_size]],axis=0)
        elif action == 3:
            self.snakeList = np.append(self.snakeList,[[self.snakeList[-1][0]-self.block_size,self.snakeList[-1][1]]],axis=0)
        if len(self.snakeList) > self.snakeLength:
            self.snakeList = np.delete(self.snakeList,0,axis=0)
        if self.snakeList[-1][0] == self.Apple[0] and self.snakeList[-1][1] == self.Apple[1]:
            self.randAppleGen()
            self.snakeLength += 1
            self.score += 1
        self.check_collision()
        return self.generate_observations()

    def generate_observations(self):
        return self.gameOver,self.score,self.snakeList,self.Apple

    def check_collision(self):
        if self.snakeList[-1][0] >= self.display_width or self.snakeList[-1][0]<0 or self.snakeList[-1][1]>=self.display_height or self.snakeList[-1][1]<0:
            self.gameOver = True
        for eachSegment in self.snakeList[:-1]:
            if not any(eachSegment - self.snakeList[-1]):
                self.gameOver = True
                
    def gameLoop(self):
        self.gameExit = False
        self.gameOver = False

        pickle_in = open("highscore.pickle","rb")
        highscore = pickle.load(pickle_in)

        self.start()
        step = self.steps
        
        while not self.gameExit:

            if self.gameOver == True:
                self.message_to_screen("Game Over",
                                  red,
                                  y_displace=-50,
                                  size="large")
                
                self.message_to_screen("Prees C to play again or Q to quit",
                                  black,
                                  50,
                                  size="medium")
                pygame.display.update()

            while self.gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameExit = True
                        self.gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.gameOver = False
                            self.gameExit = True
                        if event.key == pygame.K_c:
                            self.gameLoop()                           
            if __name__ == '__main__':
                self.move_from_keyboard()
##                prev_observation = gg.generate_observation(self.snakeList, self.Apple)
##                predictions = []
##                for action in range(-1, 2):
##                   predictions.append(model.predict(gg.add_action_to_observation(prev_observation, action).reshape(-1, 5, 1)))
##                action = np.argmax(np.array(predictions))
##                game_action = gg.get_game_action(self.snakeList, action - 1)
##                done, score, snake, Apple  = self.step(game_action)
            gameDisplay.fill(white)
            gameDisplay.blit(appleimg, (self.Apple[0], self.Apple[1])) 
            self.snake()
            self.show_score()
            self.high_score(highscore)
            self.check_collision()
            step -= 1
            if step <= 0:
                self.gameOver = True
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
        quit()    
if __name__ == '__main__':        
    s = snakegame()
    gameDisplay = pygame.display.set_mode((s.display_width, s.display_height))
    s.game_intro()
    s.gameLoop()
