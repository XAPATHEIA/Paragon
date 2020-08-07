import json
import time
from TODOListCLI import taskencode
from TODOListCLI.task import Task

total_tasks = []
time.sleep(1)
print("""
******** To-Do List ********


____________________________
""")

# Initiating loop to allow for consecutive additions/removals of tasks
while True:
    if not total_tasks:

        