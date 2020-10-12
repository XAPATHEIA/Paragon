import json
import time
import datetime as dt
import os
import re


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


# Datetime Object to String and Vice Versa function.
def dt_morph(item, reverse=False, circular=False):
    if reverse:
        return dt.datetime.strptime(item, '%d/%m/%Y')
    elif circular:
        return dt.datetime.strptime(item, '%d/%m/%Y').strftime("%d/%m/%Y")
    else:
        return item.strftime("%d/%m/%Y")


def initial_setup():
    clear(sleep=True)
    print("Executing Initial Setup...")
    time.sleep(1)
    date_format = re.compile(r'^([0-2][0-9]|(3)[0-1])(/)(((0)[0-9])|((1)[0-2]))(/)\d{4}$')

    while True:
        horizon = input("End Date for Goal (dd/mm/yyyy): ")
        if not date_format.search(horizon):
            initial_setup()
        horizon = dt_morph(horizon, circular=True)
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
                except ValueError:
                    initial_setup()
            if sum(daily_steps_temp.values()) != 100:
                print("Weights did not add up to 100. Restarting.")
                initial_setup()
            else:
                break

        clear(sleep=True)
        print(f"End Date for Goals:\n"
              f"{horizon}\n")
        print("Task and Weighting:")

        for pair in daily_steps_temp.items():
            print(f"{pair[0].ljust(20)}{pair[1]}")
        if input("\nWould you like to finalise your companion? (y/n): ") != 'y':
            initial_setup()
        else:
            clear()
            return {'start_date': (dt_morph(dt.datetime.today())), 'end_date': horizon}, \
                   daily_steps_temp, \
                   (dt_morph(horizon, reverse=True) - dt.datetime.today()).total_seconds() / 86400


# Default tasks for everyday.
def default():
    if cd in tasks.keys():
        return
    else:
        for task in daily_tasks:
            description_temp = {"task": task,
                                "completed": False,
                                "default": True,
                                "weighting": daily_tasks[task]}
            if cd not in tasks.keys():
                tasks[cd] = {}
                tasks[cd][1] = description_temp
            elif cd in tasks.keys():
                list_of_tasks = list((tasks[cd].keys()))
                tasks[cd][(list_of_tasks[-1] + 1)] = description_temp


# If no previous log.json is located, create one from scratch.
if not os.path.exists('log.json'):
    tasks = {}
else:
    with open('log.json') as json_file:
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

try:
    if not os.path.exists('user_data.json'):
        user_data, daily_tasks, initial_days_remaining = initial_setup()
        # Creating persistence for the initial setup.
        with open('user_data.json', 'w') as data_output:
            json.dump(user_data, data_output)
        with open('daily_tasks.json', 'w') as task_output:
            json.dump(daily_tasks, task_output)
        with open('days_remaining.json', 'w') as days_r_output:
            json.dump(initial_days_remaining, days_r_output)
        default()
    else:
        with open('user_data.json') as data_input:
            user_data = json.load(data_input)
        with open('daily_tasks.json') as task_input:
            daily_tasks = json.load(task_input)
        with open('days_remaining.json') as daysr_input:
            initial_days_remaining = json.load(daysr_input)
except:
    print(f"Something went wrong.")


# Interface that user interacts with TO-DO list through.
def interface():
    # If a record exists for the current date.
    if cd in tasks.keys() and tasks[cd].keys():
        lack = True
        u_query = int(input(
            "1. Add Task \n"
            "2. Mark Completion \n"
            "3. Remove Task \n"
            "4. Remove All \n"
            "7. Reset \n"
            "8. Progress \n"
            "9. View Archive \n"
            "0. Exit \n"))
    else:
        lack = False
        u_query = int(input(
            "1. Add Task \n"
            "7. Reset \n"
            "8. Progress \n"
            "9. View Archive \n"
            "0. Exit \n"))
    return u_query, lack


# Adds singular or multiple task/s based on user preference.
def add_task():
    description_task = input("")
    if description_task == '':
        return description_task
    description_template = {"task": description_task,
                            "completed": False,
                            "default": False}
    # If current date doesn't exist in the persistence, create one.
    if cd not in tasks.keys():
        tasks[cd] = {}
        tasks[cd][1] = description_template
    elif cd in tasks.keys():
        list_of_tasks = list((tasks[cd].keys()))
        # Changing the numbering of the tasks so that a new task can be added.
        tasks[cd][(list_of_tasks[-1] + 1)] = description_template


# Marks tasks as complete.
def completion():
    time.sleep(0.5)

    while (index := int(input("Enter Task: "))) > len(list(tasks[cd].keys())):
        print("That task doesn't exist, try again.")
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
        while (user_index := int(input("Enter Task: "))) > len(list(tasks[cd].keys())) or user_index < 1:
            print("That task doesn't exist. Try again.")
        del tasks[cd][user_index]
        for key_index in range(1, len(tasks[cd].keys()) + 2):
            if key_index > user_index:
                tasks[cd][key_index - 1] = tasks[cd].pop(key_index)


def reset():
    if input("Are you sure you want to reset? This process cannot be reversed. (y/n)\n") != 'y':
        return
    print("Resetting...")
    time.sleep(1)
    if os.path.exists("log.json"):
        os.remove("log.json")
    if os.path.exists("user_data.json"):
        os.remove("user_data.json")
    if os.path.exists("daily_tasks.json"):
        os.remove("daily_tasks.json")
    if os.path.exists("days_remaining.json"):
        os.remove("days_remaining.json")
    print("Complete.")
    exit()


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


default()


# Progress bar to visualise long term progress.
def progress_bar():
    progress = 100
    divisor = (initial_days_remaining / 100)
    print(divisor)
    if len(tasks) == 0:
        progress -= progress
        print(progress)
    else:
        print(progress)
        progress -= progress - (len(tasks) / divisor)
        print(progress)
    if len(tasks.keys()) == 1:
        for i in (list(tasks[cd].keys())):
            if not tasks[cd][i]['completed'] and tasks[cd][i]['default']:
                progress -= (tasks[cd][i]['weighting'] / 100 / divisor)
                print(progress)

    if len(tasks.keys()) > 1:
        for days in tuple(zip(list(tasks.keys()))):
            if len(days) > 1:
                if (difference :=
                (dt_morph(days[1], reverse=True).total_seconds()) - (
                        dt_morph(days[0], reverse=True).total_seconds())) > 86400:
                    progress -= ((difference - 86400) / 86400) / divisor
                    print(progress)
            for i in (internal_tasks := list(tasks[days[0]].keys())):
                for j in internal_tasks:
                    if not tasks[days[0]][j]['completed'] and tasks[days[0]][j]['default']:
                        progress -= (tasks[days[0]][j]['weighting'] / divisor)
                        print(progress)
    for i in range(100):
        if i == 0:
            print('0% ', end='')
        if i < progress:
            print('█', end='')
        else:
            print('░', end='')
    print(' 100%')
    rounded_progress = "{:.2f}".format(progress)
    print(f"You are at {rounded_progress} %")
    print(
        f"You have {round((dt_morph(user_data['end_date'], reverse=True) - (dt_morph(cd, reverse=True))).total_seconds() / 86400)} days remaining.")


# Initiating loop to allow for consecutive additions/removals of tasks.
while True:
    progress_bar()
    time.sleep(1)
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
        elif query == 7:
            reset()
        elif query == 8 and occupied:
            progress_bar()
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

# Creating persistence for tasks.
with open('log.json', 'w') as db_output:
    json.dump(tasks, db_output)
