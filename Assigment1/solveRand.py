
from Classes import Photo, Slide
from objective import ObjectiveFunction

def solveRand(photos):
    import time
    start_time = time.process_time()
    slides = []
    for photo in photos:
        if len(slides)==0:
            slides.append(Slide(photo))  
        elif not slides[-1].Horizontal and not photo.Horizontal:
            slides[-1].addVertical(photo)
        else:
            slides.append(Slide(photo))
    score = ObjectiveFunction(slides) 
    time = time.process_time() - start_time
    print("--------------------")
    print("Random Algorithm")
    print(" ")
    print("Score: ", score)
    print("In %.3f seconds of processor time" % time)
    return slides, score

