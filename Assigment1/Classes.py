class Photo:
       def __init__(self, id, info):
              splitInfo = info.split()
              self.id = id
              self.Horizontal = True if splitInfo[0] == "H" else False
              self.tags = set(splitInfo[2::])
              self.nr_tags = len(self.tags)

class Slide:
       def __init__(self, photo):
              self.photo1 = photo.id
              self.photo2 = None
              self.tags = photo.tags
              self.points = 0
              self.Horizontal = photo.Horizontal
              self.taglength = len(photo.tags)

       def addVertical(self, photo):
              if photo.Horizontal:
                     print("Slide is Full")
                     exit("Tried to add a photo to a slide that was full")
              else:
                     self.photo2 = photo.id
                     self.tags.update(photo.tags)

       def generateOutput(self):
              if self.Horizontal:
                     return str(self.photo1)
              else:
                     return str(self.photo1) + " " + str(self.photo2)

       def getNrTags(self):
              return len(self.tags)

       def interest(self, other):
              shared = len(self.tags.intersection(other.tags))
              only_self = self.getNrTags() - shared
              only_other = other.getNrTags() - shared

              return min(shared, only_self, only_other)


