import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
pygame.init()

font=pygame.font.SysFont('arial.ttf',25)
class Direction(Enum):
    Right=1
    Left=2
    UP=3
    Down=4

Point = namedtuple('Point', 'x, y')

WHITE=(255,255,255)
RED=(200,0,0)
BLUE1=(0,0,255)
BLUE2=(0,100,255)
BLACK=(0,0,0)
GREEN1=(0,255,15)
GREEN2=(0,200,25)

BLOCK_SIZE=20
SPEED=50

class SnakeGame:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h
        self.display = pygame.display.set_mode((w,h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):

        self.direction = Direction.Right
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-(2*BLOCK_SIZE),self.head.y)] #array with 3 points
        self.score = 0
        self.food=None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self,action):

        global SPEED

        self.frame_iteration +=1
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                quit()

        self._move(action)
        self.snake.insert(0,self.head)
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration >100*len(self.snake):
            game_over = True
            reward = -10
            return reward,game_over,self.score


        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10

            return reward,game_over,self.score

        if self.head == self.food:
            self.score+=1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return reward,game_over,self.score

    def is_collision(self,pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x <0 or pt.y > self.h - BLOCK_SIZE or pt.y<0:
            return True
        if pt in self.snake[1:]:
            return True
        return False
    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,GREEN2,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,GREEN1,pygame.Rect(pt.x+4,pt.y+4,12,12))   #inside rectangle

        pygame.draw.rect(self.display,BLUE1,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text=font.render("Score:"+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()


    def _move(self,action):

        clock_wise = [Direction.Right,Direction.Down,Direction.Left,Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action,[0,1,0]):
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x=self.head.x
        y=self.head.y
        if self.direction == Direction.Right:
            x+=BLOCK_SIZE
        elif self.direction == Direction.Left:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y-=BLOCK_SIZE
        elif self.direction==Direction.Down:
            y+=BLOCK_SIZE

        self.head=Point(x,y)





