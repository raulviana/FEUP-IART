import random
import operator
import numpy as np
from Classes import Photo, Slide 
from objective import ObjectiveFunction
import time
from utils import generate_slides

def solveRand(photos):
    
    slides = []
    for photo in photos:
        if len(slides)==0:
            slides.append(Slide(photo))  
        elif not slides[-1].Horizontal and not photo.Horizontal:
            slides[-1].addVertical(photo)
        else:
            slides.append(Slide(photo))
    return slides



def transition_score(slide1, slide2):
    #common tags
    common = len(set(slide1.tags).intersection(slide2.tags))
    # tags in photo1 but not in 2
    uncommon_slide1 = len(slide1.tags) - common
    # tgs in photo2 but not in 1´
    uncommon_slide2 = len(slide2.tags) - common
    return min(common, uncommon_slide1, uncommon_slide2)


def hill(photos, cycles, local_size):
    import time
    cycles_asked = cycles
    start_time = time.process_time()
    best_score = 0
    first_index = 0
    second_index = 0
    #start random solution
    slides = generate_slides(photos)
    length = len(slides)
    if length <= local_size:
        print("Caution, local search size is equal or greater than the number of slides")
    #get the scores of first soluton
    for i in range(0, length -1):
        slides[i].score = transition_score(slides[i], slides[i+1])
        best_score += slides[i].score
    #searches for the optimal solution
    while cycles > 0:
        first_index = random.randint(0, length - 2)
        for i in range(first_index - local_size, first_index + local_size):
            second_index = i
            if first_index >= length - 2:
                first_index = 1
            if second_index > (length - 2) or second_index < 0 or first_index == second_index:
                continue
            current_transitions = sum([transition_score(slides[first_index - 1], slides[first_index]), 
                                transition_score(slides[first_index], slides[first_index + 1]),
                                transition_score(slides[second_index - 1], slides[second_index]), 
                                transition_score(slides[second_index], slides[second_index + 1])])
            #new transitions with slides swaped
            temp_tansitions = sum([transition_score(slides[first_index - 1], slides[second_index]), 
                                transition_score(slides[second_index], slides[first_index + 1]),
                                transition_score(slides[second_index - 1], slides[first_index]), 
                                transition_score(slides[first_index], slides[second_index + 1])])
            if(temp_tansitions > current_transitions):
                #apply new configuration
                slides[first_index], slides[second_index] = slides[second_index], slides[first_index]
                #calculate new score
                best_score += temp_tansitions - current_transitions
                break
        cycles -= 1
        if cycles % 1000 == 0:
            print("Cycles left: ", cycles)
            print(best_score)
    print("--------------------")
    print("Hill Climbing")
    print(" ")
    print("Score: ", best_score) 
    print("With ", cycles_asked, " cycles")
    time = time.process_time() - start_time
    print("In %.3f seconds of processor time" % time)
    return best_score, time