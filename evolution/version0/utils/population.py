import copy
import heapq
import logging
import math
from utils import config, individual
import random

log = logging.getLogger(__name__)

class Population(object):
    def __init__(self, *args, **kwargs):
        super().__init__()
        #log.debug("Population init")
        self.children = self.generateChildren()
        self.adults = []
        self.children_fitness = None
        self.temperature = config.TEMPERATURE
        self.parents = None
        self.average_fitness = None
        self.standard_deviation = None

    def generateChildren(self):
        children = []
        for child in range(config.NUMBER_OF_CHILDREN):
            newborn = individual.Individual()
            newborn.generateGenotype()
            children.append(newborn)
        #log.debug(children)
        return children

    def develop(self):
        for child in self.children:
            child.generatePhenotype()
        #log.debug(self.children)

    def evaluate(self):
        self.children_fitness = []
        for child in self.children:
            child.evaluateFitness()
            heapq.heappush(self.children_fitness, child)
        #log.debug(self.children_fitness)
        #log.debug(self.children)

    def adultSelection(self):
        adults = []
        if config.ADULT_SELECTION == "F":
            #log.debug("Full selection")
            self.adults = []
            for child in self.children:
                child.mature()
                adults.append(child)
            self.children = []
            #log.debug(adults)
            self.adults = adults
        elif config.ADULT_SELECTION == "O":
            #log.debug("Over-production selection")
            self.adults = []
            for child in self.children_fitness[-config.POPULATION_SIZE:]:
                child.mature()
                adults.append(child)
            self.children = []
            log.debug(adults)
            self.adults = adults
        elif config.ADULT_SELECTION == "G":
            #log.debug("Mixed selection")
            mixed_fitness = (self.adults + self.children)
            heapq.heapify(mixed_fitness)
            for individual in mixed_fitness[-config.POPULATION_SIZE:]:
                individual.mature()
                adults.append(individual)
            self.children = []
            #log.debug(adults)
            self.adults = adults
        else: log.warning("Adult selection error")
    
    def parentSelection(self):
        parents = []
        self.generationInformation()

        # Fitness propogation
        if config.PARENT_SELECTION == "F":
            #log.debug("Fitness proportionate")
            total_fitness = 0
            for adult in self.adults:
                total_fitness += adult.fitness
            #log.debug(total_fitness)
            temp_fitness = 0
            for adult in self.adults:
                adult.fitness_range = (temp_fitness, temp_fitness +
                                        (adult.fitness/total_fitness))
                temp_fitness += adult.fitness / total_fitness
                #log.debug(adult.fitness_range)
            while len(parents) < (config.NUMBER_OF_CHILDREN / 
                                    config.CHILDREN_PER_PAIR):
                a = random.random()
                #log.debug(a)
                for adult1 in self.adults:
                    if adult1.fitness_range[0] < a < adult1.fitness_range[1]:
                        b = random.random()
                        #log.debug(b)
                        for adult2 in self.adults:
                            if(adult2 != adult1 and
                                    adult2.fitness_range[0] < b and
                                    b < adult2.fitness_range[1]):
                                parents.append([adult1, adult2])
                                break
                        #log.debug(len(parents))
                        break
            #log.debug(parents)
            self.parents = parents
            
        # Sigma scaling
        elif config.PARENT_SELECTION == "S":
            #log.debug("Sigma-scaling")
            total_fitness = 0
            sigma_list = []
            for adult in self.adults:
                if adult.fitness - self.average_fitness == 0:
                    sigma_factor = 1
                else:
                    sigma_factor = 1 + ((adult.fitness - self.average_fitness) / 
                                        (2 * self.standard_deviation))
                sigma_fitness = sigma_factor * adult.fitness
                sigma_list.append(sigma_fitness)
                total_fitness += sigma_fitness
            #log.debug(sigma_list)
            temp_fitness = 0
            counter = 0
            for adult in self.adults:
                adult.fitness_range = (temp_fitness, temp_fitness +
                                        (sigma_list[counter]/total_fitness))
                temp_fitness += sigma_list[counter] / total_fitness
                counter += 1
                #log.debug(adult.fitness_range)
            while len(parents) < (config.NUMBER_OF_CHILDREN / 
                                    config.CHILDREN_PER_PAIR):
                a = random.random()
                #log.debug(a)
                for adult1 in self.adults:
                    if adult1.fitness_range[0] < a < adult1.fitness_range[1]:
                        b = random.random()
                        #log.debug(b)
                        for adult2 in self.adults:
                            if(adult2 != adult1 and
                                    adult2.fitness_range[0] < b and
                                    b < adult2.fitness_range[1]):
                                parents.append([adult1, adult2])
                                break
                        #log.debug(len(parents))
                        break
            #log.debug(parents)
            self.parents = parents

        # Tournament selection
        elif config.PARENT_SELECTION == "T":
            #log.debug("Tournament selection")
            while len(parents) < (config.NUMBER_OF_CHILDREN /
                                    config.CHILDREN_PER_PAIR):
                adult_pool = copy.deepcopy(self.adults)
                random.shuffle(adult_pool)
                tournament_groups = []
                for group in range(int(config.POPULATION_SIZE / 
                                        config.GROUP_SIZE)):
                    tournament_groups.append([])
                    for individual in range(config.GROUP_SIZE):
                        tournament_groups[group].append(adult_pool.pop())
                for group in tournament_groups:
                    a = random.random()
                    if a < (1 - config.EPSILON):
                        heapq.heapify(group)
                    parents.append([group[-1], group[-2]])
                    if not len(parents) < (config.NUMBER_OF_CHILDREN / 
                                            config.CHILDREN_PER_PAIR):
                        break
                #log.info(tournament_groups)
            self.parents = parents
        
        # Boltzmann scaling
        elif config.PARENT_SELECTION == "B":
            #log.info("Boltzmann scaling")
            total_fitness = 0
            boltzmann_list = []
            boltzmann_numerators = 0
            for adult in self.adults:
                boltzmann_numerators += (math.e**(adult.fitness/self.temperature))
            average_numerator = boltzmann_numerators / len(self.adults)
            for adult in self.adults:
                boltzmann_fitness = (math.e**(adult.fitness/self.temperature) /
                                    average_numerator)
                boltzmann_list.append(boltzmann_fitness)
                total_fitness += boltzmann_fitness
            #log.debug(boltzmann_list)
            temp_fitness = 0
            counter = 0
            for adult in self.adults:
                adult.fitness_range = (temp_fitness, temp_fitness +
                                        (boltzmann_list[counter]/total_fitness))
                temp_fitness += boltzmann_list[counter] / total_fitness
                counter += 1
                #log.debug(adult.fitness_range)
            while len(parents) < (config.NUMBER_OF_CHILDREN / 
                                    config.CHILDREN_PER_PAIR):
                a = random.random()
                #log.debug(a)
                for adult1 in self.adults:
                    if adult1.fitness_range[0] < a < adult1.fitness_range[1]:
                        b = random.random()
                        #log.debug(b)
                        for adult2 in self.adults:
                            if(adult2 != adult1 and
                                    adult2.fitness_range[0] < b and
                                    b < adult2.fitness_range[1]):
                                parents.append([adult1, adult2])
                                break
                        #log.debug(len(parents))
                        break
            #log.debug(parents)
            self.parents = parents
        else: log.warning("Parent selection error")

    def reproduce(self):
        children = []
        for parents in self.parents:
            if random.random() < config.CROSSOVER_RATE:
                for child in range(config.CHILDREN_PER_PAIR):
                    crossoverpoint = random.randrange(1, 
                                        len(parents[0].phenotype))
                    newborn = individual.Individual()
                    newborn.genotype = (copy.deepcopy(
                                        parents[0].phenotype[:crossoverpoint]) + 
                                        copy.deepcopy(
                                        parents[1].phenotype[crossoverpoint:]))
                    children.append(newborn)
            else:
                for child in range(config.CHILDREN_PER_PAIR):
                    parent = child % 2
                    newborn = individual.Individual()
                    if random.random() < config.MUTATION_RATE:
                        if config.MUTATION_TYPE == "G":
                            #log.debug("Genome mutation")
                            genotype = copy.deepcopy(parents[parent].phenotype)
                            index = random.randrange(0, len(genotype))
                            if genotype[index] == 0:
                                genotype[index] = 1
                            else: genotype[index] = 0
                            newborn.genotype = genotype
                        elif config.MUTATION_TYPE == "C":
                            log.debug("Genome component mutation")
                        else: log.warning("Mutation type error")
                    else:
                        newborn.genotype = parents[parent].phenotype
                    children.append(newborn)
        #log.debug(len(children))
        self.children = children
        for adult in self.adults:
            adult.grow()

    def generationInformation(self):
        total_fitness = 0
        number_of_adults = 0
        variance_numerator = 0
        variance = 0
        for adult in self.adults:
            total_fitness += adult.fitness
            number_of_adults += 1
        self.average_fitness = total_fitness / number_of_adults
        for adult in self.adults:
            variance_numerator += (adult.fitness - self.average_fitness)**2
        variance = variance_numerator / number_of_adults
        self.standard_deviation = variance**(1/2)

