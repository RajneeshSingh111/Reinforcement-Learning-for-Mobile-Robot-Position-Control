from problemdata import *
discount_factor = 0.7                  # the discount factor gamma
# defining old and new policy functions to be usd in policy iteration process
policy_old = np.ones((1, 2 * (xmax + 1) * (ymax + 1)), dtype=int)
policy_new = np.ones((1, 2 * (xmax + 1) * (ymax + 1)), dtype=int)
# defining old and new value functions to iteratively store the computed value function
V_old = np.zeros((1, 2 * (xmax + 1) * (ymax + 1)))
V_new = np.zeros((1, 2 * (xmax + 1) * (ymax + 1)))
while True:
    for s in range(2 * (xmax + 1) * (ymax + 1)):
        policy_old[0][s] = policy_new[0][s]              # equating the old and new policy
    n = 100
    # now using a while loop for n = 100 to get an approximated value for current policy
    while n > 0:
        for s in range(2 * (xmax + 1) * (ymax + 1)):
            V_old[0][s] = V_new[0][s]
        for s in range(2 * (xmax + 1) * (ymax + 1)):
            summ = 0
            for i in range(2 * (xmax + 1) * (ymax + 1)):
                summ += V_old[0][i] * TPM[policy_old[0][s]-1][s][i]
                if s == 0 or s == 100:
                    V_new[0][s] = (100 + (discount_factor * summ))   # reward of 100 for reaching the destination
                else:
                    V_new[0][s] = (-10 + (discount_factor * summ))    # penalty of 10 for not reaching the destination
        n -= 1
    for s in range(2 * (xmax + 1) * (ymax + 1)):
        Q = np.zeros((1, len(Action_space)))        # using an arbitrary action to find the value
        for a in range(len(Action_space)):
            summ = 0
            for i in range(2 * (xmax + 1) * (ymax + 1)):
                summ += V_new[0][i] * TPM[a][s][i]
            if s == 0 or s == 100:
                Q[0][a] = 100 + (discount_factor * summ)     # reward of 100 for reaching the destination
            else:
                Q[0][a] = -10 + (discount_factor * summ)       # penalty of 10 for not reaching the destination
        policy_new[0][s] = 1 + np.argmax(Q)          # assigning the new policy based on the input from Q function
    if np.all(policy_new == policy_old):
        break          # exit from the loop when old and new policy matches
print("Results using policy iteration....")
print("The optimum policy function for this problem is\n", policy_new)
print("And the value function for optimum policy is\n", V_new)