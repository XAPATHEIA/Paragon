import json
import time
import datetime as dt
import os
import re

# TODO: Provide option to reset progress bar and initial_setup, but maintain archive that updates old goals in the
#   background to maintain accountability.

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

today = dt.date.today()
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


# TODO: Create persistence for the user_data and daily_steps - create conditionals at the beginning of script to check
# TODO: whether they exist or not, so that initial_setup() can be ran respectively.
def initial_setup():
    clear(sleep=True)
    print("Executing Initial Setup...")
    time.sleep(1)
    date_format = re.compile(r'^([0-2][0-9]|(3)[0-1])(/)(((0)[0-9])|((1)[0-2]))(/)\d{4}$')
    while True:
        date_of_birth = input("Date of Birth (dd/mm/yyyy): ")
        if not date_format.search(date_of_birth):
            initial_setup()
        date_of_birth = dt.datetime.strptime(date_of_birth, '%d/%m/%Y').strftime("%d/%m/%Y")
        horizon = input("End Date for Goal (dd/mm/yyyy): ")
        if not date_format.search(horizon):
            initial_setup()
        horizon = dt.datetime.strptime(horizon, '%d/%m/%Y').strftime("%d/%m/%Y")
        daily_steps_temp = {}
        print("Enter the daily tasks that will bring you closer to your goal/s. Press'ENTER' to cancel.")
        i = 1
        while (small_step := input(f"Task {i}: ")) != '':
            daily_steps_temp[small_step] = None
            i += 1
        i -= 1
        while True:
            clear(sleep=True)
            print(
                f"Weigh the importance of your tasks - which of these tasks will contribute the most to your goals "
                f"and development?\nMake sure the weights add up to 100.")
            for step in daily_steps_temp.keys():
                try:
                    daily_steps_temp[step] = int(input(f"{step}: "))
                except ValueError as E:
                    initial_setup()
            if sum(daily_steps_temp.values()) != 100:
                print("Weights did not add up to 100. Restarting.")
                initial_setup()
            else:
                break
        clear(sleep=True)
        print(f"Date of Birth:\n"
              f"{date_of_birth}\n")
        print(f"End Date for Goals:\n"
              f"{horizon}\n")
        print("Task and Weighting:")
        for pair in daily_steps_temp.items():
            print(f"{pair[0].ljust(20)}{pair[1]}")
        if input("\nWould you like to finalise your companion? (y/n): ") != 'y':
            initial_setup()
        else:
            return {'dob': date_of_birth, 'start_date': (dt.datetime.today()).strftime("%d/%m/%Y"),
                    'end_date': horizon}, daily_steps_temp


user_data, daily_steps, = initial_setup()


# TODO: Create a variable that stores the difference of days between the start_date, and the horizon.
# TODO: Make it so that the progress towards the horizon is re-calculated every time the app is opened.
# TODO: You need to find a way to:
#  - subtract two datetime objects
#  - apply weightings to calculate percentage growth per-day
#  - two different text representations for the progress bar. One for successful progress, and missed-out on progress.
# Progress bar to visualise long term progress.
def progress_bar():
    days_elapsed = dt.datetime.strptime(user_data['end_date'], "%d/%m/%Y") - \
                   dt.datetime.strptime(user_data['start_date'], "%d/%m/%Y")
    print(days_elapsed.total_seconds())


progress_bar()

# Adding default tasks.
# default()
# Initiating loop to allow for consecutive additions/removals of tasks.
"""while True:
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
"""
# Creating persistence.
with open('tasks.json', 'w') as outfile:
    json.dump(tasks, outfile)
