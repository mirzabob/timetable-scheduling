import random
import copy


class Scheduler:
    def __init__(self, rooms,
                 classes):  # classes=[class], class={group,subject,teacher,no of periods per week}, rooms=[list of room strings]

        self.rooms = rooms
        self.grouplist = []
        self.classgroups = classes
        self.timeTable = []
        self.dictionary = {}
        self.no_of_days = 5
        self.no_of_periods = 8
        self.no_of_rooms = len(rooms)
        self.population = []
        self.w1 = 1000
        self.w2 = 100
        self.group = []
        self.teacher = []
        self.subject = []
        for single_class in classes:
            if single_class[0] not in self.group:
                self.group.append(single_class[0])
            if single_class[1] not in self.subject:
                self.subject.append(single_class[1])
            if single_class[2] not in self.teacher:
                self.teacher.append(single_class[2])
        self.initial()

    def initial(self):
        self.makegroups()
        self.create_population()
        self.population.sort(key=lambda x: self.find_soft_constrain_weight(x))
        self.timeTable = self.population[0]

    def makegroups(self):
        classgroups = self.classgroups
        grouplist = self.grouplist
        for classgroup in classgroups:
            groupdetail = []
            groupdetail.append(classgroup[0])
            groupdetail.append(classgroup[1])
            groupdetail.append(classgroup[2])

            for i in range(int(classgroups[4])):
                grouplist.append(groupdetail)

    def Generate_chromosome(self):
        grouplist = self.grouplist
        chromosome = []
        for group in grouplist:
            gene = []
            day = random.randint(0, self.no_of_days - 1)
            room = random.randint(0, self.no_of_rooms - 1)
            timeslot = random.randint(0, self.no_of_periods - 1)
            gene.append(str(day))
            gene.append(str(room))
            gene.append(str(timeslot))
            gene.append(group)
            chromosome.append(gene)

        return chromosome

    def evaluate_hard_constraints(self, chromosome):  # room clash, teacher clash, group clash
        clashes = []
        cost = 0
        i = 0
        while i < len(chromosome):
            j = i + 1
            day1 = chromosome[i][0]
            timeslot1 = chromosome[i][2]
            room1 = chromosome[i][1]
            teacher1 = chromosome[i][3][2]
            group1 = chromosome[i][3][0]

            while j < len(chromosome):
                isclashing = False
                day2 = chromosome[j][0]
                timeslot2 = chromosome[j][2]
                room2 = chromosome[j][1]
                teacher2 = chromosome[j][3][2]
                group2 = chromosome[j][3][0]

                if day1 == day2 and timeslot1 == timeslot2:
                    if teacher1 == teacher2:
                        isclashing = True
                        cost += 1

                    if room1 == room2:
                        isclashing = True
                        cost += 1
                    if group1 == group2:
                        isclashing = True
                        cost += 1

                if isclashing:
                    clashes.append(chromosome[j])
                    chromosome.remove(chromosome[j])
                j += 1

            i += 1
        return cost, clashes

    def mutation(self, clashes):
        newGenes = []
        for gene in clashes:
            newgene = []
            day = random.randint(0, self.no_of_days - 1)
            room = random.randint(0, self.no_of_rooms - 1)
            timeslot = random.randint(0, self.no_of_periods - 1)
            newgene.append(str(day))
            newgene.append(str(room))
            newgene.append(str(timeslot))
            newgene.append(gene[3])
            newGenes.append(newgene)

        return newGenes

    def find_fittest(self):
        cost = 0

        iteration = 0
        chromosome = self.Generate_chromosome()
        while cost > 0:
            if iteration > 50:
                iteration = 0
                chromosome = self.Generate_chromosome()
            costhard, clashes = self.evaluate_hard_constraints(chromosome)
            cost = costhard
            newGenes = self.mutation(clashes)

            for gene in newGenes:
                chromosome.append(gene)
            iteration += 1

        return chromosome

    def create_population(self):
        for i in range(100):
            self.population.append(self.find_fittest())

        for i in range(100):
            self.make_new_chromosome()

    def find_var(self, val):
        mean = sum(val) / len(val)
        deviation = [(x - mean) ** 2 for x in val]
        return sum(deviation) / len(deviation)

    def find_hard_constrain_weight(self, chromosome):
        cost = 0
        i = 0
        while i < len(chromosome):
            j = i + 1
            day1 = chromosome[i][0]
            timeslot1 = chromosome[i][2]
            room1 = chromosome[i][1]
            teacher1 = chromosome[i][3][2]
            group1 = chromosome[i][3][0]

            while j < len(chromosome):

                day2 = chromosome[j][0]
                timeslot2 = chromosome[j][2]
                room2 = chromosome[j][1]
                teacher2 = chromosome[j][3][2]
                group2 = chromosome[j][3][0]

                if day1 == day2 and timeslot1 == timeslot2:
                    if teacher1 == teacher2:
                        cost += 1

                    if room1 == room2:
                        cost += 1
                    if group1 == group2:
                        cost += 1

                j += 1

            i += 1
        return cost

    def find_soft_constrain_weight(self, chromosome):
        weight = 0

        for group in self.group:
            val = [0] * 5
            for gene in chromosome:
                if group == gene[3][0]:
                    val[gene[0]] += 1
            weight += self.w1 * self.find_var(val)

        for teacher in self.teacher:
            val = [0] * 5
            for gene in chromosome:
                if teacher == gene[3][2]:
                    val[gene[0]] += 1
            weight += self.w2 * self.find_var(val)

        val = [0] * self.no_of_rooms
        for gene in chromosome:
            val[gene[2]] += 1
        weight += self.w2 * self.find_var(val)

        return weight

    def make_new_chromosome(self):
        self.population.sort(key=lambda x: self.find_soft_constrain_weight(x))
        father = self.population[0]
        mother = self.population[1]
        child = self.reproduction(father, mother)
        if self.find_hard_constrain_weight(child) == 0:
            if self.find_soft_constrain_weight(self.population[-1]) > self.find_soft_constrain_weight(child):
                self.population.pop()
                self.population.append(child)

    def compare(self, father, mother):
        x = self.find_hard_constrain_weight(father)
        y = self.find_soft_constrain_weight(father)
        z = self.find_hard_constrain_weight(mother)
        a = self.find_soft_constrain_weight(mother)
        if x < z or (x == z and y < a):
            return father
        return mother

    def reproduction(self, father, mother):

        for i in range(len(father)):
            x = random.randint(0, 1)
            if x == 1:
                temp = copy.deepcopy(father[i])
                father[i] = mother[i]
                mother[i] = temp

        if self.compare(father, mother) > 0:
            return father
        else:
            return mother
