import os
import pandas as pd
import re


def read_df(path, sheet_name):
    return pd.read_excel(path, sheet_name=sheet_name)


def clean_df(df,column):
    fill_na_df= df.fillna(0)
    grouped_df = fill_na_df.groupby(column).sum()
    int_values_df = grouped_df.astype({"Drawings Quantity": int, "BoQ Quantity": int})
    return int_values_df


def write_to_txt(txt_file,heading,df):
    with open(txt_file, "a") as txt_file:
        txt_file.write(f"{heading.strip('Schedules')} \n{df} \n\n")


def select_schedule(item):
    if item=="Doors":
        return "door_schedules", "Door No.", "schedules_summary_doors.txt"
    elif item=="Windows":
        return "window_schedules", "Window No.", "schedules_summary_windows.txt"


# navigate to buildings folder

os.chdir("../Buildings")
cwd = os.path.abspath(os.curdir)
dir_content = os.listdir()
building_folders = []

# filter for directories only
for item in dir_content:
    if os.path.isdir(os.path.join(cwd, item)):
        building_folders.append(item)

open("schedules_summary_windows.txt","w").close()
open("schedules_summary_doors.txt","w").close()

for building in building_folders:
    path = os.path.join(cwd, building)
    schedules = []
    # filter for only files starting with "Schedule" in each directory
    for file in os.listdir(path):
        if re.match(r'Schedule*', file):
            schedules.append(file)
    # copy contents of files to a pandas dataframe
    for schedule in schedules:
        items=['Doors', 'Windows']
        for item in items:
            sheet_name,column,txt_file= select_schedule(item)
            df1= read_df(f'{path}\{schedule}', sheet_name)
            df2= clean_df(df1,column)
            write_to_txt(txt_file,schedule,df2)





