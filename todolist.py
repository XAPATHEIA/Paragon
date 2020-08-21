import json
import time
import datetime

tasks = {}
today = datetime.date.today()
cd = today.strftime("%d/%m/%Y")


# Function used throughout to improve interface.
def new_lines(number_of_lines):
    for i in range(number_of_lines):
        print()
    time.sleep(1)


# Produces the visual feedback of completion/undoing completion.
def strike(text, undo=False):
    result = ''
    if undo:
        for c in text:
            result += c.strip('\u0336')
        return result
    for c in text:
        result = result + c + '\u0336'
    return result


# Interface that user interacts with TO-DO list through.
def interface():
    if cd in tasks.keys() and tasks[cd].keys():
        lack = True
        u_query = int(input(("""What would you like to do?:
1. Add Task
2. Mark Completion
3. Remove Task
4. Remove All
0. Exit
""")))
    else:
        lack = False
        u_query = int(input("""What would you like to do?:
1. Add Task
0. Exit
"""))
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


# Marks tasks as complete.
def completion():
    time.sleep(0.5)
    while (index := int(input("Enter Task: "))) > len(list(tasks[cd].keys())):
        print("That task doesn't exist. Try again.")
    else:
        if tasks[cd][index]['completed']:
            tasks[cd][index]['completed'] = False
            tasks[cd][index]['task'] = strike(tasks[cd][index]['task'], undo=True)
        elif not tasks[cd][index]['completed']:
            tasks[cd][index]['completed'] = True
            tasks[cd][index]['task'] = strike(tasks[cd][index]['task'])


def remove_task(everything=False):
    time.sleep(0.5)
    if everything:
        if input("Confirm: Y/N\n").lower() != 'y':
            return
        else:
            del tasks[cd]
            return
    else:
        while (user_index := int(input("Enter Task: "))) > len(list(tasks[cd].keys())):
            print("That task doesn't exist. Try again.")
        del tasks[cd][user_index]
        for key_index in range(1, len(tasks[cd].keys()) + 2):
            if key_index > user_index:
                tasks[cd][key_index - 1] = tasks[cd].pop(key_index)


# Initiating loop to allow for consecutive additions/removals of tasks
while True:
    print("******** To-Do List ********")
    if cd in tasks.keys():
        for n_task in tasks[cd].keys():
            print(f"{n_task}. {tasks[cd][n_task]['task']}")
    print("____________________________\n")
    time.sleep(1)
    try:
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
        elif query == 2 and occupied:
            completion()
            new_lines(3)
        elif query == 3 and occupied:
            remove_task()
            new_lines(3)
        elif query == 4 and occupied:
            remove_task(everything=True)
            new_lines(3)
        elif query == 0:
            break
    except ValueError:
        print("Unexpected input received, try again.")
        new_lines(1)

