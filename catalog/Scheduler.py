import random


class Scheduler:
    def __init__(self, rooms, classes):

        """
        classes = array of class objects
        class = an array of {group, course, lecturer, no. of periods per week}
        rooms = [ list of rooms with name only]
        """

        self.rooms = rooms
        self.grouplist = []
        self.classgroups = classes
        self.timeTable = []
        self.dictionary = {}
        self.no_of_days = 5
        self.no_of_periods = 8
        self.no_of_rooms = len(rooms)

    def make_groups(self):
        classrooms = self.classgroups
        group_list = self.grouplist
        for class_group in classrooms:
            group_detail = [class_group[0], class_group[1], class_group[2]]
            total_period = class_group[3]

            for i in range(total_period):
                group_list.append(group_detail)

    def generate_chromosome(self):
        group_list = self.grouplist
        chromosome = []
        for group in group_list:
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
                is_clashing = False
                day2 = chromosome[j][0]
                timeslot2 = chromosome[j][2]
                room2 = chromosome[j][1]
                teacher2 = chromosome[j][3][2]
                group2 = chromosome[j][3][0]

                if day1 == day2 and timeslot1 == timeslot2:
                    if teacher1 == teacher2:
                        is_clashing = True
                        cost += 1

                    if room1 == room2:
                        is_clashing = True
                        cost += 1
                    if group1 == group2:
                        is_clashing = True
                        cost += 1

                if is_clashing:
                    clashes.append(chromosome[j])
                    chromosome.remove(chromosome[j])
                j += 1

            i += 1
        return cost, clashes

    def mutation(self, clashes):
        new_genes = []
        for gene in clashes:
            new_gene = []
            day = random.randint(0, self.no_of_days - 1)
            room = random.randint(0, self.no_of_rooms - 1)
            timeslot = random.randint(0, self.no_of_periods - 1)
            new_gene.append(str(day))
            new_gene.append(str(room))
            new_gene.append(str(timeslot))
            new_gene.append(gene[3])
            new_genes.append(new_gene)

        return new_genes

    def find_fittest(self):
        cost = 0
        self.make_groups()
        iteration = 0
        chromosome = self.generate_chromosome()
        while cost > 0:
            if iteration > 50:
                iteration = 0
                chromosome = self.generate_chromosome()
            cost_hard, clashes = self.evaluate_hard_constraints(chromosome)
            cost = cost_hard
            new_genes = self.mutation(clashes)

            for gene in new_genes:
                chromosome.append(gene)
            iteration += 1

        self.timeTable = chromosome