class LolzPopulation(Population):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
    def generateChildren(self): 
        children = []
        for child in range(config.NUMBER_OF_CHILDREN):
            newborn = individual.LolzIndividual()
            newborn.generateGenotype()
            children.append(newborn)
        #log.debug(children)
        return children

    def reproduce(self):
        children = []
        for parents in self.parents:
            if random.random() < config.CROSSOVER_RATE:
                for child in range(config.CHILDREN_PER_PAIR):
                    crossoverpoint = random.randrange(1, 
                                        len(parents[0].phenotype))
                    newborn = individual.LolzIndividual()
                    newborn.genotype = (copy.deepcopy(
                                        parents[0].phenotype[:crossoverpoint]) + 
                                        copy.deepcopy(
                                        parents[1].phenotype[crossoverpoint:]))
                    children.append(newborn)
            else:
                for child in range(config.CHILDREN_PER_PAIR):
                    parent = child % 2
                    newborn = individual.LolzIndividual()
                    if random.random() < config.MUTATION_RATE:
                        if config.MUTATION_TYPE == "G":
                            #log.debug("Genome mutation")
                            genotype = copy.deepcopy(parents[parent].phenotype)
                            index = random.randrange(0, len(genotype))
                            if genotype[index] == 0:
                                genotype[index] = 1
                            else: genotype[index] = 0
                            newborn.genotype = genotype
                        elif config.MUTATION_TYPE == "C":
                            log.debug("Genome component mutation")
                        else: log.warning("Mutation type error")
                    else:
                        newborn.genotype = parents[parent].phenotype
                    children.append(newborn)
        #log.debug(len(children))
        self.children = children
        for adult in self.adults:
            adult.grow()

