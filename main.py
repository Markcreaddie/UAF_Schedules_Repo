import os
import pandas as pd
import re

# navigate to buildings folder
os.chdir("../Buildings")
cwd = os.path.abspath(os.curdir)
dir_content = os.listdir()
building_folders = []

# filter for directories only
for item in dir_content:
    if os.path.isdir(os.path.join(cwd, item)):
        building_folders.append(item)

for building in building_folders:
    path = os.path.join(cwd, building)
    schedules = []
    # filter for only files starting with "Schedule" in each directory
    for file in os.listdir(path):
        if re.match(r'Schedule*', file):
            schedules.append(file)
    # copy contents of files to a pandas dataframe
    for schedule in schedules:
        df = pd.read_excel(f'{path}\{schedule}', sheet_name="door_schedules")
        print(df)
        