import numpy as np
import random

nPercepts = 75  # This is the number of percepts
nActions = 7  # This is the number of actions

class game_stat:
    MUTATIONRATE = 0.8
    meta_gene = [10,1,0,0,0]

class MyCreature:

    def __init__(self):
        self.chromosomes = [np.random.uniform(0, 1, size=(75,7)),]
            #np.random.uniform(0, 1, size=(25, 7)),
            #np.random.uniform(0, 1, size=(25, 7))]
        #self.chromosomes = [np.random.uniform(0,1,size=25,7),]


    def AgentFunction(self, percepts):
        actions = np.zeros((nActions))
        creature_map = percepts[:,:,0]
        food_map = percepts[:,:,1]
        wall_map = percepts[:,:,2]
        creature_map[creature_map>0] = 0
        creature_map[wall_map>0] = -1
        creature_map = creature_map[1:4,1:4]
        #actions[4] = np.matmul(creature_map.flatten(),self.chromosomes[0])[0]
        #actions[5] = food_map[2,2] * self.chromosomes[0][0][0]
        for i in range(nActions):
                actions[i] = np.dot(percepts.flatten(),self.chromosomes[0])[i]
        if food_map[2, 2] == 1:
            actions[5] += 0.30
        return actions


def selectParentTournament(old_population, k):
    tournament = list()
    while len(tournament) != k:
        tournament.append(old_population[np.random.randint(0, len(old_population))])

    best = tournament[0]
    for individual in tournament:
        if get_fitness_eval(individual) > get_fitness_eval(best):
            best = individual

    return best

def crossover(x1,x2):
    """
    Cross over each of the weights
    """
    result_chromos = [np.zeros((chromo.shape)) for chromo in x1.chromosomes]
    i = 0
    for j in range(len(x1.chromosomes[i])):
        for k in range(len(x1.chromosomes[i][j])):
            if(np.random.rand(1) < 0.5):
                result_chromos[i][j][k] = x1.chromosomes[i][j][k]
            else:
                result_chromos[i][j][k] = x2.chromosomes[i][j][k]
            if(np.random.rand(1)<game_stat.MUTATIONRATE):
                result_chromos[i][j][k] += -0.05 + np.random.rand(1)*0.1
    return result_chromos

def normalize_fitness(fitness):
    exp_sum = 0
    for fit in fitness:
        exp_sum += np.power(np.exp(fit),2)
    norm_fitness = [np.power(np.exp(fit),2)/exp_sum for fit in fitness]
    return norm_fitness

def newGeneration(old_population):
    new_population = list()
    fitness = np.zeros(len(old_population))
    parent_a = selectParentTournament(old_population,5)
    parent_b = selectParentTournament(old_population,5)
    while np.array_equal(parent_a,parent_b):
        parent_b = selectParentTournament(old_population,5)

    fitness = [get_fitness_eval(creature) for creature in old_population]
    #print("\nbiased:",np.array(fitness).mean())
    fitness = normalize_fitness(fitness)
    for n in range(len(old_population)):
        super_cute_baby = MyCreature()
        batch = np.random.choice(old_population,(2),replace=False,p=fitness)
        super_cute_baby.chromosomes = crossover(parent_a,parent_b)
        new_population.append(super_cute_baby)
    avg_fitness = np.array([unbiased_fitness(creature) for creature in old_population]).mean()
    return (new_population, avg_fitness)

def get_fitness_eval(creature):
    f1 = game_stat.meta_gene[0]
    f2 = game_stat.meta_gene[1]
    f3 = game_stat.meta_gene[2]
    f4 = game_stat.meta_gene[3]
    f5 = game_stat.meta_gene[4]
    fitness = (f1*creature.alive + f2 *creature.turn + f3*creature.enemy_eats + f4*creature.strawb_eats  + f5*creature.size)
    return fitness
def unbiased_fitness(creature):
    f1 = 1
    f2 = 1
    f3 = 1
    f4 = 1
    f5 = 1
    fitness = (f1 *creature.turn + f2*creature.enemy_eats + f3*creature.strawb_eats + f4*creature.alive + f5*creature.size)
    return fitness