import numpy as np
from deap import base, creator, benchmarks

from deap import algorithms
from deap.tools._hypervolume import hv
import matplotlib.pyplot as plt

import random
from deap import tools

# ne pas oublier d'initialiser la grane aléatoire (le mieux étant de le faire dans le main))
random.seed()

def summary(n,nbgen, evaluate, IND_SIZE,ntry):

    stats = np.array([my_nsga2(n,nbgen, evaluate, IND_SIZE=IND_SIZE) for i in range(ntry)])

    values = []

    moyenne = []
    fit_25 = []
    fit_75 = []

    gen = range(nbgen)

    for t in range(ntry):
        values.append(stats[t,2])

    moyenne = np.mean(values,axis=0)
    fit_25 = np.quantile(values,0.25,axis=0)
    fit_75 = np.quantile(values,0.75,axis=0)


    plt.plot(gen,moyenne, label="Fitness moyenne")
    plt.fill_between(gen, fit_25, fit_75, alpha=0.25, linewidth=0)
    plt.show()

def my_nsga2(n, nbgen, evaluate, ref_point=np.array([1,1]), IND_SIZE=5, weights=(-1.0, -1.0)):
    """NSGA-2

    NSGA-2
    :param n: taille de la population
    :param nbgen: nombre de generation
    :param evaluate: la fonction d'évaluation
    :param ref_point: le point de référence pour le calcul de l'hypervolume
    :param IND_SIZE: la taille d'un individu
    :param weights: les poids à utiliser pour la fitness (ici ce sera (-1.0,) pour une fonction à minimiser et (1.0,) pour une fonction à maximiser)
    """

    creator.create("MaFitness", base.Fitness, weights=weights)
    creator.create("Individual", list, fitness=creator.MaFitness)


    toolbox = base.Toolbox()
    paretofront = tools.ParetoFront()

    toolbox = base.Toolbox()

    # à compléter pour sélectionner les opérateurs de mutation, croisement, sélection avec des toolbox.register(...)

    hof = tools.HallOfFame(1)

    toolbox.register("attr_float", np.random.uniform,-5,5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mutate",tools.mutPolynomialBounded,eta=15,low=-5,up=5,indpb=0.2)
    toolbox.register("crossover",tools.cxSimulatedBinaryBounded,eta=15,low=-5,up=5)
    toolbox.register("select",tools.selNSGA2)
    toolbox.register("evaluate",evaluate)

    # Les statistiques permettant de récupérer les résultats
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("1q",np.quantile,q=0.25)
    stats.register("3q",np.quantile,q=0.75)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop = toolbox.population(n)

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    paretofront.update(pop)

    CXPB, MUTPB = 0.5, 0.2

    # Pour récupérer l'hypervolume, nous nous contenterons de mettre les différentes valeur dans un vecteur s_hv qui sera renvoyé par la fonction.
    pointset=[np.array(ind.fitness.getValues()) for ind in paretofront]
    s_hv=[hv.hypervolume(pointset, ref_point)]

    # Begin the generational process
    for gen in range(1, nbgen):

        offspring = toolbox.select(pop,len(pop))
        offspring = list(map(toolbox.clone,offspring))

        for child1, child2 in zip(offspring[::2],offspring[1::2]):
            if random.random() < CXPB:
                toolbox.crossover(child1,child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        paretofront.update(pop)
        pointset=[np.array(ind.fitness.getValues()) for ind in paretofront]
        s_hv.append(hv.hypervolume(pointset, ref_point))

    return pop, paretofront, s_hv
