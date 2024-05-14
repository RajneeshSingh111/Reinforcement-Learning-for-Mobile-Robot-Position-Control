import pygame
import numpy as np
import math
import matplotlib.pyplot as plt
pygame.init()
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
posX = math.floor((xlim - roversize) * np.random.rand())      # x coordinate of the robot
posY = math.floor((ylim - roversize) * np.random.rand())       # y coordinate of the robot
pos_Xchange = 0         # Change in x coordinate
pos_Ychange = 0       # Change in y coordinate
speed = 2
direction = np.array([1, 0, 0, 0])    # Defining the initial direction of the robot


def robot(x, y):
    screen.blit(robotImg, (x, y))

# obstacle
obstaclesize = 32
obstacleImg =[]
posXobs = []
posYobs = []
nobs = 2     # No. of obstacles
distance = []
num_steps = 0    # initially the number of steps taken by the robot is 0

for i in range(nobs):
    obstacleImg.append(pygame.image.load('obstacle.png'))
    posXobs.append(math.floor((xlim - obstaclesize) * np.random.rand()))
    posYobs.append(math.floor((ylim - obstaclesize) * np.random.rand()))


def obstacle(i):
    screen.blit(obstacleImg[i], (posXobs[i], posYobs[i]))

# destination
destinationsize = 32
destinationImg = pygame.image.load('destination.png')
posXdes = math.floor((xlim - destinationsize) * np.random.rand())
posYdes = math.floor((ylim - destinationsize) * np.random.rand())

# To avoid the spawn of obstacle and destination at the same location
verify = True
while verify:
    if ((min((math.pow((math.pow((posXdes - posXobs[i]), 2)) + (math.pow((posYdes - posYobs[i]), 2)), 0.5)) for i in range(nobs)) <= 46) or (min(math.pow((math.pow((posX - posXobs[i]), 2)) + (math.pow((posY - posYobs[i]), 2)), 0.5)for i in range(nobs)) <= 46)):
        posXdes = math.floor((xlim - destinationsize) * np.random.rand()) + destinationsize
        posYdes = math.floor((ylim - destinationsize) * np.random.rand()) + destinationsize
        posX = math.floor((xlim - roversize) * np.random.rand()) + roversize
        posY = math.floor((ylim - roversize) * np.random.rand()) + roversize
    else:
        verify = False


def destination():
    screen.blit(destinationImg, (posXdes, posYdes))


deflect = 25  # this happens when robot collides with obstacle

running = True
while running:
    num_steps += 1
    distance.append(math.pow((math.pow((posX - posXdes), 2)) + (math.pow((posY - posYdes), 2)), 0.5))
    screen.fill((173, 98, 66))
    # Enable below code to control the robot using keys on the keyboard
    '''for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pos_Xchange = -speed
            if event.key == pygame.K_RIGHT:
                pos_Xchange = speed
            if event.key == pygame.K_UP:
                pos_Ychange = -speed
            if event.key == pygame.K_DOWN:
                pos_Ychange = speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                pos_Xchange = 0
                pos_Ychange = 0'''

    check = False
    for i in range(nobs):
        if math.sqrt(math.pow(posX - posXobs[i], 2) + math.pow(posY - posYobs[i], 2)) <= max(1.0 * nobs, 70):
            check = True
        else:
            check = False
    # now implementing the policy
    if check:
        vl = math.pow(-1, np.random.choice([0, 1])) * speed * np.random.rand()    # choosing a random velocity for left wheel
        vr = math.pow(-1, np.random.choice([0, 1])) * speed * np.random.rand()    # choosing a random velocity for right wheel
    else:
        if (posX > posXdes) and (posY > posYdes):
            if direction[0] == 1:
                vl = -speed
                vr = np.random.choice([-speed, speed])
            elif direction[1] == 1:
                vl = -speed
                vr = np.random.choice([-speed, speed])
            elif direction[2] == 1:
                vl = np.random.choice([-speed, speed])
                vr = speed
            else:
                vl = np.random.choice([-speed, speed])
                vr = speed

        elif (posX > posXdes) and (posY < posYdes):
            if direction[0] == 1:
                vr = -speed
                vl = np.random.choice([-speed, speed])
            elif direction[1] == 1:
                vl = speed
                vr = np.random.choice([-speed, speed])
            elif direction[2] == 1:
                vr = np.random.choice([-speed, speed])
                vl = speed
            else:
                vl = np.random.choice([-speed, speed])
                vr = -speed

        elif (posX < posXdes) and (posY > posYdes):
            if direction[0] == 1:
                vr = speed
                vl = np.random.choice([-speed, speed])
            elif direction[1] == 1:
                vl = -speed
                vr = np.random.choice([-speed, speed])
            elif direction[2] == 1:
                vr = np.random.choice([-speed, speed])
                vl = -speed
            else:
                vl = speed
                vr = np.random.choice([-speed, speed])

        else:
            if direction[0] == 1:
                vl = speed
                vr = np.random.choice([-speed, speed])
            elif direction[1] == 1:
                vr = speed
                vl = np.random.choice([-speed, speed])
            elif direction[2] == 1:
                vl = np.random.choice([-speed, speed])
                vr = -speed
            else:
                vr = -speed
                vl = np.random.choice([-speed, speed])

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
    for i in range(nobs):    # case when the robot collides with the obstacle
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

    posX += pos_Xchange     # change in x coordinate of the robot
    posY += pos_Ychange     # change in y coordinate of the robot
    # To prevent robot from going out of the screen
    if posX <= 0:
        posX = 0
    elif posX >= (xlim-roversize):
        posX = xlim-roversize
    if posY <= 0:
        posY = 0
    elif posY >= (ylim - roversize):
        posY = ylim - roversize
    robot(posX, posY)
    destination()
    pygame.display.update()
    if (posX > posXdes - roversize and posX < posXdes + destinationsize) and (posY > posYdes - roversize and posY < posYdes + destinationsize):
        running = False    # The robot has reached the destination

steps = np.arange(1, num_steps + 1).reshape(num_steps,)  # creating an array to plot the distance between the robot and the destination as a function of steps taken by it
plt.plot(steps, distance)
plt.xlim(0, num_steps + 50)
plt.ylim(0, max(distance) + 1000)
plt.xlabel('Time (steps)')
plt.ylabel('Distance')
plt.title('Performance analysis using control policy')
plt.show()

