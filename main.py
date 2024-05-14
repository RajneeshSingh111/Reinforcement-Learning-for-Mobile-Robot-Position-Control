import pygame
import numpy as np
import math
import random
import pickle

pygame.init()

# screen size
xlim = 400
ylim = 300

# caption and icon
pygame.display.set_caption("Mobile Robot")
icon = pygame.image.load('robot.png')
pygame.display.set_icon(icon)

# sizes
roversize = 32
destinationsize = 32
obstaclesize = 32

# deciding parameters
speed = 2  # speed of the robot
nobs = 1    # no.of obstacles
# nobs = random.randint(1, 10)  # no. of obstacles
deflect = 32  # this happens when robot collides with obstacle
epsilon = 0.5
num_episodes = 100
steps = np.zeros((1, num_episodes))     # defining an array to store the no. of steps taken by the robot

print('Loading Q-Table')
# loading the trained robot
with open('q_table-10000000.pkl', 'rb') as f:
    q_table = pickle.load(f)


class Mobile_robot:
    def __init__(self, screen):
        self.screen = screen
        self.robotImg = pygame.image.load('rover.png')
        self.posX = math.floor((xlim - roversize) * np.random.rand()) + roversize / 2
        self.posY = math.floor((ylim - roversize) * np.random.rand()) + roversize / 2
        self.destinationImg = pygame.image.load('destination.png')
        self.posXdes = math.floor((xlim - destinationsize) * np.random.rand()) + destinationsize / 2
        self.posYdes = math.floor((ylim - destinationsize) * np.random.rand()) + destinationsize / 2
        self.obstacleImg = []
        self.posXobs = []
        self.posYobs = []
        # introducing the obstacles
        for i in range(nobs):
            self.obstacleImg.append(pygame.image.load('obstacle.png'))
            self.posXobs.append(math.floor((xlim - 4 * obstaclesize) * np.random.rand()) + 2 * obstaclesize)
            self.posYobs.append(math.floor((ylim - 4 * obstaclesize) * np.random.rand()) + 2 * obstaclesize)
        # To avoid the spawn of obstacle and destination at the same location
        verify = True
        while verify:
            if ((min((math.pow((math.pow((self.posXdes - self.posXobs[i]), 2)) + (math.pow((self.posYdes - self.posYobs[i]), 2)),0.5)) for i in range(nobs)) <= 46) or (min((math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)), 0.5))for i in range(nobs)) <= 46)):
                self.posXdes = math.floor((xlim - destinationsize) * np.random.rand()) + destinationsize / 2
                self.posYdes = math.floor((ylim - destinationsize) * np.random.rand()) + destinationsize / 2
                self.posX = math.floor((xlim - roversize) * np.random.rand()) + roversize / 2
                self.posY = math.floor((ylim - roversize) * np.random.rand()) + roversize / 2
            else:
                verify = False

    # A function to draw pygame screen
    def draw(self):
        self.screen.fill((173, 98, 66))
        self.robo_rect = self.robotImg.get_rect(center=(self.posX, self.posY))
        self.screen.blit(self.robotImg, self.robo_rect)
        self.des_rect = self.destinationImg.get_rect(center=(self.posXdes, self.posYdes))
        self.screen.blit(self.destinationImg, self.des_rect)
        for i in range(nobs):
            self.obs_rect = self.obstacleImg[i].get_rect(center=(self.posXobs[i], self.posYobs[i]))
            self.screen.blit(self.obstacleImg[i], self.obs_rect)
        pygame.display.flip()

    # A function to check whether robot has reached it's destination
    def check(self):
        if (math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)), 0.5)) <= 32:
            return False  # stopping the programme when the destination is reached
        else:
            return True

    # Function to control the movement of the robot
    def move(self, x, y):
        self.posX += x
        self.posY += y
        # defining the state after collision with the obstacle
        for i in range(nobs):
            if ((math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)),0.5))) <= 32:
                if (self.posX > self.posXobs[i]) and (self.posY > self.posYobs[i]):
                    self.posX = self.posX + deflect
                    self.posY = self.posY + deflect
                elif (self.posX > self.posXobs[i]) and (self.posY < self.posYobs[i]):
                    self.posX = self.posX + deflect
                    self.posY = self.posY - deflect
                elif (self.posX < self.posXobs[i]) and (self.posY > self.posYobs[i]):
                    self.posX = self.posX - deflect
                    self.posY = self.posY + deflect
                else:
                    self.posX = self.posX - deflect
                    self.posY = self.posY - deflect
        # conditions such that the robot remains within the frame
        if self.posX <= roversize / 2:
            self.posX = roversize / 2
        elif self.posX >= (xlim - roversize / 2):
            self.posX = xlim - roversize / 2
        if self.posY <= roversize / 2:
            self.posY = roversize / 2
        elif self.posY >= (ylim - roversize / 2):
            self.posY = ylim - roversize / 2
        self.draw()

    # Now defining a reward function to give rewards to the robot
    def rewards(self):
        if min((math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)),0.5)) for i in range(nobs)) <= 32:
            output = -1000
        elif (math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)), 0.5)) <= 32:
            output = 2000
        else:
            output = -(math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)), 0.5))
        reward.append(output)
        return output

    # Now defining the function to get the states [[destination distance, destination angle], [nearest obstacle distance, nearest obstacle angle]]
    def get_state(self):
        self.des_distance = math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)), 0.5)
        if (self.posX < self.posXdes and self.posY >= self.posYdes):
            self.des_position = 0
        elif (self.posX <= self.posXdes and self.posY < self.posYdes):
            self.des_position = 1
        elif (self.posX > self.posXdes and self.posY <= self.posYdes):
            self.des_position = 2
        else:
            self.des_position = 3
        # getting the distance to the nearest obstacle and it's position
        self.obs_distance = min(math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)), 0.5) for i in range(nobs))
        for i in range(nobs):
            if math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)),0.5) == self.obs_distance:
                self.index = i
        if (self.posX < self.posXobs[self.index] and self.posY >= self.posYobs[self.index]):
            self.obs_position = 0
        elif (self.posX <= self.posXobs[self.index] and self.posY < self.posYobs[self.index]):
            self.obs_position = 1
        elif (self.posX > self.posXobs[self.index] and self.posY <= self.posYobs[self.index]):
            self.obs_position = 2
        else:
            self.obs_position = 3
        self.destination = (math.floor(self.des_distance), self.des_position)
        self.obstacle = (math.floor(self.obs_distance), self.obs_position)
        return (self.destination, self.obstacle)

    # Now defining the actions right, down, left, up
    def get_action(self, action):
        if action == 0:
            pos_Xchange = speed
            pos_Ychange = -speed
        elif action == 1:
            pos_Xchange = speed
            pos_Ychange = speed
        elif action == 2:
            pos_Xchange = -speed
            pos_Ychange = speed
        else:
            pos_Xchange = -speed
            pos_Ychange = -speed
        return pos_Xchange, pos_Ychange


# A class which will run the simulator
class Run():
    num_steps = 0   # initially the number of steps taken by the robot is 0

    # Initializing
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((xlim, ylim))
        self.screen.fill((173, 98, 66))
        self.robo = Mobile_robot(self.screen)
        self.robo.draw()

    # Executing
    def execute(self):
        running = self.robo.check()
        while running:
            self.num_steps += 1   # increasing the number of steps
            obs = self.robo.get_state()    # getting the current state
            if np.random.random() > epsilon:
                action = np.argmax(q_table[obs])    # EXPLOITATION
            else:
                action = random.randint(0, 3)         # EXPLORATION
            pos_Xchange, pos_Ychange = self.robo.get_action(action)
            self.robo.move(pos_Xchange, pos_Ychange)
            running = self.robo.check()

for i in range(num_episodes):
    reward = []
    simulation = Run()
    simulation.execute()
    steps[0][i] = simulation.num_steps
avg_steps = np.average(steps)   # average steps taken by the robot
print(steps)
print('The average number of steps taken by the robot is ', avg_steps)