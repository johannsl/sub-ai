# Python 3

import logging
import logging.config
from utils import config
from utils import individual
from utils import plot
from utils import population

def main():
    # Logging
    logging.config.dictConfig(config.LOG_CONFIG)
    log = logging.getLogger(__name__)
    
    # Plot data
    generations = []
    best_values = []
    average_values = []
    standard_deviations = []

    # Run evolutionary loop
    log.debug("\n\n\n")
    log.info("#### RUN EVOLUTIONARY LOOP ####")
    if config.POPULATION_TYPE == "O":
        popula = population.Population()
    elif config.POPULATION_TYPE == "L":
        popula = population.LolzPopulation()
    elif config.POPULATION_TYPE == "S":
        popula = population.SurprisingPopulation()

    for i in range(config.NUMBER_OF_GENERATIONS):
        log.info(("Iteration #:", i))
        popula.develop()
        popula.evaluate()
        popula.adultSelection()
        popula.parentSelection()
        popula.reproduce()
        
        # Log information
        highest_fitness = 0
        fittest_adult = None
        for adult in popula.adults:
            if highest_fitness < adult.fitness:
                highest_fitness = adult.fitness
                fittest_adult = adult
        log.info(("Highest fitness:", highest_fitness))
        log.info(("Average fitness:", popula.average_fitness))
        log.info(("Standard deviation:", popula.standard_deviation))
        log.info(("Fittest phenotype:", fittest_adult.phenotype))
        
        # Plot information
        generations.append(i)
        best_values.append(highest_fitness)
        average_values.append(popula.average_fitness)
        standard_deviations.append(popula.standard_deviation)
    
    # Create plot
    plot.createPlot(generations, best_values, average_values, 
                    standard_deviations)

if __name__ == "__main__":
    main()
