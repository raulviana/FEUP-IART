from Classes import Photo, Slide

#Objective function to be maximized 
def ObjectiveFunction(slides):
       score = 0
       for i in range(len(slides)-1):
              shared = 0
              for tag in slides[i].tags:
                     if tag in slides[i+1].tags:
                            shared += 1

              exclusiveToFirst = len(slides[i].tags) - shared 
              exclusiveToSecond = len(slides[i+1].tags) - shared 
              score += min(shared, exclusiveToFirst, exclusiveToSecond)  

       return score