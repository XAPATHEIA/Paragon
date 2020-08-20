import json
import time
import datetime
from TODOListCLI import taskencode

tasks = {}
today = datetime.date.today()
cd = today.strftime("%d/%m/%Y")

description = {"task": "Finish Homework",
               "completed": False}
instantiation = {1: description}
tasks[cd] = instantiation
print(tasks)


def interface():
    if tasks[cd].keys():
        u_query = int(input(("""What would you like to do?:
1. Add Task
2. Mark Completion
3. Remove Task
4. Remove All
0. Exit
""")))
    else:
        u_query = int(input(("""What would you like to do?:
1. Add Task
0. Exit
""")))
    return u_query


def add_task():
    if cd not in tasks.keys():
        print("Im here")
        description_task = input("Task?: ")
        if description_task == '':
            return description_task
        description_temp = {"task": description_task,
                            "completed": False}
        tasks[cd][1] = description_temp
    else:
        description_task = input("Task?: ")
        if description_task == '':
            return description_task
        description_temp = {"task": description_task,
                            "completed": False}
        list_of_tasks = list((tasks[cd].keys()))
        tasks[cd][(list_of_tasks[-1] + 1)] = description_temp

def completion():
    


# Initiating loop to allow for consecutive additions/removals of tasks
while True:
    print("******** To-Do List ********")
    if tasks[cd]:
        for n_task in tasks[cd].keys():
            print(f"{n_task}. {tasks[cd][n_task]['task']}")
    print("____________________________\n")
    time.sleep(1)
    query = interface()
    if query == 1:
        if input("Would you like to add multiple tasks? Y/N: ").lower() == 'y':
            print("To exit, press enter.")
            while True:
                if add_task() == '':
                    break
        else:
            add_task()
    if query == 2:
        pass
    if query == 3:
        pass
    if query == 4:
        pass
    if query == 0:
        break
