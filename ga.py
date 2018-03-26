import random

# keep the cities distances (dict of dict)
cities_distances = {}

# read the file with the cities distances
def readFile():
    file = open('input-file', 'r')
    
    for line in file:
        line_arr = line.split(' ')
        city_from = line_arr[0]
        city_to = line_arr[1]
        distance = line_arr[2]

        if city_from in cities_distances:
            cities_distances[city_from][city_to] = float(distance)
        else:
            cities_distances[city_from] = { city_to: float(distance) }

        if city_to in cities_distances:
            cities_distances[city_to][city_from] = float(distance)
        else:
            cities_distances[city_to] = { city_from: float(distance) }

    #for e in cities_distances:
    #    for i in cities_distances[e]:
    #        print e + ' ' + i['name'] + ' ' + str(i['distance']) 
    
    #print cities_distances
    # if ('A' in cities_distances):
    #     if ('B' in cities_distances['A']):
    #         print cities_distances['A']['B']

class cities_tour:  
    def randonizeCities(self):
        for city in cities_distances:
            self.cities.append(city)

        random.shuffle(self.cities)

    def fitness(self):
        total_distance = 0

        for i in range(1, len(self.cities)):
            city_from = self.cities[i - 1]
            city_to = self.cities[i]
            total_distance += cities_distances[city_from][city_to]

        return total_distance

    def __str__(self):
        return str(self.cities)

    def __init__(self):
        self.cities = []
        self.randonizeCities()

class population:
    def getFittest(self):
        fittest = self.tours[0]
        for tour in self.tours[1:]:
            if tour.fitness() < fittest.fitness():
                fittest = tour
        return fittest

    def appendTour(self, tour):
        if len(self.tours) < self.size:
            self.tours.append(tour)

    def appendTours(self, tours):
        if len(self.tours) + len(tours) <= self.size:
            self.tours.extend(tours)

    def __init__(self, size, initalize):
        self.tours = []
        self.size = size
        if initalize == True:
            for i in range(0, size):
                city_tour = cities_tour()
                self.tours.append(city_tour)

class ga:
    mutation_rate = 0.1
    tournament_size = 4
    elitism = True

    def mutate(self, tour):
        cities = tour.cities

        for city1 in cities:
            if random.random() < ga.mutation_rate:
                city2 = random.choice(cities)
                
                city1_index = cities.index(city1)
                city2_index = cities.index(city2)

                tour.cities[city1_index] = city2
                tour.cities[city2_index] = city1

    def crossover(self, parent_1, parent_2):         
        return parent_1

    def tournament_selection(self, pop):
        tours_sample = random.sample(pop.tours, ga.tournament_size)
        tournament_population = population(pop.size, False)
        tournament_population.appendTours(tours_sample)

        return tournament_population.getFittest()

    def evolve_population(self, pop, size):
        new_population = population(size, False)

        elitism_offset = 0
        if ga.elitism:
            fittest_tour = pop.getFittest()
            new_population.appendTour(fittest_tour)
            elitism_offset = 1

        for i in range(elitism_offset, size):
            tour_parent_1 = self.tournament_selection(pop)
            tour_parent_2 = self.tournament_selection(pop)

            tour_child = self.crossover(tour_parent_1, tour_parent_2)

            new_population.appendTour(tour_child)
        
        for tour in new_population.tours:
            self.mutate(tour)

        return new_population


if "__main__":
    readFile()
    pop = population(5, True)
    # for t in a.tours:
    #     print t

    # print 'fittest'
    # print a.getFittest()

    print 'initial distance'
    print pop.getFittest()
    print pop.getFittest().fitness()

    _ga = ga()

    for i in range(0, 300):
        pop = _ga.evolve_population(pop, 5)
        print 'step ' + str(i) +  ' distance = ' + str(pop.getFittest())
        #print pop.getFittest()
        print pop.getFittest().fitness()

    print 'the final population is: ' + str(pop.getFittest())
    print 'the final fitness is: ' + str(pop.getFittest().fitness())
