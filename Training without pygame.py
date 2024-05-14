import numpy as np
import math
import random
import pickle
import matplotlib.pyplot as plt

# screen size
xlim = 400
ylim = 300

# sizes
roversize = 32
destinationsize = 32
obstaclesize = 32

# deciding parameters
speed = 2    # speed of the robot
nobs = 1        # no. of obstacles
deflect = 32   # this happens when robot collides with obstacle
epsilon = 0     # a default value for epsilon
eps_decay = 0.998
alpha_decay = 0.998
num_episodes = 10000
learning_rate = 0.9
discount = 0.95
steps = np.zeros((9, num_episodes))  # This defines the number of steps taken by th erobot to reach the destinationfor various values of epsilon


# Class
class Mobile_robot:
    def __init__(self):
        self.posX = math.floor((xlim - roversize) * np.random.rand()) + roversize / 2
        self.posY = math.floor((ylim - roversize) * np.random.rand()) + roversize / 2
        self.posXdes = math.floor((xlim - destinationsize) * np.random.rand()) + destinationsize / 2
        self.posYdes = math.floor((ylim - destinationsize) * np.random.rand()) + destinationsize / 2
        self.posXobs = []
        self.posYobs = []
        # introducing the obstacles
        for i in range(nobs):
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

    # Now defining a reward function to give rewards to the robot
    def rewards(self):
        if min((math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)),0.5)) for i in range(nobs)) <= 32:
            output = -1000     # Reward = -1000 when the robot hits the obstacle
        elif (math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)), 0.5)) <= 32:
            output = 2000      # Reward = 2000 when the robot reaches the destination
        else:     # when the robot is at some distance s from the destination then the reward is -s
            output = -(math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)), 0.5))

        reward.append(output)
        return output

    # Now defining the function to get the states [[destination distance, destination angle], [nearest obstacle distance, nearest obstacle angle]]
    def get_state(self):
        self.des_distance = math.pow((math.pow((self.posX - self.posXdes), 2)) + (math.pow((self.posY - self.posYdes), 2)),0.5)
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
            if math.pow((math.pow((self.posX - self.posXobs[i]), 2)) + (math.pow((self.posY - self.posYobs[i]), 2)), 0.5) == self.obs_distance:
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
    num_steps = 0             # initially the number of steps taken by the robot is 0

    # Initializing
    def __init__(self):
        self.robo = Mobile_robot()

    # Executing
    def execute(self):
        running = self.robo.check()
        while running:
            self.num_steps += 1   # updating the number of steps
            obs = self.robo.get_state()        # getting the current state
            if np.random.random() > epsilon:
                action = np.argmax(q_table[obs])           # EXPLOITATION
            else:
                action = random.randint(0, 3)                 # EXPLORATION
            pos_Xchange, pos_Ychange = self.robo.get_action(action)
            self.robo.move(pos_Xchange, pos_Ychange)
            new_obs = self.robo.get_state()      # Getting the next state
            max_future_q = np.max(q_table[new_obs])  # Choosing maximum value for next state
            current_q = q_table[obs][action]  # storing the value in the Q-MATRIX
            result = self.robo.rewards()
            if result == 2000:
                new_q = 2000
            else:
                new_q = (1-learning_rate) * current_q + learning_rate * (result + discount * max_future_q)
            q_table[obs][action] = new_q     # Updating the Q-MATRIX
            running = self.robo.check()

for m in range(9):
    print('Creating Q-Table')            # Creating a pickle file to store the Q-table
    q_table = {}
    for i in range(int(math.pow((math.pow(xlim, 2.0)) + (math.pow(ylim, 2.0)), 0.5))):
        for j in range(4):
            for k in range(int(math.pow((math.pow(xlim, 2.0)) + (math.pow(ylim, 2.0)), 0.5))):
                for l in range(4):
                    q_table[((i, j), (k, l))] = [np.random.uniform(0, 1000) for i in range(4)]
    epsilon += 0.1
    for i in range(num_episodes):
        reward = []
        simulation = Run()
        simulation.execute()
        if i % 100 == 0:
            print(f'Episode {i + 1} : {np.sum(reward)}')
            if i % 50000 == 0:
                with open(f'q_table-{i}.pkl', 'wb') as f:
                    pickle.dump(q_table, f)  # saving the q_table
        steps[m][i] = simulation.num_steps         # Storing the number of steps taken in each episode for every value of epsilon
avg_steps = np.mean(steps, axis=1).reshape(1, 9)  # storing teh average number of steps
print(avg_steps)
fig = plt.figure()
x = np.arange(1, num_episodes + 1).reshape(1, num_episodes)     # an array to store the number of episodes
e_matrix = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])    # matrix to store all the values of epsilon used here
ax1 = plt.subplot(1, 2, 1)
ax2 = plt.subplot(1, 2, 2)
for i in range(9):
    row = steps[i: i+1, :]
    ax1.plot(x.T, row.T,  label=f'Epsilon = {(i + 1)/10}')
ax1.legend(loc='upper left')
ax1.set_xlim(0, num_episodes + 1000)
ax1.set_ylim(0, np.max(steps) + 10000)
ax1.set_xlabel('Episode No.')
ax1.set_ylabel('Number of Steps')
ax1.set_title('Number of steps with respect to episode')
ax2.plot(e_matrix.T, avg_steps.T)
ax2.set_xlim(0, 1.0)
ax2.set_ylim(0, np.max(avg_steps) + 1000)
ax2.set_xlabel('Epsilon')
ax2.set_ylabel('Average number of steps')
ax2.set_title('Performance analysis for various values of epsilon')
plt.show()