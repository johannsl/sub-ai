import logging
from matplotlib import pyplot
from matplotlib import patches

log = logging.getLogger(__name__)

def createPlot(generations, best_values, average_values, standard_deviations):
    log.info("Creating plot")
    best_patch = patches.Patch(color="blue", label="Best values")
    
    # Labels
    average_patch = patches.Patch(color="red", label="Average values")
    sd_patch = patches.Patch(color="yellow", label="Standard deviations")
    pyplot.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                    ncol=3, mode="expand", borderaxespad=0.,
                    handles=[best_patch, average_patch, sd_patch])
    
    # Plots
    pyplot.plot(generations, best_values, "b", linewidth=2.0)
    pyplot.plot(generations, average_values, "r", linewidth=2.0)
    pyplot.plot(generations, standard_deviations, "y", linewidth=2.0)
    pyplot.show()
