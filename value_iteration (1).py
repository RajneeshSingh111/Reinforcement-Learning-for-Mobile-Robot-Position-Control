from problemdata import *
discount_factor = 0.7            # the discount factor gamma
tolerance = 0.00001                 # choosing some value for the tolerance
# defining old and new value functions to iteratively store the computed value function
V_old = np.zeros((1, 2 * (xmax + 1) * (ymax + 1)))
V_new = np.zeros((1, 2 * (xmax + 1) * (ymax + 1)))
policy = np.zeros((1, 2 * (xmax + 1) * (ymax + 1)), dtype=int)        # to store the optimum policy
while True:
    for s in range(2 * (xmax + 1) * (ymax + 1)):
        V_old[0][s] = V_new[0][s]             # equating the new and old values
    for s in range(2 * (xmax + 1) * (ymax + 1)):
        test = np.zeros((1, len(Action_space)))
        for a in range(len(Action_space)):
            summ = 0
            for i in range(2 * (xmax + 1) * (ymax + 1)):
                summ += V_old[0][i] * TPM[a][s][i]
            if s == 0 or s == 100:
                test[0][a] = 100 + (discount_factor * summ)    # reward of 100 for reaching the destination
            else:
                test[0][a] = -10 + (discount_factor * summ)    # penalty of 10 for not reaching the destination

        V_new[0][s] = np.max(test)                        # maximising the values using value iteration
        policy[0][s] = 1 + np.argmax(test)             # storing the policy
    if np.max(np.abs(V_new - V_old)) < tolerance:
        break             # exit from the loop when the error falls below the assigned tolerance
print("Results using value iteration....")
print("The last two iterations which give the approximate value function are\n", V_old, " and\n", V_new)
print("And the policy which maximises the value is\n", policy)