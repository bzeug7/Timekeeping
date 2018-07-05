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

params = []

while not(mode == 'quit' or mode == 'q'):
    valid = True
    if mode == 'start':
        mode = 'switch'
        now = datetime.datetime.now()
    elif mode == 'task' or mode == 't':
        if len(params) == 0:
            desc = input("Input task/project description: ")
            budget = input("Input budget: ")
        elif len(params) == 2:
            desc = params[0]
            budget = params[1]
        else:
            valid = False
        if valid:
            if desc not in tasks:
                tasks[desc] = budget
                taskTimes[budget] = 0
            else:
                print("Error: task name {0} already in use!".format(desc))            
    elif mode == 'switch' or mode == 's':
        newTask = input('Select new task: ')
        if newTask in tasks:
            UpdateTask()
            task = newTask
        else:
            print("Error: no such task")
    elif mode == 'view' or mode == 'v':
        UpdateTask()
    elif mode == 'amend' or mode == 'a':
        UpdateTask()
        modTask = input("Select task to modify: ")
        time = 0.0
        if modTask in tasks:
            time = taskTimes[tasks[modTask]]
        else:
            budget = input("New task selected- enter budget: ")
            tasks[modTask] = budget
            taskTimes[budget] = 0
        print("Total time for task {0}: {1:.1f}".format(modTask, round(time, 1)))
        diff = float(input("Enter time to add/remove: "))
        if -diff > time:
            print("Invalid amount of time entered.")
        else:
            time += diff
            taskTimes[tasks[modTask]] = time
    Print()
    inp = input('>> ').split()
    mode = inp[0]
    params = inp[1:]

UpdateTask()
Print()