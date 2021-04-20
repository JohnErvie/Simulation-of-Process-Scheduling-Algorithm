import numpy as np

values = ['p1', 3, 4, 'p2', 5, 9, 'p3', 8, 4, 'p4', 0, 7, 'p5', 12, 6]
lengthSRTF_valTables = len(values)

listedVal = []

listedVal = np.array(values).reshape(int(lengthSRTF_valTables/3),3)

savedlistedVal = listedVal

allProcess = int(lengthSRTF_valTables/3)

loop = True
btloop = True
lowbt = 0
time = 0
atcheck = 0
btcheck = 0
lowat = 0

queue = []
checkqueue = 0

endAllProcess = 0
for i in range(allProcess):
    endAllProcess += int(listedVal[i][1]) + int(listedVal[i][2]) 

lastrow = 0

while loop != False:
    for col in range(allProcess):
        ### finding the lowest Arrival Time
        if int(listedVal[col][1]) == time:
            if int(len(queue)) > 1: ## checking if there is/are another queue
                for j in range(int(len(queue))):
                    if int(queue[j][2]) == lowbt: ## checking lowest burst time
                        queue[j][1] = int(queue[j][2]) - 1
                        lastrow = j ## saving the last row

                    lowbt += 1

            #else: ## if only one queue
            if int(len(queue)) > 0: ## Adding in Queue
                for i in range(int(len(queue))):
                    if queue[i][0] == listedVal[col][0]: ## checking if already in queue then -1 burst time
                        queue[i][2] = int(queue[i][2]) - 1

                    else:
                        checkqueue += 1
                    if checkqueue == int(len(queue)): ## if there no equal then add to queue
                        queue.append([])
                        queue[int(len(queue))-1].append(listedVal[col][0])
                        queue[int(len(queue))-1].append(int(listedVal[col][1]))
                        queue[int(len(queue))-1].append(int(listedVal[col][2]))
                        queue[int(len(queue))-1][2] = int(queue[int(len(queue))-1][2]) - 1

            else: ## if no queue then add to queue
                queue.append([])
                queue[int(len(queue))-1].append(listedVal[col][0])
                queue[int(len(queue))-1].append(int(listedVal[col][1]))
                queue[int(len(queue))-1].append(int(listedVal[col][2]))
                queue[int(len(queue))-1][2] = int(queue[int(len(queue))-1][2]) - 1

        else:
            atcheck += 1

        if int(len(queue)) > 0:
            if atcheck == allProcess:
                queue[lastrow][2] = int(queue[lastrow][2]) - 1

    qRow = 0
    while qRow < int(len(queue)):
        if int(queue[qRow][2]) == 0: # if the bt is 0, delete the queue
            queue.pop(qRow)
        qRow += 1
        
    if time == endAllProcess:
        loop = False

    #btloop = True
    atcheck = 0
    lowbt = 0
    checkqueue = 0
    time += 1
    print(queue)



    
