import numpy as np
from maze import build_maze
from toolbox import random_policy
import time


def get_policy_from_q(q):
    p = np.zeros(q.shape[0])
    for s in range(q.shape[0]):
        p[s] = np.argmax(q[s,:])
    return p

def get_policy_from_v(mdp, v):
    # Outputs a policy given the state values
    policy = np.zeros(mdp.nb_states)  # initial state values are set to 0
    for x in range(mdp.nb_states):  # for each state x
        # Compute the value of the state x for each action u of the MDP action space
        v_temp = []
        for u in mdp.action_space.actions:
            if x not in mdp.terminal_states:
                # Process sum of the values of the neighbouring states
                summ = 0
                for y in range(mdp.nb_states):
                    summ = summ + mdp.P[x, u, y] * v[y]
                v_temp.append(mdp.r[x, u] + mdp.gamma * summ)
            else:  # if the state is final, then we only take the reward into account
                v_temp.append(mdp.r[x, u])
        policy[x] = np.argmax(v_temp)
    print(policy)
    return policy


def improve_policy_from_v(mdp, v, policy):
    
    return np.argmax(mdp.r[x,u]+mdp.gamma*np.sum(mdp.P[x,u,:]*v[:]))


def evaluate_one_step_v(mdp, v, policy):
    # Outputs the state value function after one step of policy evaluation
    # Corresponds to one application of the Bellman Operator
    v_new = np.zeros(mdp.nb_states)  # initial state values are set to 0
    for x in range(mdp.nb_states):  # for each state x
        # Compute the value of the state x for each action u of the MDP action space
        v_temp = []
        if x not in mdp.terminal_states:
            # Process sum of the values of the neighbouring states
            summ = 0
            for y in range(mdp.nb_states):
                summ = summ + mdp.P[x, policy[x].astype("int"), y] * v[y]
            v_temp.append(mdp.r[x, policy[x].astype("int")] + mdp.gamma * summ)
        else:  # if the state is final, then we only take the reward into account
            v_temp.append(mdp.r[x, policy[x].astype("int")])

        # Select the highest state value among those computed
        v_new[x] = np.max(v_temp)
    return v_new


def evaluate_v(mdp, policy):
    # Outputs the state value function of a policy
    v = np.zeros(mdp.nb_states)  # initial state values are set to 0
    stop = False
    while not stop:
        vold = v.copy()
        v = evaluate_one_step_v(mdp, vold, policy)

        # Test if convergence has been reached
        if (np.linalg.norm(v - vold)) < 0.01:
            stop = True
    return v

def evaluate_one_step_q(mdp, q, policy):
    # Outputs the state value function after one step of policy evaluation
    q_new = np.zeros((mdp.nb_states, mdp.action_space.size))  # initial action values are set to 0
    for x in range(mdp.nb_states):  # for each state x
        # Compute the value of the state x for each action u of the MDP action space
        q_temp = []
        if x not in mdp.terminal_states:
            # Process sum of the values of the neighbouring states
            summ = 0
            for y in range(mdp.nb_states):
                summ = summ + mdp.P[x, :, y] * q[y,policy[y].astype("int")]
            q_temp.append(mdp.r[x, :] + mdp.gamma * summ)
        else:  # if the state is final, then we only take the reward into account
            q_temp.append(mdp.r[x, :])

        # Select the highest state value among those computed
        q_new[x] = np.max(q_temp)
    return q_new


def evaluate_q(mdp, policy):
    # Outputs the state value function of a policy
    q = np.zeros((mdp.nb_states, mdp.action_space.size))  # initial action values are set to 0
    stop = False
    while not stop:
        qold = q.copy()
        q = evaluate_one_step_q(mdp, qold, policy)

        # Test if convergence has been reached
        if (np.linalg.norm(q - qold)) < 0.01:
            stop = True
    return q

# ------------------------- Value Iteration with the V function ----------------------------#
# Given a MDP, this algorithm computes the optimal state value function V
# It then derives the optimal policy based on this function


