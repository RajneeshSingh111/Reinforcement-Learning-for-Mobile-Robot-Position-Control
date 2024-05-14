import pygame
import numpy as np
import math

pygame.init() # initialising pygame
# screen size
xlim = 400
ylim = 300
screen = pygame.display.set_mode((xlim, ylim))

# caption and icon
pygame.display.set_caption("Mobile Robot")
icon = pygame.image.load('robot.png')
pygame.display.set_icon(icon)

# robot
roversize = 32
robotImg = pygame.image.load('rover.png')
posX = math.floor((xlim - roversize) * np.random.rand())
posY = math.floor((ylim - roversize) * np.random.rand())
pos_Xchange = 0
pos_Ychange = 0
speed = 2  # speed of the robot
direction = np.array([1, 0, 0, 0])   # initial direction of the robot


def robot(x,y):
    screen.blit(robotImg, (x, y))

# obstacle list(as there can be many obstacles)
obstaclesize = 32
obstacleImg =[]
posXobs = []
posYobs = []
nobs = 1   # no. of obstacles
num_steps = 0   # initially the number of steps taken by the robot = 0

for i in range(nobs):
    obstacleImg.append(pygame.image.load('obstacle.png'))
    posXobs.append(math.floor((xlim - obstaclesize) * np.random.rand()))
    posYobs.append(math.floor((ylim - obstaclesize) * np.random.rand()))


def obstacle(i):
    screen.blit(obstacleImg[i], (posXobs[i], posYobs[i]))

#destination
destinationsize = 32
destinationImg = pygame.image.load('destination.png')
posXdes = math.floor((xlim - destinationsize) * np.random.rand())
posYdes = math.floor((ylim - destinationsize) * np.random.rand())
# To avoid the spawn of obstacle and destination at the same location
verify = True
while verify:
    if ((min((math.pow((math.pow((posXdes - posXobs[i]), 2)) + (math.pow((posYdes - posYobs[i]), 2)), 0.5)) for i in range(nobs)) <= 46) or (min(math.pow((math.pow((posX - posXobs[i]), 2)) + (math.pow((posY - posYobs[i]), 2)), 0.5)for i in range(nobs)) <= 46)):
        posXdes = math.floor((xlim - destinationsize) * np.random.rand()) + destinationsize / 2
        posYdes = math.floor((ylim - destinationsize) * np.random.rand()) + destinationsize / 2
        posX = math.floor((xlim - roversize) * np.random.rand()) + roversize / 2
        posY = math.floor((ylim - roversize) * np.random.rand()) + roversize / 2
    else:
        verify = False


def destination():
    screen.blit(destinationImg, (posXdes, posYdes))
deflect = 32   # this happens when robot collides with obstacle
running = True
while running:
    num_steps += 1    # incrementing the steps taken by the robot
    screen.fill((173, 98, 66))
    vl = math.pow(-1, np.random.choice([0, 1])) * speed * np.random.rand()  # random speed for left wheel
    vr = math.pow(-1, np.random.choice([0, 1])) * speed * np.random.rand()  # random speed for right wheel
    # defining the actions
    if (vl == vr) and vr >= 0:
        if direction[0] == 1:
            pos_Xchange = (vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([1, 0, 0, 0])
        elif direction[1] == 1:
            pos_Xchange = 0
            pos_Ychange = (vl + vr) / 2
            direction = np.array([0, 1, 0, 0])
        elif direction[2] == 1:
            pos_Xchange = -(vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([0, 0, 1, 0])
        else:
            pos_Xchange = 0
            pos_Ychange = -(vl + vr) / 2
            direction = np.array([0, 0, 0, 1])
    elif (vl == vr) and vr <= 0:
        if direction[0] == 1:
            pos_Xchange = -(vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([0, 0, 1, 0])
        elif direction[1] == 1:
            pos_Xchange = 0
            pos_Ychange = -(vl + vr) / 2
            direction = np.array([0, 0, 0, 1])
        elif direction[2] == 1:
            pos_Xchange = (vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([1, 0, 0, 0])
        else:
            pos_Xchange = 0
            pos_Ychange = (vl + vr) / 2
            direction = np.array([0, 1, 0, 0])
    elif vl > vr:
        if direction[0] == 1:
            pos_Xchange = 0
            pos_Ychange = (vl + vr) / 2
            direction = np.array([0, 1, 0, 0])
        elif direction[1] == 1:
            pos_Xchange = -(vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([0, 0, 1, 0])
        elif direction[2] == 1:
            pos_Xchange = 0
            pos_Ychange = -(vl + vr) / 2
            direction = np.array([0, 0, 0, 1])
        else:
            pos_Xchange = (vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([1, 0, 0, 0])
    else:
        if direction[0] == 1:
            pos_Xchange = 0
            pos_Ychange = -(vl + vr) / 2
            direction = np.array([0, 0, 0, 1])
        elif direction[1] == 1:
            pos_Xchange = (vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([1, 0, 0, 0])
        elif direction[2] == 1:
            pos_Xchange = 0
            pos_Ychange = (vl + vr) / 2
            direction = np.array([0, 1, 0, 0])
        else:
            pos_Xchange = -(vl + vr) / 2
            pos_Ychange = 0
            direction = np.array([0, 0, 1, 0])

    for i in range(nobs):
        obstacle(i)

    # defining the state after collision with the obstacle
    for i in range(nobs):
        if (posX > posXobs[i] - deflect and posX < posXobs[i] + deflect) and (posY > posYobs[i] - deflect and posY < posYobs[i] + deflect):
            if (posX > posXobs[i]) and (posY > posYobs[i]):
                posX = posXobs[i] + deflect
                posY = posYobs[i] + deflect
            elif (posX > posXobs[i]) and (posY < posYobs[i]):
                posX = posXobs[i] + deflect
                posY = posYobs[i] - deflect
            elif (posX < posXobs[i]) and (posY > posYobs[i]):
                posX = posXobs[i] - deflect
                posY = posYobs[i] + deflect
            else:
                posX = posXobs[i] - deflect
                posY = posYobs[i] - deflect
    posX += pos_Xchange   # changing the x coordinate of the robot
    posY += pos_Ychange        # changing the y coordinate of the robot
    # conditions such that the robot remains within the frame
    if posX <= 0:
        posX = 0
    elif posX >= (xlim - roversize):
        posX = xlim - roversize
    if posY <= 0:
        posY = 0
    elif posY >= (ylim - roversize):
        posY = ylim - roversize
    robot(posX, posY)
    destination()
    pygame.display.update()
    if (posX > posXdes - roversize and posX < posXdes + destinationsize) and (posY > posYdes - roversize and posY < posYdes + destinationsize):
        running = False  # stopping the programme when the destination is reached
print('The number of steps taken by the robot is ', num_steps)
