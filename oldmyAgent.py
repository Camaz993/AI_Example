import numpy as np
import random
from sklearn.preprocessing import normalize

playerName = "myAgent"
nPercepts = 75  # This is the number of percepts
nActions = 7  # This is the number of actionss

class game_stat:
    MUTATIONRATE = 0.8
    meta_gene = [1,1,1,1,1]

# This is the class for your creature/agent

class MyCreature():

    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values
        self.chromosomes = [np.random.uniform(0, 1, size=(7, 75)),]

    def AgentFunction(self, percepts):
        # This agent creates a 7-dim vector of zeros for actions
        actions = np.zeros((nActions))

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 7-dim numpy vector or a
        # list with 7 numbers.
        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 3 - move down
        # 4 - do nothing
        # 5 - eat
        # 6 - move in a random direction
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.
        # .
        # .
        # .
        actions = np.zeros((nActions))
        food_map = percepts[:,:,1]
        for i in range(nActions):
            actions[i] = np.dot(percepts.flatten(), self.chromosomes[0][i])
        #if food_map[2, 2] == 1:
        #   actions[5] += 0.3
        return actions




def newGeneration(old_population):
    # This function should return a list of 'new_agents' that is of the same length as the
    # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
    # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    fitnesss = []
    f1 = game_stat.meta_gene[0]
    f2 = game_stat.meta_gene[1]
    f3 = game_stat.meta_gene[2]
    f4 = game_stat.meta_gene[3]
    f5 = game_stat.meta_gene[4]
    for n, creature in enumerate(old_population):
        # creature is an instance of MyCreature that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the objects has attributes provided by the
        # game engine:
        #
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies
        fitness[n] = (f3*creature.alive + f4*creature.turn + f1*creature.enemy_eats + f2*creature.strawb_eats  + f5*creature.size)
        fitnesss.append(fitness[n])
    # At this point you should sort the agent according to fitness and create new population
    new_population = list()

    for n in range(N):
        # Create new creature
        new_creature = MyCreature()

        normfit = normalize_fitness(fitnesss)

        # Here you should modify the new_creature's chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_creature.chromosome

        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.

        batch = np.random.choice(old_population, (2), replace=False,p=normfit)
        new_creature.chromosomes = crossover(batch[0], batch[1])

        # Add the new agent to the new population
        new_population.append(new_creature)


    # At the end you neet to compute average fitness and return it along with your new population

    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)

def crossover(x1,x2):
    """
    Cross over each of the weights
    """
    for chromo in x1.chromosomes:
        result_chromos = [np.zeros((chromo.shape))]
    #result_chromos = [np.zeros((chromo.shape)) for chromo in x1.chromosomes]
    i = 0
    for j in range(len(x1.chromosomes[i])):
        for k in range(len(x1.chromosomes[i][j])):
            if(np.random.rand(1) < 0.5):
                result_chromos[i][j][k] = x1.chromosomes[i][j][k]
            else:
                result_chromos[i][j][k] = x2.chromosomes[i][j][k]
            if(np.random.rand(1)< 0.8):#at 0.3 very agressive
                result_chromos[i][j][k] += -0.05 + np.random.rand(1)*0.1
    return result_chromos

def normalize_fitness(fitness):
    exp_sum = 0
    for fit in fitness:
        exp_sum += np.power(np.exp(fit),2)
    norm_fitness = [np.power(np.exp(fit),2)/exp_sum for fit in fitness]
    return norm_fitness



