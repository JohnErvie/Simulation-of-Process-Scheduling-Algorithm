values = ['p1', 3, 4, 'p2', 5, 9, 'p3', 8, 4, 'p4', 0, 7, 'p5', 12, 6]
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

time = 0
lowbt = 0
queue = []
loopqueue = True

numTerminate = 0

loop = True
while loop != False:
    # if is there process arrive in current time then add it into queue
    for row in range(allProcess):
        if time == int(listedVal[row][1]): ## if they're equal to time
            queue.append([]) ## adding to queue
            queue[int(len(queue))-1].append(listedVal[row][0])
            queue[int(len(queue))-1].append(int(listedVal[row][1]))
            queue[int(len(queue))-1].append(int(listedVal[row][2]))

    # find the lowest burst time in queue then execute that
    lowbt = 0
    loopqueue = True
    if int(len(queue)) > 0:
        while loopqueue != False:
            rowbt = 0
            while rowbt < int(len(queue)):
                if int(queue[rowbt][2]) == lowbt:
                    queue[rowbt][2] = int(queue[rowbt][2]) - 1 # subtract 1 burst time
                    rowbt = int(len(queue))
                    loopqueue = False
                rowbt +=1
            lowbt += 1

        # deleting the process in queue if 0 burst time
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
        loop = False

    time += 1

for i in range(allProcess): #inputing the turn around time and waiting time
    listedVal[i].append(int(listedVal[i][3]) - int(listedVal[i][1])) # End Time - Arrival Time
    listedVal[i].append(int(listedVal[i][4]) - int(listedVal[i][2])) # Turn Around Time - Burst Time

aveTT = 0
aveWT = 0

for i in range(allProcess): #computing the average turn around time
    aveWT += int(listedVal[i][5])/allProcess
    aveTT += int(listedVal[i][4])/allProcess

print("Average Waiting Time: ", "%.2f" %aveWT)
print("Average Turn Around Time: ", "%.2f" %aveTT)

    