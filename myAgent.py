import numpy as np
import matplotlib.pyplot as plt

playerName = "myAgent"
nPercepts = 75  # This is the number of percepts
nActions = 7  # This is the number of actions
graphfitness = [] # Used only for graphing average fitness

# This is the class for your creature/agent
# It is where the basic functionality of my program is created
# It usually starts winning around game 50-100. The random player can however, do very well randomly....
# In the mutation part of the code I tested it with adding and equaling a random number and have provided the code
# that I used for both.
# By around game 200-300 it should start holding the random player to under 10 individuals sometimes less.
# If the agents fitness is varying up to 200 and sometimes will lose a couple games then start winning,
# then it is relearning the most effective behaviour, eventually it reaches peak despite this.
# The occurrence of this was rare for me but could happen, it is still worth watching regardless.
class MyCreature():

    # I decided to map my chromosomes so there are 7 lots of 75, 525 chromosomes in total.
    # These consisted of uniform distribution numbers between 0-1 which I found worked best with my GA.
    # The chromosomes datatype is a list.
    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        self.chromosomes = [np.random.uniform(0, 1, size=(7, 75)),]

        # This is the code I used to graph the fitness
        # It is fairly basic the only messy thing is that it prints 25 graphs at the end of the game
        # I hope this doesn't prove to be inconvenience (all graphs are the same)
        if len(graphfitness) == 499:
            plt.close('all')
            plt.plot(graphfitness)
            plt.ylabel('Avg Fitness For Each Evolution')
            plt.xlabel('Amount of evolutions')
            plt.show()


    # This is the function that transfers percepts into actions.
    # For each of the seven actions the function uses np.dot to multiply the total
    # percepts (flattened) and the added total of 75 of the chromosomes.
    # As i is increments it maps through all of the chromosomes
    def AgentFunction(self, percepts):
        # This agent creates a 7-dim vector of zeros for actions
        actions = np.zeros((nActions))

        for i in range(nActions):
            actions[i] = np.dot(percepts.flatten(), self.chromosomes[0][i])
        return actions

# This method is what creates the new population for each round.
# I use a while loop to append each of the new creatures to the new population,
# this makes sure that there is 34 creatures in the new population.
# Tournament selection is run to select two parents from the old population.
# These parents chromosomes are then crossed over to create a new fit individual.
# So, for each new individual two "fit" parents are crossed over and this is done 34 times.
def newGeneration(old_population):
    # At this point you should sort the agent according to fitness and create new population
    new_population = list()

    while len(new_population) != len(old_population):#34
        parent1 = tournament_selection(old_population)
        parent2 = tournament_selection(old_population)
        # This is important because without it the parents have a chance of being the same.
        # I originally had an if statement but it seems sometimes they could be selected as the same twice.
        while parent1 == parent2:
           parent2 = tournament_selection(old_population)

        # Create new creature
        new_creature = MyCreature()

        # Cross over parents selected by tournament
        new_creature.chromosomes = crossover(parent1, parent2)

        # Add the new agent/creature to the new population
        new_population.append(new_creature)

    # At the end you need to compute average fitness and return it along with your new population
    # Basic average fitness calculations computed here.
    # I also append the average fitness of each generation to the list for graphing
    avg_fitness = 0
    for creature in old_population:
        avg_fitness += get_fitness(creature)
    avg_fitness = avg_fitness/len(old_population)
    graphfitness.append(avg_fitness)
    return (new_population, avg_fitness)


# This is the method I have created for crossing over the two parents genes/chromosomes.
# First I created a list filled with zeros that mirrored the parents 525 chromosomes.
# I then did a 50/50 or uniform crossover so there is an even chance of either parents chromosomes being selected.
# The for loops run through each of the parents chromosomes (all 525) and interchange them.
# For example, chromosome[0][1][63] might be selected from parent1 and so on and [0][1][64] from parent2.
# I tried crossing over just the 75 chromosomes (chromosome[0][0-6]) however this didn't work as well.
# The second if statement imports a chance that each chromosome is mutated slightly to be
# different from the parents. The mutation rate is set at 0.01 so one in every 100 chromosomes will be mutated.
# You could run it with 0.1 which would mutate more aggressively and work better.
# I've also included the code for the equals method for mutation instead of adding.
# The new chromosomes are then returned and given to the new creature.
# new_chromosomes[i][x][y] = np.random.random(1) this is the code for none limited mutation
def crossover(genes1,genes2):

    new_chromosomes = [np.zeros((7, 75))]
    i = 0
    selectionchance = 0.5
    mutationRate = 0.01 # or 0.1 aggressive.....

    # Crosses over the two Genes based on the original Mapping
    for x in range(nActions):
        for y in range(nPercepts):

            if(np.random.random(1) < selectionchance):#Parent One
                new_chromosomes[i][x][y] = genes1.chromosomes[i][x][y]

            else:# Parent Two
                new_chromosomes[i][x][y] = genes2.chromosomes[i][x][y]

            # Here is where mutation occurs saved me writing another nested for loop method
            # A form of random reset mutation
            if(np.random.random(1) < mutationRate):
                new_chromosomes[i][x][y] += np.random.random(1)# Change + to equals for different method

    return new_chromosomes


# This is the fitness function I have created which can be called to get a creatures fitness.
# The reason why I have included all of the "creature.'s" is because then agents learn to do multiple actions.
# The main influence in the function will be how many turns they survive as that could be as high as 100.
# So once we have the ones that survived the game it is then based on their eating habits or size.
# It seems relatively simple but after playing around with it for a while these values seemed to work best.
def get_fitness(creature):
    # The reason why it is multiplied by 1 is so it either equals 0 or 1. Either way
    # it shouldn't have much influence until late games.
    fitness = (1*creature.alive + creature.turn + creature.strawb_eats + creature.enemy_eats + creature.size)
    return fitness


# This method works by taking in the old population and creating a tournament from it.
# I think a good tournament size is between 5-7 or else it will tend to over or under fit.
# Each tournament consists of 6 random players from the old population.
# These individuals are then compared with each other based on fitness until the
# "winner" (fittest creature) of the tournament is found.
def tournament_selection(old_population):
    tourney = list()
    count = 0

    # Tournament size is 6 and the count increments so that only 6 random creatures are added
    while count != 6:
        tourney.append(old_population[np.random.random_integers(0, len(old_population)-1)])
        count+=1

    # Comparisons method using fitness function
    winner = tourney[0]
    for critter in tourney:
        if get_fitness(critter) > get_fitness(winner):
            winner = critter
    return winner



