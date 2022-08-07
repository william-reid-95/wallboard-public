#statsGUI by William Reid started 12/11/2021
#main

autologin_enabled = False #disabled login function

if autologin_enabled:
    import autologin as autologin

import datetime 
from itertools import count
from operator import imod
from wallboard_functions import *
import csv_decoder
from os.path import exists
import time

### config ###

username = os.getlogin()
data_path = fr"c:\Users\{username}\Downloads"

default_row_x = 180
default_row_y = 24

default_block_width = 180
default_block_height = 24

queue_default_row_x = 160
queue_default_block_width = 160

queue_enabled = True
agents_enabled = True

### init variables ###

clock = pygame.time.Clock()
t = time.localtime()

refresh_time = 4 # seconds
tick_rate = 6 #ticks per second
timer = 0

npt_pull_refresh_count = 0 #number of refreshes since npt was pulled
npt_pull_refresh_times = 10 #number of refreshes tow ait before pulling npt

sla_thermometer.draw()
sla_thermometer_string = "0"

### main loop ###

is_running = True

while is_running:
    
    current_time = datetime.datetime.now()

    clock.tick(tick_rate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))

    pygame.draw.rect(background,(1+(5*timer),1+(5*timer),1+(5*timer)),((54,1050),(72*(timer+1),8))) # loading bar down the bottom

    if timer >= (tick_rate * refresh_time):

        timer = 0

        if autologin_enabled: # calls the functions to navigate to csv download buttons on webpage and download csv files
            time.sleep(2)
            if not exists(data_path + r'\Real Time Metrics Report.csv'):
                autologin.pull_data()
            time.sleep(2)
            if not exists(data_path + r'\Historical Metrics Report.csv'):
                autologin.pull_npt()
            
        time.sleep(5)

        if exists(data_path + r'\Real Time Metrics Report.csv') and exists(data_path + r'\Historical Metrics Report.csv'):
            print(f" - [{current_time}] Succesful refresh")
            queue_reader = csv_decoder.read_queues_csv() #KEYS: "Name","Online","NPT","In queue","Oldest","Queued","Handled","Abandoned","AHT","SL 60 secs"
            agent_reader = csv_decoder.read_agents_csv() # KEYS: "Agent","Activity","Duration","Agent Name","Handled in","Handled out","AHT"
            npt_reader = csv_decoder.read_npt_csv() # KEYS: "Agent","Nonproductive time","Online time","Outbound Call time"
            csv_decoder.remove_data_files() #delete files
        else:
            print(f" - [{current_time}] Failed refresh")
            queue_reader = None
            npt_reader = None
            agent_reader = None

        if(agents_enabled):
            row_number = 1
            if agent_reader != None and npt_reader != None:
                for agent in agent_list:
                    npt_found = False
                    agent_npt = None
                    for npt in npt_reader:
                        if npt["Agent"] == (agent.email):
                            true_npt_seconds = (int(npt["Nonproductive time"]) - int(npt["Outbound Call time"]))
                            agent_npt = str(datetime.timedelta(seconds = true_npt_seconds))
                            npt_found = True
                            break #stop looking for npt for agents

                    found_row = False
                    for row in agent_reader:
                        if row['Agent'] == agent.email: #if email adress in row matches agent email
                            #create or update agent's GUI row
                            if agent_npt:
                                row["True NPT"] = agent_npt 
                            else:
                                row["True NPT"] = "???"

                            #print(row)
                            found_row = True
                            agent.agent_row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row)
                            break

                    if found_row == False:
                        agent.agent_row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, {"Agent" : agent.email,"Activity" : "Offline","Duration" : "EoS", "Agent Name" : agent.l_name + " " + agent.f_name,"Handled in" : "-","Handled out" : "-","AHT" : "00:00:00","True NPT" : "-"})
                    row_number += 1

        if(queue_enabled):
            if queue_reader != None:
                for queue_row in queue_reader:
                    for queue in queue_list:
                        if queue_row["Name"] == queue.name:
                            queue.queue_row(queue_list.index(queue)+1, queue_default_row_x, default_row_y, queue_default_block_width, default_block_height, queue_row)
                    if queue_row["Name"] == "Summary":
                        sla_thermometer_string = queue_row["SL 60 secs"].split("%")[0]

        if agent_reader != None:
            stats_available.reset_count()
            stats_on_contact.reset_count()
            stats_ticketing.reset_count()
            stats_on_break.reset_count()
            stats_offline.reset_count()
            stats_other.reset_count()

            for row in agent_reader:# count all agents in given catagories
                if row["Activity"] == "On contact":
                    stats_on_contact.amount += 1
                elif row["Activity"] == "Available":
                    stats_available.amount += 1
                elif row["Activity"] == "Incoming":
                    stats_on_contact.amount += 1
                elif row["Activity"] == "Outbound Call":
                    stats_on_contact.amount += 1
                elif row["Activity"] == "Training":
                    stats_other.amount += 1
                elif row["Activity"] == "Meetings":
                    stats_other.amount += 1
                elif row["Activity"] == "Projects":
                    stats_other.amount += 1
                elif row["Activity"] == "Missed":
                    stats_available.amount += 1
                elif row["Activity"] == "Ticketing":
                    stats_ticketing.amount += 1
                elif row["Activity"] == "After contact work":
                    stats_ticketing.amount += 1
                elif row["Activity"] == "Short Break":
                    stats_on_break.amount += 1
                elif row["Activity"] == "Lunch Break":
                    stats_on_break.amount += 1
                elif row["Activity"] == "Comfort Break":
                    stats_on_break.amount += 1
                elif row["Activity"] == "Offline Tasks":
                    stats_other.amount += 1
                elif row["Activity"] == "System Down":
                    stats_other.amount += 1
                elif row["Activity"] == "Offline":
                    stats_offline.amount += 1
                else:
                    stats_other.amount += 1

        for stats in stats_list:
            stats.stats_row(stats_list.index(stats)+1, queue_default_row_x, default_row_y, queue_default_block_width, default_block_height)


    timer += 1

    sla_thermometer.update(sla_thermometer_string)
    sla_thermometer.draw()

    pygame.display.update()

if autologin_enabled:
    autologin.driver.quit()

