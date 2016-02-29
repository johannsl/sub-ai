from utils import config
import logging
import random

log = logging.getLogger(__name__)

class Individual(object):
    def __init__(self, *args, **kwargs):
        #log.debug("Individual init")
        self.adult = False
        self.age = 0
        self.genotype = None
        self.phenotype = None
        self.fitness = None
        self.fitness_range = None

    def __lt__(self, other):
        return self.fitness < other.fitness

    def mature(self):
        self.adult = True

    def grow(self):
        self.age += 1

    def generateGenotype(self):
        genotype = []
        for binary in range(config.GENOTYPE_LENGTH):
            genotype.append(random.randrange(0, 2))
        #log.debug(genotype)
        self.genotype = genotype

    def generatePhenotype(self):
        phenotype = []
        for binary in self.genotype:
            phenotype.append(binary)
        #log.debug(phenotype)
        self.phenotype = phenotype

    def evaluateFitness(self):
        fitness = 0
        for number in self.phenotype:
            fitness += number
        #log.debug(fitness)
        self.fitness = fitness

class LolzIndividual(Individual):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.z_value = config.Z_VALUE
        
    def evaluateFitness(self):
        fitness = 1
        counter = 1
        if self.phenotype[0] == 0:
            while counter < len(self.phenotype) and self.phenotype[counter] == 0:
                fitness += 1
                counter +=1
            if self.z_value < fitness:
                fitness = self.z_value
        elif self.phenotype[0] == 1:
            while counter < len(self.phenotype) and self.phenotype[counter] == 1:
                fitness += 1
                counter +=1
        #log.info(self.phenotype)
        #log.info(fitness)
        self.fitness = fitness

class SurprisingIndividual(Individual):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
    def generateGenotype(self):
        genotype = []
        for symbol in range(config.GENOTYPE_LENGTH):
            genotype.append(random.randrange(0, config.SYMBOL_SET))
        #log.debug(genotype)
        self.genotype = genotype

    def generatePhenotype(self):
        phenotype = []
        for symbol in self.genotype:
            phenotype.append(symbol)
        #log.debug(phenotype)
        self.phenotype = phenotype

    def evaluateFitness(self):
        fitness = config.SURPRISING_FITNESS
        if config.SEQUENCE_TYPE == "G":
            #log.info("Global sequence type")
            pair_list = []
            for symbol1 in range(len(self.phenotype)):
                for symbol2 in range(symbol1+1, len(self.phenotype)):
                    pair_list.append([self.phenotype[symbol1], 
                                    self.phenotype[symbol2], 
                                    symbol2-symbol1-1])
            for pair1 in range(len(pair_list)):
                for pair2 in range(pair1+1, len(pair_list)):
                    if pair_list[pair1] == pair_list[pair2]: fitness -= 1
            #log.info(self.phenotype)
            #log.info(pair_list)
            #log.info(fitness)
            
        elif config.SEQUENCE_TYPE == "L":
            #log.info("Local sequence type")
            pair_list = []
            for symbol1 in range(len(self.phenotype)-1):
                pair_list.append([self.phenotype[symbol1],
                                self.phenotype[symbol1+1]])
            for pair1 in range(len(pair_list)):
                for pair2 in range(pair1+1, len(pair_list)):
                    if pair_list[pair1] == pair_list[pair2]: fitness -= 1
                         
        else: log.warning("Sequence type error")
        self.fitness = fitness
