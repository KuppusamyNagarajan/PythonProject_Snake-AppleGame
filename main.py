import pygame
from pygame.locals import *
import time
import random

SIZE = 20
BACKGROUND_COLOR = (3, 252, 24)

class Apple:
    def __init__(self, parent_screen): #This is the constructor method.It is called automatically when an instance of the Apple class is created.
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self): #draw apple
         self.parent_screen.blit(self.image, (self.x, self.y))
         pygame.display.flip()  # updates the display

    def move(self): #moving the apple to a new random location
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()  #imageload
        self.block.fill((30, 99, 156)) #blockcolor
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down' #Stores the initial direction of the snake’s movement

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self): #drawing the snake
         #self.parent_screen.fill((212, 214, 208))
         for i in range(self.length):
          self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
         pygame.display.flip() #Updates the display so that the drawn snake is visible.

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self): #moving the snake

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1] #Each segment of the snake takes the position of the segment in front of it.
            self.y[i] = self.y[i-1] #Previous block positions

        if self.direction == 'left':
            self.x[0] = self.x[0]-SIZE
        if self.direction == 'right':
            self.x[0] = self.x[0]+SIZE
        if self.direction == 'up':
            self.y[0] = self.y[0]-SIZE
        if self.direction == 'down':
            self.y[0] = self.y[0]+SIZE

        self.draw()
class Game:
    def __init__(self):
        pygame.init() #Initialize the pygame module
        pygame.display.set_caption("Snake and Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((800, 600))  #create the display with size(width,height)
        self.render_background()
        #self.surface.fill((BACKGROUND_COLOR))  # for backgroundcolors
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.paused = False
    def is_collision(self, x1, y1, x2, y2): #Checks whether the snake's head has collided with the apple
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #Snake eating apple scenario
        for i in range(self.snake.length):
         if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move() #Move the apple to a new position if the snake eats it

        #Snake colliding with itself
        for i in range(1, self.snake.length):  # snake colliding with itself
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
             self.play_sound('crash')
             raise "Hit the boundry error"
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (168, 52, 50))
        self.surface.blit(score,(650,10))

    def display_pause_message(self):
        font = pygame.font.SysFont('arial', 50)
        pause_message = font.render("Game Paused", True, (168, 52, 50))
        self.surface.blit(pause_message, (150, 200))
        pygame.display.flip()

    def show_game_over(self):
        self.render_background()
        #self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is Over! Your score is {self.snake.length}", True, (168, 52, 50))
        self.surface.blit(line1, (150, 200))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (168, 52, 50))
        self.surface.blit(line2, (150, 250))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


    def run(self):
        running = True #Initializes a flag that controls the main game loop.
        pause = False

        while running: #The loop listens for user inputs like key presses or the quit event.
            for event in pygame.event.get():  #get events from the queue
                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:  #Escape key
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_SPACE:  # Spacebar to pause/unpause the game
                        pause = not pause  # Toggle the pause state
                        if pause:
                            pygame.mixer.music.pause()
                            self.display_pause_message()
                        else:
                            pygame.mixer.music.unpause()

                    if not pause:
                       if event.key == K_UP:
                        self.snake.move_up()
                       if event.key == K_DOWN:
                        self.snake.move_down()
                       if event.key == K_LEFT:
                        self.snake.move_left()
                       if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:  #Quit
                        running = False
            try:
                if not pause:
                 self.play()  #updates the game state by moving the snake and checking for collisions.
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.1)  #Pauses the loop for 0.3 seconds to control the speed of the game

if __name__ == "__main__":
    game = Game() #obj creation for game class
    game.run()




