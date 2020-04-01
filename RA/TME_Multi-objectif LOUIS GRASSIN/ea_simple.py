import numpy as np
from deap import base, creator, benchmarks

import random
from deap import tools

import matplotlib.pyplot as plt

# ne pas oublier d'initialiser la grane aléatoire (le mieux étant de le faire dans le main))
random.seed()

def summary(n,nbgen, evaluate, IND_SIZE,ntry, weights=(-1.0,)):

    stats = np.array([ea_simple(n,nbgen, evaluate, IND_SIZE,weights) for i in range(ntry)])

    moyenne = []
    fit_25 = []
    fit_75 = []

    gen = range(nbgen)

    for t in range(ntry):
        moyenne.append(stats[t,2].select('avg'))
        fit_25.append(stats[t,2].select('1q'))
        fit_75.append(stats[t,2].select('3q'))

    moyenne = np.mean(moyenne,axis=0)
    fit_25 = np.mean(fit_25,axis=0)
    fit_75 = np.mean(fit_75,axis=0)


    plt.plot(gen,moyenne, label="Fitness moyenne")
    plt.fill_between(gen, fit_25, fit_75, alpha=0.25, linewidth=0)
    plt.show()

def ea_simple(n, nbgen, evaluate, IND_SIZE, weights=(-1.0,)):
    """Algorithme evolutionniste elitiste

    Algorithme evolutionniste elitiste.
    :param n: taille de la population
    :param nbgen: nombre de generation
    :param evaluate: la fonction d'évaluation
    :param IND_SIZE: la taille d'un individu
    :param weights: les poids à utiliser pour la fitness (ici ce sera (-1.0,) pour une fonction à minimiser et (1.0,) pour une fonction à maximiser)
    """

    creator.create("MaFitness", base.Fitness, weights=weights)
    creator.create("Individual", list, fitness=creator.MaFitness)


    toolbox = base.Toolbox()

    # à compléter pour sélectionner les opérateurs de mutation, croisement, sélection avec des toolbox.register(...)

    toolbox.register("attr_float", random.uniform,-5,5)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mutate",tools.mutPolynomialBounded,eta=15,low=-5,up=5,indpb=0.2)
    toolbox.register("crossover",tools.cxSimulatedBinary,eta=15)
    toolbox.register("select",tools.selTournament,tournsize=3)
    toolbox.register("evaluate",evaluate)

    # Les statistiques permettant de récupérer les résultats
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("1q",np.quantile,q=0.25)
    stats.register("3q",np.quantile,q=0.75)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # La structure qui permet de stocker les statistiques
    logbook = tools.Logbook()


    # La structure permettant de récupérer le meilleur individu
    hof = tools.HallOfFame(1)


    ## à compléter pour initialiser l'algorithme, n'oubliez pas de mettre à jour les statistiques, le logbook et le hall-of-fame.

    pop = toolbox.population(n)

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    record = stats.compile(pop)
    logbook.record(gen=0,fit=np.array(fitnesses)[:,0],**record)

    CXPB, MUTPB = 0.5, 0.2

    for g in range(1,nbgen):

        
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

        record = stats.compile(pop)
        logbook.record(gen=g,**record)

        hof.update(pop)

    return pop, hof, logbook
