import pygame
import numpy as np
import math
import random
from collections import defaultdict
import matplotlib.pyplot as plt
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

# Simulation parameters
speed = 5  # speed of the robot
nobs = random.randint(1, 5)  # no. of obstacles
deflect = 25  # this happens when robot collides with obstacle
num_episodes = 1  # defining the number of episodes

class Mobile_robot:
    # initializing
    def __init__(self, screen):
        self.screen = screen
        self.robotImg = pygame.image.load('rover.png')
        self.posX = math.floor((xlim - roversize) * np.random.rand())
        self.posY = math.floor((ylim - roversize) * np.random.rand())
        self.destinationImg = pygame.image.load('destination.png')
        self.posXdes = math.floor((xlim - destinationsize) * np.random.rand())
        self.posYdes = math.floor((ylim - destinationsize) * np.random.rand())
        self.obstacleImg = []
        self.posXobs = []
        self.posYobs = []
        for i in range(nobs):
            self.obstacleImg.append(pygame.image.load('obstacle.png'))
            self.posXobs.append(math.floor((xlim - obstaclesize) * np.random.rand()))
            self.posYobs.append(math.floor((ylim - obstaclesize) * np.random.rand()))

        # To avoid the spawn of obstacle and destination at the same location
        verify = True
        while verify:
            if ((min((math.pow((math.pow((self.posXdes - self.posXobs[i]), 2)) + (math.pow((self.posYdes - self.posYobs[i]), 2)),0.5)) for i in range(nobs)) <= 46) or (min((math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)), 0.5))for i in range(nobs)) <= 46)):
                self.posXdes = math.floor((xlim - destinationsize) * np.random.rand())
                self.posYdes = math.floor((ylim - destinationsize) * np.random.rand())
                self.posX = math.floor((xlim - roversize) * np.random.rand())
                self.posY = math.floor((ylim - roversize) * np.random.rand())
            else:
                verify = False

    # A function to draw pygame screen
    def draw(self):
        self.screen.fill((173, 98, 66))
        self.screen.blit(self.robotImg, (self.posX, self.posY))
        self.screen.blit(self.destinationImg, (self.posXdes, self.posYdes))
        for i in range(nobs):
            self.screen.blit(self.obstacleImg[i], (self.posXobs[i], self.posYobs[i]))
        pygame.display.flip()

    # A function to check whether robot has reached it's destination
    def check(self):
        if (self.posX >= self.posXdes - roversize and self.posX <= self.posXdes + destinationsize) and (self.posY >= self.posYdes - roversize and self.posY <= self.posYdes + destinationsize):
            return False  # stopping the programme when the destination is reached
        else:
            return True

    # Function to control the movement of the robot
    def move(self, x, y):
        self.posX += x
        self.posY += y
        # defining the state after collision with the obstacle
        for i in range(nobs):
            if (self.posX > self.posXobs[i] - deflect and self.posX < self.posXobs[i] + deflect) and (self.posY > self.posYobs[i] - deflect and self.posY < self.posYobs[i] + deflect):
                if (self.posX > self.posXobs[i]) and (self.posY > self.posYobs[i]):
                    self.posX += deflect
                    self.posY += deflect
                elif (self.posX > self.posXobs[i]) and (self.posY < self.posYobs[i]):
                    self.posX += deflect
                    self.posY -= deflect
                elif (self.posX < self.posXobs[i]) and (self.posY > self.posYobs[i]):
                    self.posX -= deflect
                    self.posY += deflect
                else:
                    self.posX -= deflect
                    self.posY -= deflect
        # conditioning such that the robot remains within the frame
        if self.posX <= 0:
            self.posX = 0
        elif self.posX >= (xlim - roversize):
            self.posX = xlim - roversize
        if self.posY <= 0:
            self.posY = 0
        elif self.posY >= (ylim - roversize):
            self.posY = ylim - roversize
        self.draw()

    # The reward function
    def rewards(self):
        if (math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)),0.5)) <= 32:
            output = 0   # Reward is 0 if the robot reaches close to the destination
        elif min((math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)), 0.5)) for i in range(nobs)) <= 46:
            output = -1000   # Reward is -1000 if the robot collides with the obstacle
        else:
            output = -(math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)),  0.5))
        reward.append(output)  # Otherwise the reward is proportional to the negative of the distance between robot and destination
        return output

    def get_state(self):
        # getting the distance to the destination and it's position
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
        self.obs_distance = min(math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)), 0.5)for i in range(nobs))
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
        self.destination = [math.floor(self.des_distance), self.des_position]
        self.obstacle = [math.floor(self.obs_distance), self.obs_position]
        # state is of the form[[destination distance, destination angle], [nearest obstacle distance, nearest obstacle angle]]
        state = [self.destination, self.obstacle]
        states.append(state)
        return state


# A class which will run the simulator
class Run():
    # Initializing
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((xlim, ylim))
        self.screen.fill((173, 98, 66))
        self.robo = Mobile_robot(self.screen)
        self.robo.draw()

    # Executing the simulator
    def execute(self):
        pos_Xchange = 0    # to store the change in x-coordinate of the robot
        pos_Ychange = 0     # to store the change in y-coordinate of the robot
        running = self.robo.check()
        while running:
            robostate = self.robo.get_state()    # getting the current state
            action = random.randint(0, 3)        # choosing a random action
            actions.append(action)
            # defining the actions
            if action == 0:
                pos_Xchange = np.random.uniform() * speed
                pos_Ychange = -np.random.uniform() * speed
            elif action == 1:
                pos_Xchange = np.random.uniform() * speed
                pos_Ychange = np.random.uniform() * speed
            elif action == 2:
                pos_Xchange = -np.random.uniform() * speed
                pos_Ychange = np.random.uniform() * speed
            else:
                pos_Xchange = -np.random.uniform() * speed
                pos_Ychange = -np.random.uniform() * speed
            self.robo.move(pos_Xchange, pos_Ychange)    # updating the robot's position
            result = self.robo.rewards()    # storing the reward
            running = self.robo.check()   # to check whether robot has reached destination

# The main method
for i in range(num_episodes):
    reward = []     # the reward array
    states = []      # the state array
    actions = []  # the action array
    merged_dictionary = defaultdict(list)
    simulation = Run()        # creating a run variable for simulation
    simulation.execute()             # executing the simulation
    #print(reward)
    #print(states)
    #print(actions)
    for stage in range(len(reward)):
        merged_dictionary['STATE ', stage + 1].append(states[stage])
        merged_dictionary['ACTION ', stage + 1].append(actions[stage])
        merged_dictionary['REWARD ', stage + 1].append(reward[stage])
    Simulation_result = dict(merged_dictionary)   # This is the result obtained from the simulation or the sample run
    print(Simulation_result)
    print(f'Episode {i + 1} : {np.sum(reward)}')
    fig, ax = plt.subplots()
    ax.plot(reward)
    ax.set_title("REWARDS")
    ax.set_xlabel("STEPS")
    ax.set_ylabel("OBTAINED REWARD")
    plt.show()