import math
import random
import numpy as np
import heapq
from objective import ObjectiveFunction
from Classes import *

#Dependencies: Numpy 

#To Avoid repetition we will use:
#For the crossover -> Ordered Crossover (OX1)
#https://www.researchgate.net/publication/2268568_On_Genetic_Crossover_Operators_for_Relative_Order_Preservation
#For the mutation -> Reverse Sequence Mutation (RSM). (PSM and HPRM if we have time)
#https://www.researchgate.net/publication/282732991_A_New_Mutation_Operator_for_Solving_an_NP-Complete_Problem_Travelling_Salesman_Problem

def genInitialPop(arrayLen, nSol):
       gen1 = []
       for i in range (0,nSol):
              individual = list(range(0, arrayLen-1))
              random.shuffle(individual)
              gen1.append(individual)
       return gen1

def geneticStartup(photos, generations, solutions, reproduction_size, mutation_probability):
       import time
       start_time = time.process_time()
       nGen = generations
       nSol = solutions
       if nSol % 2:
              nSol += 1
       poolSize = reproduction_size
       mutProb = mutation_probability
       fitness = []
       trace = None
       f = open("output/GAtrace.txt", "w+")
       for i in range(0,nGen):
              if i == 0:
                     population = genInitialPop(len(photos), nSol)
              else:
                     population = reproduce(population, fitness, poolSize)
                     population = mutate(population, mutProb)
              fitness = calculateFitness(population, photos)
              trace = "Generation: " + str(i) +" Best Individual: " + str(max(fitness))+"\n"
              f.write(trace)
              print(trace)
       f.close()
       print("--------------------")
       print("Genetic Algorithm")
       print(" ")
       print("Score: ", max(fitness))
       time = time.process_time() - start_time
       print("In %.3f seconds of processor time" % time)
       return SlidesFromIndividual(photos, population[fitness.index(max(fitness))])

def calculateFitness(population, photos):
    fitness = []           
    for individual in population:
       slides = []
       for photo in individual:
        if len(slides)==0:
            slides.append(Slide(photos[photo]))  
        elif not slides[-1].Horizontal and not photos[photo].Horizontal:
            slides[-1].addVertical(photos[photo])
        else:
            slides.append(Slide(photos[photo]))
       fitness.append(ObjectiveFunction(slides))
       
    return fitness


def reproduce(population, fitness, poolSize):
       newPopulation = []
       minFitness = min(fitness) 
       probability = [i - (minFitness) for i in fitness]
       #Subtracting the min fitness to avoid all probabilities being very similar when solution values are high and close
       
       poolIndices, poolProbability = selectPool(probability, poolSize)
       
       if sum(poolProbability) == 0:
              poolProbability = [1/len(poolProbability) for i in poolProbability] #Avoiding getting stuck in an "all soutions have fitness = 0" situation
       
       else:
              poolProbability = [float(i)/sum(poolProbability) for i in poolProbability] # Normalizing porbability for random.choice
       
       for i in range(0, len(population)//2):

              parents = np.random.choice(poolIndices, 2, replace=False, p=poolProbability)

              child1, child2 = OX1(population[parents[0]],population[parents[1]])
              
              newPopulation.append(child1)
              newPopulation.append(child2)

       return newPopulation

       
def mutate(population, mutProb):
       for individual in population:
              if random.uniform(0, 1) < mutProb:
                     mutationPoints = np.random.choice(len(individual), 2, replace=False)
                     individual[mutationPoints[0]], individual[mutationPoints[1]] =  individual[mutationPoints[1]], individual[mutationPoints[0]]

       return population    
       


def selectPool(probability, poolSize):

       if  2 >= poolSize >= len(probability):
              return list(range(0, len(probability))), probability
       else:
              poolIndices = heapq.nlargest(poolSize, range(len(probability)), probability.__getitem__)
              poolProbability = [probability[i] for i in poolIndices]
              return poolIndices, poolProbability



def OX1(parent1, parent2):

       crossoverPoints = np.random.choice(len(parent1), 2, replace=False)

       crossoverPoint1 = min(crossoverPoints)
       crossoverPoint2 = max(crossoverPoints)

       child1 = OX1aux(parent1, parent2, crossoverPoint1, crossoverPoint2)
       child2 = OX1aux(parent2, parent1, crossoverPoint1, crossoverPoint2)

       return child1, child2

def OX1aux(parent1, parent2, crossoverPoint1, crossoverPoint2):

       lenght = len(parent1)
       child = [None]*lenght
       index = crossoverPoint2
       for i in range(crossoverPoint1, crossoverPoint2):

              child[i] = parent1[i]
       
       for gene in parent2:
              if index >= lenght: 
                     index = 0
              if gene not in child:
                     child[index] = gene
                     index += 1

       return child


def SlidesFromIndividual(photos, individual):
       slides = []
       for photo in individual:
              if len(slides)==0:
                     slides.append(Slide(photos[photo]))  
              elif not slides[-1].Horizontal and not photos[photo].Horizontal:
                     slides[-1].addVertical(photos[photo])
              else:
                     slides.append(Slide(photos[photo]))
       
       return slides