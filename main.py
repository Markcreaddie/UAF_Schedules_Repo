import os
import pandas as pd
import re


def select_schedule(item):
    if item=="Doors":
        return "door_schedules", "Door No.", "schedules_summary_doors.txt"
    elif item=="Windows":
        return "window_schedules", "Window No.", "schedules_summary_windows.txt"


def read_df(path, sheet_name):
    return pd.read_excel(path, sheet_name=sheet_name)


def clean_df(df,column):
    fill_na_df= df.fillna(0)
    grouped_df = fill_na_df.groupby(column).sum()
    int_values_df = grouped_df.astype({"Drawings Quantity": int, "BoQ Quantity": int, "Contractor Quantity": int})
    unequal_quantities= int_values_df[int_values_df["Drawings Quantity"]!=int_values_df["Contractor Quantity"]]
    if unequal_quantities.empty == False:
        return unequal_quantities.loc[:,["Drawings Quantity","Contractor Quantity"]]


def write_to_txt(txt_file,sub_heading,df):
    with open(txt_file, "a") as txt_file:
        txt_file.write(f" {sub_heading.strip('Schedules')} \n{df} \n\n")


# navigate to buildings folder

os.chdir("../REV 01")
path = os.path.abspath(os.curdir)
schedules = []
open("schedules_summary_windows.txt","w").close()
open("schedules_summary_doors.txt","w").close()


for file in os.listdir(path):
    if re.match(r'Schedule*', file):
        schedules.append(file)
# copy contents of files to a pandas dataframe
for schedule in schedules:
    items = ['Doors', 'Windows']
    for item in items:
        sheet_name, column, txt_file = select_schedule(item)
        df1 = read_df(f'{path}\{schedule}', sheet_name)
        df2 = clean_df(df1, column)
        write_to_txt(txt_file, schedule, df2)
