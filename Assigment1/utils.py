from Classes import *
from datetime import datetime


#Retorna array de slides com slides horizontais e verticais.
def generate_slides(photos):
    slides = []
    vertical_photos = []

    for photo in photos:
        if photo.Horizontal:
            slides.append(Slide(photo))
        else:
            vertical_photos.append(photo)

    sortedvPhotos = sort_vertical_photos(vertical_photos)

    vertical_slides = pair_vPhotosFrontBack(sortedvPhotos)

    for vs in vertical_slides:
        slides.append(vs)

    return slides

#Emparelha as fotos verticais com menor numero de tags com as fotos verticais com maior numero de tags. Retorna lista de slides.
def pair_vPhotosFrontBack(vPhotos):
    slides = []
    length = len(vPhotos)

    if length == 0:
        return []
    elif length == 2:
        s = Slide(vPhotos[0])
        s.addVertical(vPhotos[1])
        return [s]
    elif ((length % 2) == 0):
        l = length//2
        for idx in range(l):
               s1 = Slide(vPhotos[idx])
               s1.addVertical(vPhotos[length-idx-1]) #match primeiro com o ultimo
               slides.append(s1)

    else: #eliminar a foto que tem menos tags (neste caso a primeira)
        print("One pic will be left out.")
        vPhotos.pop(0)

        length=length-1
        l = length//2
        for idx in range(l):
               s1 = Slide(vPhotos[idx])
               s1.addVertical(vPhotos[length-idx-1]) #match primeiro com o ultimo
               slides.append(s1)
    return slides

#Ordena as fotografias verticais pelo numero de tags
def sort_vertical_photos(vPhotos):
    v_sorted = sorted(vPhotos, key=lambda x: x.nr_tags, reverse=False) #ordenar por ordem crescente de nr de tags
    return v_sorted


def outputSolution(Slides):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    f = open("output/solution" + dt_string +".txt", "w+")
    for Slide in Slides:
        f.write(Slide.generateOutput() +"\n")
    f.close()
    return