class SurprisingPopulation(Population):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
    def generateChildren(self): 
        children = []
        for child in range(config.NUMBER_OF_CHILDREN):
            newborn = individual.SurprisingIndividual()
            newborn.generateGenotype()
            children.append(newborn)
        #log.debug(children)
        return children

    def reproduce(self):
        children = []
        for parents in self.parents:
            if random.random() < config.CROSSOVER_RATE:
                for child in range(config.CHILDREN_PER_PAIR):
                    crossoverpoint = random.randrange(1, 
                                        len(parents[0].phenotype))
                    newborn = individual.SurprisingIndividual()
                    newborn.genotype = (copy.deepcopy(
                                        parents[0].phenotype[:crossoverpoint]) + 
                                        copy.deepcopy(
                                        parents[1].phenotype[crossoverpoint:]))
                    children.append(newborn)
            else:
                for child in range(config.CHILDREN_PER_PAIR):
                    parent = child % 2
                    newborn = individual.SurprisingIndividual()
                    if random.random() < config.MUTATION_RATE:
                        if config.MUTATION_TYPE == "G":
                            #log.debug("Genome mutation")
                            genotype = copy.deepcopy(parents[parent].phenotype)
                            index = random.randrange(0, len(genotype))
                            genotype[index] = random.randrange(0, 
                                                            config.SYMBOL_SET)
                            newborn.genotype = genotype
                        elif config.MUTATION_TYPE == "C":
                            log.debug("Genome component mutation")
                        else: log.warning("Mutation type error")
                    else:
                        newborn.genotype = parents[parent].phenotype
                    children.append(newborn)
        #log.debug(len(children))
        self.children = children
        for adult in self.adults:
            adult.grow()
