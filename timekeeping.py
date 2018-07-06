# -*- coding: utf-8 -*-
import datetime

mode = 'start'
task = 'break'
tasks = {'break': 'None'}
taskTimes = {'None' : 0}
now = datetime.datetime.now()

def UpdateTask():
    global now
    budget = tasks[task]
    prev = now
    now = datetime.datetime.now()
    hr = now.hour - prev.hour
    mn = (now.minute - prev.minute) / 60.0
    taskTimes[budget] += hr + mn

def Print():
    print("\n Task\t\tBudget\t\tTime")
    total = 0
    for iTask in tasks:
        tIndent = "\t" * (2 - (len(iTask) >> 3))
        budget = tasks[iTask]
        bIndent = "\t" * (2 - (len(budget) >> 3))
        firstChar = " "
        time = round(taskTimes[budget], 1)
        if budget != 'None':
            total += time
        if iTask == task:
            firstChar = "*"
        printStr = firstChar + \
                    iTask + \
                    tIndent + \
                    budget + \
                    bIndent + \
                    "{0:.1f}".format(time)
        print(printStr)
    print("Total time: {0:.1f}".format(total))

def AmendTime(modTask, diff):
    UpdateTask()
    time = 0.0
    if modTask in tasks:
        time = taskTimes[tasks[modTask]]
        print("Total time for task {0}: {1:.1f}".format(modTask, round(time, 1)))
        if -diff > time:
            print("Invalid amount of time entered.")
            return False
        else:
            time += diff
            taskTimes[tasks[modTask]] = time
        return True
    else:
        return False

params = []

while not(mode == 'quit' or mode == 'q'):
    UpdateTask()
    Print()
    inp = input('>> ').split()
    mode = inp[0]
    params = inp[1:]
    if mode == 'task' or mode == 't':
        if len(params) == 0:
            desc = input("Input task/project description: ")
            budget = input("Input budget: ")
        elif len(params) % 2 == 0:
            for i in range (0, len(params), 2):
                desc = params[i]
                budget = params[i + 1]
        else:
            continue
        if desc not in tasks:
            tasks[desc] = budget
            taskTimes[budget] = 0
        else:
            print("Error: task name {0} already in use!".format(desc))            
    elif mode == 'switch' or mode == 's':
        if len(params) == 0:
            newTask = input('Select new task: ')
        elif len(params) == 1:
            newTask = params[0]
        else:
            continue
        if newTask in tasks:
            UpdateTask()
            task = newTask
        else:
            print("Error: no such task")
    elif mode == 'amend' or mode == 'a':
        if(len(params) == 0):
            modTask = input("Select task to modify: ")
            diff = float(input("Enter time to add/remove: "))
            AmendTime(modTask, diff)
        elif(len(params) % 2 == 0):
            valid = True
            for i in range(0, len(params), 2):
                if(valid):
                    valid = AmendTime(params[i], float(params[i + 1]))    

UpdateTask()
Print()