def value_iteration_v(mdp, render=True):
    # Value Iteration using the state value v
    v = np.zeros(mdp.nb_states)  # initial state values are set to 0
    stop = False

    if render:
        mdp.new_render()

    while not stop:
        v_old = v.copy()
        if render:
            mdp.render(v)

        for x in range(mdp.nb_states):  # for each state x
            # Compute the value of the state x for each action u of the MDP action space
            v_temp = []
            for u in mdp.action_space.actions:
                if x not in mdp.terminal_states:
                    # Process sum of the values of the neighbouring states
                    summ = 0
                    for y in range(mdp.nb_states):
                        summ = summ + mdp.P[x, u, y] * v_old[y]
                    v_temp.append(mdp.r[x, u] + mdp.gamma * summ)
                else:  # if the state is final, then we only take the reward into account
                    v_temp.append(mdp.r[x, u])

                    # Select the highest state value among those computed
            v[x] = np.max(v_temp)

        # Test if convergence has been reached
        if (np.linalg.norm(v - v_old)) < 0.01:
            stop = True

    policy = get_policy_from_v(mdp, v)
    if render:
        mdp.render(v, policy)

    return v

# ------------------------- Value Iteration with the Q function ----------------------------#
# Given a MDP, this algorithm computes the optimal action value function Q
# It then derives the optimal policy based on this function


def value_iteration_q(mdp, render=True):
    q = np.zeros((mdp.nb_states, mdp.action_space.size))  # initial action values are set to 0
    stop = False

    if render:
        mdp.new_render()

    while not stop:
        qold = q.copy()

        if render:
            mdp.render(q)

        for x in range(mdp.nb_states):
            for u in mdp.action_space.actions:
                if x in mdp.terminal_states:
                    q[x, :] = mdp.r[x, u]
                else:
                    summ = 0
                    for y in range(mdp.nb_states):
                        summ += mdp.P[x, u, y] * np.max(qold[y, :])
                    q[x, u] = mdp.r[x, u]+mdp.gamma * summ

        if (np.linalg.norm(q - qold)) <= 0.01:
            stop = True

    if render:
        mdp.render(q)
    return q


def improve_policy_from_q(mdp, q, policy):
    best_policy = False
    while not best_policy:
        pi = np.zeros(mdp.nb_states)

        for s in range(mdp.nb_states):
            t = []
            for u in mdp.action_space.actions:
                temp = []
                for x in range(mdp.nb_states):
                    temp.append(mdp.P[s, u, x] * np.max(q[x, :]))

                t.append(max(temp))
            pi[s] = np.argmax(np.array(t))

        for i in range(policy.shape[0]):
            best_policy = True
            if (policy[i] != pi[i]):
                policy[i] = pi[i]
                best_policy = False

    return policy

# ------------------------- Policy Iteration with the Q function ----------------------------#
# Given a MDP, this algorithm simultaneously computes the optimal action value function Q and the optimal policy

def policy_iteration_q(mdp, render=True):  # policy iteration over the q function
    q = np.zeros((mdp.nb_states, mdp.action_space.size))  # initial action values are set to 0
    policy = random_policy(mdp)

    stop = False

    if render:
        mdp.new_render()
        
    i=0

    while not stop:
        i+=1
        
        qold = q.copy()

        q = evaluate_q(mdp,policy)
        
        if render:
            mdp.render(q)
            mdp.plotter.render_pi(policy)
        

        policy = improve_policy_from_q(mdp,q,policy)

        # Check convergence
        if (np.linalg.norm(q - qold)) <= 0.01:
            stop = True

    if render:
        mdp.render(q, get_policy_from_q(q))
        
    print(i)
    return q


# ------------------------- Policy Iteration with the V function ----------------------------#
# Given a MDP, this algorithm simultaneously computes the optimal state value function V and the optimal policy

def policy_iteration_v(mdp, render=True):
    # policy iteration over the v function
    v = np.zeros(mdp.nb_states)  # initial state values are set to 0
    policy = random_policy(mdp)

    stop = False

    if render:
        mdp.new_render()
        
    i=0

    while not stop:
        i+=1
        vold = v.copy()
        
        v = evaluate_v(mdp,policy)

        if render:
            mdp.render(v)
            mdp.plotter.render_pi(policy)

        policy = get_policy_from_v(mdp,v)

        # Check convergence
        if (np.linalg.norm(v - vold)) < 0.01:
            stop = True

    if render:
        mdp.render(v)
        mdp.plotter.render_pi(policy)
        
    print(i)
    
    return v


def run():
    walls = [7, 8, 9,10,21,27,30,31,32,33,45,46,47]
    height = 6
    width = 9

    m = build_maze(width, height, walls)  # maze-like MDP definition

    print("value iteration V")
    value_iteration_v(m, render=True)
    print("value iteration Q")
    value_iteration_q(m, render=True)
    print("policy iteration Q")
    t = time.time()
    policy_iteration_q(m, render=True)
    print(time.time()-t)
    print("policy iteration V")
    t = time.time()
    policy_iteration_v(m, render=True)
    print(time.time()-t)
    input("press enter")

run()
