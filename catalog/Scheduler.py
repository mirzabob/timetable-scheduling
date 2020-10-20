import random



class Scheduler():
    def __init__(self, rooms, classes):  #classes=[class], class={group,subject,teacher,no of periods per week}, rooms=[list of room strings]

        self.rooms=rooms
        self.grouplist=[]
        self.classgroups=classes
        self.timeTable = []
        self.dictionary = {}
        self.no_of_days=5
        self.no_of_periods=8
        self.no_of_rooms=len(rooms)




    def makegroups(self):
        classgroups=self.classgroups
        grouplist=self.grouplist
        for classgroup in classgroups:
            groupdetail = []
            groupdetail.append(classgroup[0])
            groupdetail.append(classgroup[1])
            groupdetail.append(classgroup[2])

            for i in range(int(classgroups[4])):
                grouplist.append(groupdetail)

    def Generate_chromosome(self):
        grouplist=self.grouplist
        chromosome=[]
        for group in grouplist:
            gene = []
            day = random.randint(0, self.no_of_days-1)
            room = random.randint(0, self.no_of_rooms-1)
            timeslot = random.randint(0, self.no_of_periods)
            gene.append(str(day))
            gene.append(str(room))
            gene.append(str(timeslot))
            gene.append(group)
            chromosome.append(gene)

        return chromosome

    def  evaluate_hard_constraints(self,chromosome):  #room clash, teacher clash, group clash
        clashes=[]
        cost=0
        i=0
        while i < len(chromosome):
            j=i+1
            day1=chromosome[i][0]
            timeslot1=chromosome[i][2]
            room1=chromosome[i][1]
            teacher1=chromosome[i][3][2]
            group1=chromosome[i][3][0]

            while j < len(chromosome):
                isclashing = False
                day2 = chromosome[j][0]
                timeslot2 = chromosome[j][2]
                room2 = chromosome[j][1]
                teacher2 = chromosome[j][3][2]
                group2 = chromosome[j][3][0]

                if day1 == day2 and timeslot1 == timeslot2 :
                    if teacher1 == teacher2 :
                        isclashing=True
                        cost+=1

                    if room1 == room2:
                        isclashing=True
                        cost+=1
                    if group1 == group2:
                        isclashing=True
                        cost+=1

                if isclashing:
                    clashes.append(chromosome[j])
                    chromosome.remove(chromosome[j])
                j+=1

            i+=1
        return cost,clashes

    def mutation(self,clashes):
        newGenes = []
        for gene in clashes:
            newgene = []
            day = random.randint(0, self.no_of_days-1)
            room = random.randint(0, self.no_of_rooms-1)
            timeslot = random.randint(0, self.no_of_periods)
            newgene.append(str(day))
            newgene.append(str(room))
            newgene.append(str(timeslot))
            newgene.append(gene[3])
            newGenes.append(newgene)

        return newGenes






    def find_fittest(self):
        cost=0
        self.makegroups()
        iteration=0
        chromosome = self.Generate_chromosome()
        while cost >0:
            if iteration > 50:
                iteration = 0
                chromosome = self.Generate_chromosome()
            costhard , clashes =self.evaluate_hard_constraints(chromosome)
            cost=costhard
            newGenes = self. mutation(clashes)

            for gene in newGenes:
                chromosome.append(gene)
            iteration+=1

        self.timeTable = chromosome








