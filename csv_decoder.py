import os
# import datetime
import csv

'''
Contains functions to read npt csv and agents queues csv and return a list of dictionaries from each csv where the keys are the headers of each category 
Categories: agent npt, agent status, queue status

TODO: - convert times to HH:MM:SS
      - calcuate true agent npt by subtracting outbound time form npt
      - Remove unneeded columns

'''

ALPHABET_CAPITALISED = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

username = os.getlogin()
csv_path = fr"c:\Users\{username}\Downloads" #TODO: figure out how to save data form chromedriver into custom location as to not complicate user experience

def read_npt_csv() -> list:
    try:
        with open(csv_path + r'\Historical Metrics Report.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile) 
            npt_dict_list = []
            for row in reader:
                if row["Nonproductive time"] == "":
                    row["Nonproductive time"] = "0"
                if row["Online time"] == "":
                    row["Online time"] = "0"
                if row["Outbound Call time"] == "":
                    row["Outbound Call time"] = "0"
                #print(row)
                npt_dict_list.append(row)
        
        csvfile.close()
        return npt_dict_list
    except:
        print("File @ " + csv_path + r'\Historical Metrics Report.csv' + " NOT FOUND!")
        return None

def read_agents_csv() -> list:
    ''' Opens the csv downloaded from Amazon Connect,
     extracts the AGENTS section as a list of dictionaries,
     where the keys are the csv headers and the values are the row values'''
    try:
        with open(csv_path+r'\Real Time Metrics Report.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            agent_dict_list = []
            for row in reader:
                if row == [' ']: #stop when arriving at the split in the csv
                    break
                agent_dict_list.append(convert_list_to_dict(9,row,["Agent","Channels","Activity","Duration","Agent Name","Handled in","Handled out","AHT","Callback contacts handled"]))

            #delete the junk at the top
            del agent_dict_list[0]
            del agent_dict_list[0]
            del agent_dict_list[0]

            for x in agent_dict_list:
                del x["Callback contacts handled"] #remove "Callback contacts handled"" column from row
                del x["Channels"] #remove "Channels" column from row

        csvfile.close()
        return agent_dict_list
    except:
        print(csv_path+r'\Real Time Metrics Report.csv' + " NOT FOUND!")
        return None

def read_queues_csv() -> list:
    ''' Opens the csv downloaded from Amazon Connect,
     extracts the QUEUES section as a list of dictionaries,
     where the keys are the csv headers and the values are the row values'''
    try:
        with open(csv_path+r'\Real Time Metrics Report.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            queue_dict_list = []
            start_reading = False
            for row in reader:
                if row == [' ']: #wait untill arriving at the split in the csv to start reading
                    start_reading = True
                    continue
                if start_reading == True:
                    queue_dict_list.append(convert_list_to_dict(10,row,["Name","Online","NPT","In queue","Oldest","Queued","Handled","Abandoned","AHT","SL 60 secs"]))

            #delete the junk at the top
            del queue_dict_list[0]
            del queue_dict_list[0]
            del queue_dict_list[0]

        csvfile.close()
        return queue_dict_list
    except:
        print("File @ " + csv_path+r'\Real Time Metrics Report.csv' + " NOT FOUND!")
        return None

def convert_list_to_dict(length : int, row_data: list , headers : list) -> dict:
    '''convert a csv row of type list to a dict where the csv headers are the keys, and row values are pairs.'''

    output = None
    if len(row_data) == length:
        output = ({headers[x] : row_data[x] for x in range(0,length)})

    if output != None:
        return output

def remove_data_files():
    os.remove(csv_path + r'\Real Time Metrics Report.csv')
    os.remove(csv_path + r'\Historical Metrics Report.csv')
