from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import time
from Classes import Photo, Slide
from objective import ObjectiveFunction
import ntpath
from tkinter import messagebox


from simulated_annealing import simulated_annealing
from tabu_search import tabu_search
from hill_climbing import hill
from solveRand import solveRand
from genetic_algorithm import geneticStartup
from utils import outputSolution

def loadFile():
    f = open(filename, 'r')
    global photos
    lineNumber = 0
    for line in f:
        if (lineNumber != 0):
            photos.append(Photo(lineNumber-1, line))
        lineNumber += 1
    messagebox.showinfo("Loaded", "File Loaded")

def solve_rand(photos):
    score = solveRand(photos)


def solveHillClimbing(*args):
    outputSolution(hill(args[0], args[1], args[2]))
    return 0


def solveGeneticAlgorithm(*args):
    outputSolution(geneticStartup(args[0], args[1], args[2], args[3], args[4]))
    return 0


def solveTabuSearch(*args):
    outputSolution(tabu_search(photos))
    return 0

def solveSimulatedAnneling(*args):
    outputSolution(simulated_annealing(args[0], args[1], args[2], args[3], args[4]))
    return 0


def fileLoaded(*args):

    ttk.Label(mainframe, text="Choose algorithm:").grid(column=1, row=8, sticky=(W))
    ttk.Button(mainframe, text="Random Solution", command= lambda: solveRand(photos)).grid(column=1, row=10, sticky=W)
    ttk.Button(mainframe, text="Genetic Algorithm", command=lambda: solveGeneticAlgorithm(photos, Gen_generations.get(), Gen_sol_per_gen.get(), Gen_crossover.get(), Gen_mutation.get())).grid(column=1, row=14, sticky=W)
    ttk.Button(mainframe, text="Simulated Anneling", command= lambda: solveSimulatedAnneling(photos, SA_temp.get(), SA_min_temp.get(), SA_cool_rate.get(), SA_it_per_temp.get())).grid(column=1, row=16, sticky=W)
    ttk.Button(mainframe, text="Tabu Search", command= lambda: solveTabuSearch(photos)).grid(column=1, row=18, sticky=W)
    ttk.Button(mainframe, text="Hill Climbing", command= lambda: solveHillClimbing(photos, hill_cycles.get(), hill_local_size.get())).grid(column=1, row=20, sticky=W)
   
    ttk.Label(mainframe, text="Cycles: ").grid(column=2, row=20,  sticky=E)
    ttk.Label(mainframe, text="Search Size: ").grid(column=4, row=20,  sticky=E)
    ttk.Label(mainframe, text="Temperature: ").grid(column=2, row=16,  sticky=E)
    ttk.Label(mainframe, text="Min Temperature: ").grid(column=4, row=16,  sticky=E)
    ttk.Label(mainframe, text="Cooling Rate: ").grid(column=6, row=16,  sticky=E)
    ttk.Label(mainframe, text="Iter per Temperature: ").grid(column=8, row=16,  sticky=E)
    ttk.Label(mainframe, text="Generations: ").grid(column=2, row=14,  sticky=E)
    ttk.Label(mainframe, text="Solution per generation: ").grid(column=4, row=14,  sticky=E)
    ttk.Label(mainframe, text="Crossover: ").grid(column=6, row=14,  sticky=E)
    ttk.Label(mainframe, text="Mutation Probability: ").grid(column=8, row=14,  sticky=E)


    #--------hil_climbing variables-------
    hill_entry = ttk.Entry(mainframe, textvariable=hill_cycles, width=9)
    hill_cycles.set('50000')
    hill_entry.grid(column=3, row=20,  sticky=W)

    hill_local_entry = ttk.Entry(mainframe, textvariable=hill_local_size, width=4)
    hill_local_size.set('50')
    hill_local_entry.grid(column=5, row=20,  sticky=W)
    #------------------------------------

    #-----------------Simulated Annealing variables---------------------
    SA_temperature_entry = ttk.Entry(mainframe, textvariable=SA_temp, width=5)
    SA_temp.set('1000')
    SA_temperature_entry.grid(column=3, row=16,  sticky=W)

    SA_min_temperature_entry = ttk.Entry(mainframe, textvariable=SA_min_temp, width=5)
    SA_min_temp.set('1')
    SA_min_temperature_entry.grid(column=5, row=16,  sticky=W)

    SA_cool_rate_entry = ttk.Entry(mainframe, textvariable=SA_cool_rate, width=5)
    SA_cool_rate.set('5')
    SA_cool_rate_entry.grid(column=7, row=16,  sticky=W)

    SA_iter_p_Temp_entry = ttk.Entry(mainframe, textvariable=SA_it_per_temp, width=5)
    SA_it_per_temp.set('10')
    SA_iter_p_Temp_entry.grid(column=9, row=16,  sticky=W)
    #-------------------------------------------------------------------------

    #--------------------Genetic Algorithm Variables------------------------
    Gen_generations_entry = ttk.Entry(mainframe, textvariable=Gen_generations, width=6)
    Gen_generations.set('100')
    Gen_generations_entry.grid(column=3, row=14,  sticky=W)

    Gen_Solution_per_gen_entry = ttk.Entry(mainframe, textvariable=Gen_sol_per_gen, width=4)
    Gen_sol_per_gen.set('50')
    Gen_Solution_per_gen_entry.grid(column=5, row=14,  sticky=W)

    Gen_crossover_entry = ttk.Entry(mainframe, textvariable=Gen_crossover, width=4)
    Gen_crossover.set('5')
    Gen_crossover_entry.grid(column=7, row=14,  sticky=W)

    Gen_mutation_entry = ttk.Entry(mainframe, textvariable=Gen_mutation, width=4)
    Gen_mutation.set('0.03')
    Gen_mutation_entry.grid(column=9, row=14,  sticky=W)
    #-----------------------------------------------------------------------

root = Tk()

#input variables
hill_cycles = IntVar()
hill_local_size = IntVar()
SA_temp = IntVar()
SA_min_temp = IntVar()
SA_cool_rate = IntVar()
SA_it_per_temp = IntVar()
Gen_generations = IntVar()
Gen_sol_per_gen = IntVar()
Gen_crossover = IntVar()
Gen_mutation = DoubleVar()


root.title("Google Hashcode 2019 solver  ")
filename = askopenfilename()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)	

ttk.Label(mainframe, text="Input file:").grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, text=ntpath.basename(filename)).grid(column=1, row=4, sticky=(W, E))

photos = []
ttk.Button(mainframe, text="Load File", command= loadFile).grid(column=1, row=5, sticky=W)
fileLoaded()
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
