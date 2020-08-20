import json
import time
import datetime
from TODOListCLI import taskencode

tasks = {}
today = datetime.date.today()
cd = today.strftime("%d/%m/%Y")


def new_lines(number_of_lines):
    for i in range(number_of_lines):
        print()


def interface():
    if cd in tasks.keys() and tasks[cd].keys():
        lack = True
        u_query = int(input(("""What would you like to do?:
1. Add Task
2. Mark Completion
3. Remove Task
4. Remove All
0. Exit
\n""")))
    else:
        lack = False
        u_query = int(input(("""What would you like to do?:
1. Add Task
0. Exit
\n""")))
    return u_query, lack


def add_task():
    description_task = input("")
    if description_task == '':
        return description_task
    description_temp = {"task": description_task,
                        "completed": False}
    if cd not in tasks.keys():
        tasks[cd] = {}
        tasks[cd][1] = description_temp
    elif cd in tasks.keys():
        list_of_tasks = list((tasks[cd].keys()))
        tasks[cd][(list_of_tasks[-1] + 1)] = description_temp


def completion():
    time.sleep(0.5)
    while index := int(input("Enter Task: ")) > len(list(tasks[cd].keys())):
        print("That task doesn't exist. Try again.")
    else:
        pass


# Initiating loop to allow for consecutive additions/removals of tasks
while True:
    print("******** To-Do List ********")
    if cd in tasks.keys():
        for n_task in tasks[cd].keys():
            print(f"{n_task}. {tasks[cd][n_task]['task']}")
    print("____________________________\n")
    time.sleep(1)
    query, occupied = interface()
    if query == 1:
        counter = 1
        if input("Would you like to add multiple tasks? Y/N: ").lower() == 'y':
            print("To cancel, press enter.")
            while True:
                if add_task() == '':
                    break
                counter += 1
        else:
            print("To cancel, press enter.")
            add_task()
        new_lines(3)
        time.sleep(1)
    elif query == 2 and occupied:
        completion()
        new_lines(3)
        time.sleep(1)
    elif query == 3 and occupied:
        pass
    elif query == 4 and occupied:
        pass
    elif query == 0:
        break
