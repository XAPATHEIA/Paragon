import json
import time
import datetime
import os

# If no previous tasks.json is located, start from scratch.
if not os.path.exists('tasks.json'):
    tasks = {}
else:
    with open('tasks.json') as json_file:
        prelim = json.load(json_file)
        # Acquiring the dates to loop through.
        prelim_dates = list(prelim.keys())
    for entry in prelim_dates:
        for prelim_task in list(prelim[entry].keys()):
            # Turning the task numbers in the dates to integers.
            prelim[entry][int(prelim_task)] = prelim[entry].pop(prelim_task)
    tasks = prelim
    del prelim

today = datetime.date.today()
cd = today.strftime("%d/%m/%Y")  # Current Date.


# Clear Command Line output for improving readability.
def clear(sleep=False):
    os.system('cls')
    if sleep:
        time.sleep(1)




# Function used throughout to improve interface.
def new_lines(number_of_lines):
    for i in range(number_of_lines):
        print()
    time.sleep(1)


# Interface that user interacts with TO-DO list through.
def interface():
    # If a record exists for the current date.
    if cd in tasks.keys() and tasks[cd].keys():
        lack = True
        u_query = int(input(("""What would you like to do?:
1. Add Task
2. Mark Completion
3. Remove Task
4. Remove All
9. View Archive
0. Exit
""")))
    else:
        lack = False
        u_query = int(input("""What would you like to do?:
1. Add Task
9. View Archive
0. Exit
"""))
    return u_query, lack


# Adds singular or multiple task/s based on user preference.
def add_task():
    description_task = input("")
    if description_task == '':
        return description_task
    description_temp = {"task": description_task,
                        "completed": False}
    # If current date doesn't exist in the persistence, create one.
    if cd not in tasks.keys():
        tasks[cd] = {}
        tasks[cd][1] = description_temp
    elif cd in tasks.keys():
        list_of_tasks = list((tasks[cd].keys()))
        # Changing the numbering of the tasks so that a new task can be added.
        tasks[cd][(list_of_tasks[-1] + 1)] = description_temp


# Marks tasks as complete.
def completion():
    time.sleep(0.5)

    while (index := int(input("Enter Task: "))) > len(list(tasks[cd].keys())):
        print("That task doesn't exist. Try again.")
    else:
        task_completed = tasks[cd][index]['completed']
        if task_completed:
            tasks[cd][index]['completed'] = False
            tasks[cd][index]['task'] = f"{(tasks[cd][index]['task'])[:-11]}"  # Removing completion through slicing.

        elif not task_completed:
            tasks[cd][index]['completed'] = True
            tasks[cd][index]['task'] = f"{tasks[cd][index]['task']} [COMPLETE]"


# Removes singular or all task/s based on user preference.
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


# Visual access to persistence, navigated via date in DD/MM/YYYY format.
def archive():
    dates = list(tasks.keys())
    while True:
        try:
            selection = int(input("1. Enter Archive\n"
                                  "2. Exit\n"))
            if selection == 2:
                break
            elif selection == 1:
                for j in range(len(dates)):
                    if (j + 1) % 4 == 0:  # New line every 4 dates, so as to look better.
                        print(f"[{dates[j]}]")
                    else:
                        print(f"[{dates[j]}] ", end='')
                print()
                user_input = input("Enter Date: ")
                if user_input not in dates:
                    print("Could not find that date, returning.")
                    time.sleep(1)
                    break
                print("____________________________\n"
                      "Tasks that day: ")
                for previous_task in tasks[user_input].keys():
                    print(f"{previous_task}. {tasks[user_input][previous_task]['task']}")
                print("____________________________\n")
            else:
                print("Invalid Input. Returning.")
        except ValueError:
            print("Error Occurred: Exiting.")


# Default tasks for everyday - change to your preference.
def default():
    if cd in tasks.keys():
        return
    else:
        default_tasks = [
            'TEST 1',
            'TEST 2',
            'TEST 3',
            'TEST 4',
            'TEST 5',
        ]
        for task in default_tasks:
            description_temp = {"task": task,
                                "completed": False}
            if cd not in tasks.keys():
                tasks[cd] = {}
                tasks[cd][1] = description_temp
            elif cd in tasks.keys():
                list_of_tasks = list((tasks[cd].keys()))
                tasks[cd][(list_of_tasks[-1] + 1)] = description_temp


# Progress bar to visualise long term progress.
def progress_bar():
    for step in tasks.keys():
        print(step)


def initial_setup():
    while True:
        date_of_birth = input("Date of Birth (dd/mm/yyyy): ")
        try:
            horizon = int(input("End Date for Goal (months): "))
            daily_steps = []
            print("Enter the daily tasks that will bring you closer to your goal/s. Press'ENTER' to cancel.")
            i = 1
            while (small_step := input(f"Task {i}: ")) != '':
                daily_steps.append(small_step)
                i += 1
                continue
            clear(sleep=True)
            print(f"Weigh the importance of your tasks - which of these tasks will contribute the most to your goals "
                  f"and development? Number from 1 to {i}")

        except ValueError as E:
            print(f"Error Occurred: {E}")


























# Adding default tasks.
default()
# Initiating loop to allow for consecutive additions/removals of tasks.
while True:
    print("______________________________________")
    if cd in tasks.keys():
        for n_task in tasks[cd].keys():
            print(f"{n_task}. {tasks[cd][n_task]['task']}")
    print("______________________________________\n")
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
            clear()
        elif query == 2 and occupied:
            completion()
            clear()
        elif query == 3 and occupied:
            remove_task()
            clear()
        elif query == 4 and occupied:
            remove_task(everything=True)
            clear()
        elif query == 9:
            clear()
            time.sleep(1)
            archive()
            clear()
        elif query == 0:
            break
    except ValueError:
        print("Unexpected input received, try again.")
        clear()

# Creating persistence.
with open('tasks.json', 'w') as outfile:
    json.dump(tasks, outfile)