
from objective import *
from utils import *

def tabu_search(photos):
    import time
    start_time = time.process_time()
    slides = generate_slides(photos)

    last = []
    solution = []
    current = slides.pop()
    solution.append(current)

    it = 0
    while it < len(slides):
        #obtem lista de candidatos com tags em comum com o current slide
        neighborhood = getCandidates(current, slides, solution, last)

        #seleciona a melhor opcao
        bestMatch = selectSolution(current, neighborhood)

        if bestMatch == -1: #current nao tem tags em comum com nada, fica para ultimo
            last.append(current)
            print(len(last))

        else: #update tabu memory and make the move
            solution.append(bestMatch)
            current = bestMatch

        it = it + 1

    solution = solution + last
    score = ObjectiveFunction(solution)
    print("--------------------")
    print("Tabu Search")
    print(" ")
    print("Score: ", score)
    time = time.process_time() - start_time
    print("In %.3f seconds of processor time" % time)
    return solution

#Seleciona o slide que maximiza a transicao entre o slide atual e os possiveis candidatos. Retorna o slide escolhido
def selectSolution(comparable, neighborhood):
    maxPoints = 0
    selected = -1

    for s in neighborhood:
        if len(s.tags) > 2*maxPoints:
            points = s.interest(comparable)
            if points > maxPoints:
                maxPoints = points
                selected = s

    return selected

#Retorna uma lista dos slides com tags em comum com o slide atual.
def getCandidates(slide, slides, cantMatch, haveNoMatch):
    candidates = []

    canSearch = list(set(slides) ^ set(cantMatch) ^ set(haveNoMatch))

    for s in canSearch:
        if len(slide.tags.intersection(s.tags)) > 0: #slides com tags em comum
            if slides != s:
                candidates.append(s)

    return candidates
