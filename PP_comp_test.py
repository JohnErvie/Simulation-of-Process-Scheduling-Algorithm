values = ['p1', 3, 4, 2, 'p2', 5, 9, 1, 'p3', 8, 4, 2, 'p4', 0, 7, 1, 'p5', 12, 6, 1]
lengthSRTF_valTables = len(values)

PP = 4

allProcess = int(lengthSRTF_valTables/PP)

listedVal = []

for i in range(allProcess): # adding 2d array
    listedVal.append([])

indexVal = 0
for row in range(allProcess): # Converting the values to 2d array
    for col in range(PP):
        listedVal[row].append(values[indexVal])
        indexVal += 1

totalEndTime = 0
queue = []
loopqueue = True
samePriority = []
sameBurstTime = []

numTerminate = 0

time = 0
loop = True
while loop != False: 
    # if is there process arrive in current time then add it into queue
    for row in range(allProcess):
        if time == int(listedVal[row][1]): ## if there equal to time
            queue.append([]) ## adding to queue
            queue[int(len(queue))-1].append(listedVal[row][0])
            queue[int(len(queue))-1].append(int(listedVal[row][1]))
            queue[int(len(queue))-1].append(int(listedVal[row][2]))
            queue[int(len(queue))-1].append(int(listedVal[row][3]))

    # find the lowest priority in queue
    if int(len(queue)) > 0:
        if int(len(queue)) > 1 : # if more than 1 in queue check the lowest priority
            lowP = 0
            loopqueue = True
            while loopqueue != False:
                rowP = 0
                while rowP < int(len(queue)):
                    if int(queue[rowP][3]) == lowP:
                        samePriority.append(rowP)
                        loopqueue = False
                    rowP +=1
                lowP += 1

            # if there are the same priority
            if int(len(samePriority)) > 1:
                lowbt = 0
                loopqueue = True
                while loopqueue != False:
                    rowbt = 0
                    while rowbt < int(len(samePriority)):
                        if int(queue[int(samePriority[rowbt])][2]) == lowbt:
                            sameBurstTime.append(samePriority[rowbt]) # add the row into burst time
                            loopqueue = False
                        rowbt +=1
                    lowbt += 1

                # then if there are the same burst time
                if int(len(sameBurstTime)) > 1:
                    lowat = 0
                    loopqueue = True
                    while loopqueue != False:
                        rowat = 0
                        while rowat < int(len(sameBurstTime)):
                            if int(queue[int(sameBurstTime[rowat])][1]) == lowat:
                                queue[int(sameBurstTime[rowat])][2] = int(queue[int(sameBurstTime[rowat])][2]) - 1 # subtract 1 burst time
                                rowat = int(len(queue))
                                loopqueue = False
                            rowat +=1
                        lowat += 1

                else: 
                    queue[int(sameBurstTime[0])][2] = int(queue[int(sameBurstTime[0])][2]) - 1
            
            else:
                queue[int(samePriority[0])][2] = int(queue[int(samePriority[0])][2]) - 1
            
        else: # if only 1 process in queue then execute it
            queue[0][2] = int(queue[0][2]) - 1 # subtract 1 burst time

        #print(sameBurstTime)
        samePriority.clear()
        sameBurstTime.clear()

    # deleting the 0 burst time in queue
    qRow = 0
    while qRow < int(len(queue)):
        if int(queue[qRow][2]) <= 0: # if the process has 0 burst time, delete that process in queue
            for x in range (allProcess): # inputing the end time process
                if listedVal[x][0] == queue[qRow][0]: # if process id is same as in queue, then input it in specific process
                    listedVal[x].append(time+1)
                    numTerminate +=1
            queue.pop(qRow)
        qRow += 1

    if numTerminate == allProcess:
        totalEndTime = time+1
        loop = False

    time += 1
    print(time)
    #print(queue)


for i in range(allProcess): #inputing the turn around time and waiting time
    listedVal[i].append(int(listedVal[i][4]) - int(listedVal[i][1])) # End Time - Arrival Time
    listedVal[i].append(int(listedVal[i][5]) - int(listedVal[i][2])) # Turn Around Time - Burst Time

print(listedVal)


cpuUtil = 0
totalBurstTime = 0
aveTT = 0
aveWT = 0

for i in range(allProcess): #computing the Cpu Utilization
    totalBurstTime += int(listedVal[i][2])

cpuUtil = (totalBurstTime/totalEndTime)*100 # formula for Cpu Utilization

for i in range(allProcess): #computing the average turn around time
    aveWT += int(listedVal[i][5])/allProcess
    aveTT += int(listedVal[i][6])/allProcess

print("CPU Utilization: ", "%.2f" %cpuUtil)
print("Average Waiting Time: ", "%.2f" %aveWT)
print("Average Turn Around Time: ", "%.2f" %aveTT)
