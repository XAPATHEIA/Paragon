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




# Initiating loop to allow for consecutive additions/removals of tasks
while True:
    print("******** To-Do List ********")
    print("____________________________\n")
    time.sleep(1)
    query = interface()
    if query == 1:
        pass
    if query == 2:
        pass
    if query == 3:
        pass
    if query == 4:
        pass
    if query == 0:
        break
