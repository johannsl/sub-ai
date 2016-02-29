import os

# Population types are O(ne-Max), L(OLZ), and S(urprising sequences)
POPULATION_TYPE = "S" 
NUMBER_OF_GENERATIONS = 200
POPULATION_SIZE = 100

# NUMBER_OF_CHILDREN > POPULATION_SIZE should use Over-production repl.
NUMBER_OF_CHILDREN = 100
GENOTYPE_LENGTH = 21

# Adult selections are F(ull generation replacement), 
# O(ver-production replacement), or G(eneration mixing)
ADULT_SELECTION = "G"

# Parent selections are F(itness-proportionate), S(igma-scaling), 
# T(ournament selection), or B(oltzmann scaling)
PARENT_SELECTION = "T"

# Tournament selection variables
EPSILON = 0.2
GROUP_SIZE = 10

# Boltzmann scaling variables
TEMPERATURE = 1 #* (10**4)
DELTA_T = TEMPERATURE / NUMBER_OF_GENERATIONS
TEMPERATURE += DELTA_T

CROSSOVER_RATE = 0.01
CHILDREN_PER_PAIR = 1

# Mutation types are per G(enome), [or per genome C(omponent) #TODO]
MUTATION_TYPE = "G" 
MUTATION_RATE = 1

# LOLZ problem variable
Z_VALUE = 30

# Surprising sequence variables
# Sequence types are G(lobal), or L(ocal)
SEQUENCE_TYPE = "G"
SYMBOL_SET = 9
SURPRISING_FITNESS = 20

# Logging config
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": os.path.join(os.path.dirname(__name__), "debug.log"),
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 1,
        }
    },
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s"
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        }
    }
}
