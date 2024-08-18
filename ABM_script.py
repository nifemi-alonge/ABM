# packages
import numpy as np
import matplotlib.pyplot as plt
import random
from copy import deepcopy

## Assumptions
# set seed
random.seed(1)

# setting out agents:
# group A = on-peak, group B = off-peak
# like vowels in tutorial
groups_a = ['A'] * 980
groups_b = ['B'] * 20

# groups_a = ['A'] * 500
# groups_b = ['B'] * 500
groups = groups_a + groups_b

# setting up willingness parameter
# distribution from which to sample
# uniform distribution between 0 and 1
willingness_distribution = np.random.uniform(0,1.0, 1000)

# setting up persuasion parameter
persuasion_distribution = np.random.uniform(0,1.0, 1000)

# plot distribution
plt.hist(willingness_distribution)
plt.show()

plt.hist(persuasion_distribution)
plt.show()

## Functions
# create function to make agents
def make_agent(groups, willingness_to_switch, persuasiveness):
    return [groups, willingness_to_switch, persuasiveness]

# assign willingness to switch and persuasiveness (attributes of agents) to agents
def create_population(n):
    population = []
    for i in range(n):
        # pick a random agent from the list
        g = random.choice(groups)
        # willingness_to_switch is a random choice from willingness_distribution
        # like 'personalities' in tutorial
        willingness_to_switch = random.choice(willingness_distribution)
        # persuasiveness is a random choice from persuasion_distribution
        persuasiveness = random.choice(persuasion_distribution)

        agent = make_agent(g, willingness_to_switch, persuasiveness)
        population.append(agent)
    return population

# run function
population = create_population(1000)
print(population)

# calculate proportion of agents in groups A and B
def count(population):
    t=0.
    for agent in population:
        if agent[0] == 'A':
            t+= 1
    return t / len(population)

# run function, check proportions
prop_A = count(create_population(1000))
print('prop in A = ', prop_A)
print('prop in B = ', 1 - prop_A)

## Interaction functions
# create function to select agent pairs
def choose_pair(population):
    i = np.random.randint(0, len(population) -1)
    j = np.random.randint(0, len(population) -1)

    while i == j:
        j = np.random.randint(0, len(population) - 1) #only select unique agents

    return population[i], population[j]

# testing
population = create_population(8)
influencee, influencer = choose_pair(population)

# printouts
print('population = ', population)
print('chosen pair = ', influencee, influencer)
print('the person being influenced (influencee) is', influencee)
print('the person influencing (influencer) is', influencer)

# interact
# if influencee and influencer are in the same group - no change
# if influencee and influencer are in different groups:
# influencee will change groups is influencee[1], willingness * influencer[2], persuasiveness > threshold
# [0] = group, [1] = willingness_to_switch, [2] = persuasiveness
def interact(influencee,influencer, threshold):
    if influencee[0] == influencer[0]: # same - no change
        return influencee
    elif influencee[1] * influencer[2] >= threshold: # change is product
        influencee[0]=deepcopy(influencer[0])
        return influencee
    else:
        return influencee # anything else


# 3 conditions of interaction and switching

# testing the above interaction function
randominfluencee, randominfluencer = choose_pair(create_population(8))
print('influencee = ', randominfluencee)
print('influencer = ', randominfluencer)

# 0.7 is threshold here
updated_influencee = interact(randominfluencee, randominfluencer, 0.7)
print('after interaction the influencee is', updated_influencee[0])

# testing function works as expected 0 correct
t_influencee =  ['A', 0.9167229343173493, 0.6485551485138286]
t_influencer =  ['B', 0.4167229343173493, 1.0000000000000000]
# 0.7 is threshold here
updated_influencee = interact(t_influencee, t_influencer, 0.7)
print('after interaction the influencee is', updated_influencee[0])

## Simulation
# n no. of agents
# k no. of interactions
# threshold input to interact function
def simulate(n,k,threshold):
    population = create_population(n)
    print('initial pop = ', population)

    proportion = []

    for i in range(k):
        pair = choose_pair(population)
        interact(pair[0],pair[1], threshold)
        proportion.append(count(population))
    return population, proportion

# running simulation function
new_population, proportion = simulate(1000, 50, 0.7)
print('final pop = ', new_population)

# plot
plt.plot(proportion)
plt.title('Changes in A over time')
plt.ylabel('Prop in A')
plt.xlabel('Time')
plt.ylim(0.9,1) # can change these to zoom in
plt.show()

# batch simulate
# n no. of agents
# k no. of interactions
# so no. of simulations - how many times
# threshold input to interact function
def batch_simulate(n, k, s, threshold):
    batch_proportions = []
    for i in range(s):
        new_population, proportion = simulate(n, k, threshold)
        batch_proportions.append(proportion)
    return batch_proportions

# show batch simulate
results = batch_simulate(1000, 5000, 20, 0.7)

plt.ylim(0.9,1) # can change these to zoom in

# plotting
for i in results:
    plt.plot(i)

plt.title('Changes in A over time (Batch Simulation Modelling)')
plt.ylabel('Prop in A')
plt.xlabel('Time')
plt.show()

# Threshold modelling
def batch_threshold(n, k, threshold):
    batch_proportions = []
    for i in threshold:
        new_population, proportion = simulate(n, k, i)
        batch_proportions.append(proportion)
    return batch_proportions

# show batch simulate
list_of_thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
results = batch_threshold(1000, 5000, list_of_thresholds)

plt.ylim(0.9,1) # can change these to zoom in

# plotting
for i in range(len(results)):
    plt.plot(results[i], label=list_of_thresholds[i])

plt.title('Changes in A over time (varying thresholds)')
plt.ylabel('Prop in A')
plt.xlabel('Time')
plt.legend()
plt.show()

#Source: Bill Thompson and Limor Raviv, 2018 Tutorial Agent Based Models, Github