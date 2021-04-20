values = ['p1', 10, 5, 'p2', 8, 4, 'p3', 12, 4, 'p4', 3, 3, 'p5', 15, 5]
lengthSRTF_valTables = len(values)

allProcess = int(lengthSRTF_valTables/3)

listedVal = []

for i in range(allProcess): # adding 2d array
    listedVal.append([])

indexVal = 0
for row in range(allProcess): # Converting the values to 2d array
    for col in range(3):
        listedVal[row].append(values[indexVal])
        indexVal += 1

totalEndTime = 0
queue = []
lowbt = 0
loopqueue = True

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

    # find the lowest arrival time in queue then execute that
    lowbt = 0
    loopqueue = True
    if int(len(queue)) > 0:
        while loopqueue != False:
            rowbt = 0
            while rowbt < int(len(queue)):
                if int(queue[rowbt][1]) == lowbt:
                    queue[rowbt][2] = int(queue[rowbt][2]) - 1 # subtract 1 burst time
                    rowbt = int(len(queue))
                    loopqueue = False
                rowbt +=1
            lowbt += 1

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



for i in range(allProcess): #inputing the turn around time and waiting time
    listedVal[i].append(int(listedVal[i][3]) - int(listedVal[i][1])) # End Time - Arrival Time
    listedVal[i].append(int(listedVal[i][4]) - int(listedVal[i][2])) # Turn Around Time - Burst Time

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
    aveTT += int(listedVal[i][4])/allProcess

print("CPU Utilization: ", "%.2f" %cpuUtil)
print("Average Waiting Time: ", "%.2f" %aveWT)
print("Average Turn Around Time: ", "%.2f" %aveTT)
