#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import pygame
import time
import os
from getpass import getpass

# This script automates naviagtion to the Amazon connect report with the relvant data for the wallboard.
#
#

chosen_email = False
login_as_bill = True

if login_as_bill:
    chosen_email = True
    username = "william.reid@dxc.com"
    password = "SudokuOver200Puzzles!"

if login_as_bill == False:
    while chosen_email == False:

        print("welccome to the cba wallboard application, please choose a user:\n")

        print("1. william.reid@dxc.com")
        print("2. jack.courtney2@dxc.com")
        print("3. bchivers@dxc.com")
        print("4. edward.knight@dxc.com")
        print("5. daniel.eastaway@dxc.com")
        print("6. scott.large@dxc.com")
        print("7. laura.henry2@dxc.com")
        print("8. tlovell5@dxc.com")

        print("9. other")

        user_val = input("Choose User: ")

        #this should be a switch statement but i got lazy
        if user_val == "1":
            username = "william.reid@dxc.com"
            chosen_email = True
        elif user_val == "2":
            username = "jack.courtney2@dxc.com"
            chosen_email = True

        elif user_val == "3":
            username = "bchivers@dxc.com"
            chosen_email = True

        elif user_val == "4":
            username = "edward.knight@dxc.com"
            chosen_email = True

        elif user_val == "5":
            username = "daniel.eastaway@dxc.com"
            chosen_email = True

        elif user_val == "6":
            username = "scott.large@dxc.com"
            chosen_email = True

        elif user_val == "7":
            username = "laura.henry2@dxc.com"
            chosen_email = True

        elif user_val == "8":
            username = "tlovell5@dxc.com"
            chosen_email = True

        elif user_val == "9":
            username = input("Email: ")
            chosen_email = True
        else:
            print("Invalid Entry, Try again..")

    print("\nEnter password (note: characters are hidden)")
    password = getpass()

options = Options()
options.headless = True #enable/disable visiblity of the chrome instance

PATH = "chromedriver.exe" #filepath of chrome webdriver
driver = webdriver.Chrome(PATH,options=options)

driver.get("https://servicedeskofthefuture.com/")

email_search = driver.find_element(By.TAG_NAME,"input")
email_search.send_keys("@dxc.com")
email_search.send_keys(Keys.RETURN)
time.sleep(2)
button_search = driver.find_elements(By.TAG_NAME,"button")
button_search[1].click()

print("Entering Login Info...")


time.sleep(2)
login_search = driver.find_elements(By.TAG_NAME,"input")
login_search[0].send_keys(username)
login_search[1].send_keys(password)
login_button_search = driver.find_element(By.CLASS_NAME,"o-form-button-bar")
login_button_search.click()

del password

print("Waiting for MFA...")
time.sleep(3)

send_push_search = driver.find_element(By.TAG_NAME,"input")
send_push_search.click()


print("\n\n\nCHECK FOR PUSH NOTIFICATION!\n")


for i in range(20):
    time.sleep(1)
    print("waiting for ASD Supervisor Console for ... " + str(i) + " seconds...")

print("Finding link...")

try:
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div[3]/div[3]/a"))
    )
    element.click()
    
except:
    print("ASD Supervisor Console timed out, please retry... ")
    print("Make sure your login credentials were correct... ")
    print("Closing...")
    driver.quit()
    exit()


print("logged on!")

while len(driver.window_handles) < 2:
    time.sleep(1)
    print("\nWaiting for new window...")

open_windows = driver.window_handles
for window in open_windows: #switches to the first avaible window that is not the current window
  if window != driver.current_window_handle:
    driver.switch_to.window(window)
    print("switching window to: ")
    print(driver.title)

print("Finding Metrics Menu...")

try:
    metrics = WebDriverWait(driver, 90).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/ul/li[2]/div/button"))
    )
    hover = ActionChains(driver).move_to_element(metrics)
    hover.perform()
    
except:
    print("Finding metrics menu timed out... ")
    print("Closing...")
    driver.quit()
    exit()


print("Finding Saved reports...")

try:
    saved_reports = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/ul/li[2]/div/ul/a[5]/li/span"))
    )
    
except:
    print("Finding saved reports timed out... ")
    print("Closing...")
    driver.quit()
    exit()

saved_reports.click()

####

print("Finding Real Time Metrics Button...")

try:
    real_time_metrics = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/ul/li[2]/a"))
    )
    
except:
    print("Finding Real Time Metrics Button timed out... ")
    print("Closing...")
    driver.quit()
    exit()

real_time_metrics.click()


print("Searching metrics...")

try:
    metrics_search = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div/div[2]/div/metrics-report/div[2]/input"))
    )
    
except:
    print("Searching metrics timed out... ")
    print("Closing...")
    driver.quit()
    exit()
    

#metrics_search.click()
time.sleep(1)
metrics_search.send_keys("Hobart Agents and Queue")
time.sleep(1)

open_windows = driver.window_handles
for window in open_windows: #switches to the first avaible window that is not the current window
  if window != driver.current_window_handle:
    driver.switch_to.window(window)
    print("switching window to: ")
    print(driver.title)

print("Opening Hobart Agents and Queues...")

try:
    data_page_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div/div[2]/div/metrics-report/div[4]/div/table/tbody/tr/td[1]/a/span"))
    )
    
except:
    print("Opening Hobart Agents and Queues timed out... ")
    print("Closing...")
    driver.quit()
    exit()

on_data_page = False
attempts = 1
while(on_data_page == False):
    time.sleep(1)
    try:
        data_page_link.click()
        time.sleep(5)
        data_page_link.click()
        time.sleep(5)
    except:
        print(f"attempt {attempts} failed, trying again in 1 second...")
        attempts += 1
        if attempts >= 10:
            driver.quit()
            quit()
    else:
        on_data_page = True
        print("\n Successfully loaded data pages! \n")


print("Finding Historical Metrics Button...")

try:
    historical_metrics = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/ul/li[3]/a"))
        
    )
    
except:
    print("Finding Historical Metrics Button timed out... ")
    print("Closing...")
    driver.quit()
    exit()

historical_metrics.click()

try:
    historical_metrics_search = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div/div[3]/div/metrics-report/div[2]/input"))
    )
    
except:
    print("Searching historical metrics timed out... ")
    print("Closing...")
    driver.quit()
    exit()

time.sleep(1)
historical_metrics_search.send_keys("Historical - Hob only")
time.sleep(2)

print("Opening Historical - Hob only...")

try:
    historical_data_page_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div/div[3]/div/metrics-report/div[4]/div/table/tbody/tr/td[1]/a/span"))
    )
    
except:
    print("Opening Historical - Hob only metrics timed out...")
    print("Closing...")
    driver.quit()
    exit()

historical_data_page_link.click()
time.sleep(1)


driver.close()
time.sleep(1)
driver.switch_to.window(driver.window_handles[0])
driver.close()
time.sleep(1)

print("waiting 10 seconds for data to load...")
time.sleep(10)

print("done waiting, reading data...")

reading_data = True
text_write_path = r"info.txt"
text_write_path_2 = r"info2.txt"
npt_write_path = r"npt.txt"

page_number = 1

# the follow functions are called in the main wallboard script loop and are used to alternate between sets of data

def check_page_2() -> bool:
    '''
    The function returns true if a second page of agents exists (50+), 
    '''

    try:
        page2 = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/main/lily-real-time-metrics/div/div[2]/div[1]/div/div[3]/div[2]/button[2]")) #/span?
        )
        
        if page2:
            print("page 2 exists")
            return True
        else:
            print("No page 2")
            return False

    except:
        print("check failed, No page 2")
        return False


def goto_page_2():

    try:
        page2 = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-real-time-metrics/div/div[2]/div[1]/div/div[3]/div[2]/button[2]")) #/span?
        )
        
        page2.click()
        print("clicked on page 2 button")
    except:
        print("attempted to click, No page 2 button")



def goto_page_1():
    try:
        page1 = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-real-time-metrics/div/div[2]/div[1]/div/div[3]/div[2]/button[1]/span"))
        )
        page1.click()
        print("went to page 1")
    except:
        print("No page 1 available")
        

def swap_tab():
    open_windows = driver.window_handles
    for window in open_windows: #switches to the first avaible window that is not the current window
        if window != driver.current_window_handle:
            driver.switch_to.window(window)
            print("switching window to: ")
            print(driver.title)


def pull_npt():
    # grab data from body of npt page
    # save data to a text file
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(5)
    try:
        dropdown = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/historical-metrics-report/div[2]/div[2]/div[2]/div/span[2]/select"))
        )
        print("Found Dropdown box")
    except:
        print("No Dropdown available")

    select = Select(dropdown)
    select.select_by_index(2)
    time.sleep(1)

    opened_file = False
    try:
        if os.access(npt_write_path, os.R_OK):
            try:
                f = open(npt_write_path, "w")
                opened_file = True
            except:
                print("writing to file failed!")
    except:
        print("ERROR: " + npt_write_path + " doesn't exist or cannot be opened")
        
    if opened_file:
        print("writing npt data...")
        page_text = driver.find_element(By.ID, "body")
        f.write(page_text.text)
        f.close()

    #driver.switch_to.window(driver.window_handles[1])

def pull_data():

    over_page_limit = False

    driver.switch_to.window(driver.window_handles[1]) # ensures we are on the first page before reading data

    if check_page_2(): #check if there is more than <page limit> agents (normally 50)
        over_page_limit = True

    opened_file = False
    try:
        if os.access(text_write_path, os.R_OK):
            try:
                f = open(text_write_path, "w")
                opened_file = True
            except:
                print("writing to file failed!")
    except:
        print("ERROR: " + text_write_path + " doesn't exist or cannot be opened")
        
    if opened_file:
        print("writing page 1 data...")
        page_text = driver.find_element(By.ID, "body")
        f.write(page_text.text)
        f.close()


    if len(driver.window_handles) >= 2 and over_page_limit: #if more than 1 tab is open (there should always be 2 tabs open)
        driver.switch_to.window(driver.window_handles[2])

        if check_page_2(): #if not on last page, go to next page
            goto_page_2()
            time.sleep(1)

        opened_file = False
        try:
            if os.access(text_write_path_2, os.R_OK):
                try:
                    f = open(text_write_path_2, "w")
                    opened_file = True
                except:
                    print("appending to file failed!")
        except:
            print("ERROR: " + text_write_path_2 + " doesn't exist or cannot be opened")
            
        if opened_file:
            print("writing page 2 data...")
            page_text = driver.find_element(By.ID, "body")
            f.write(page_text.text)
            f.close()

        #driver.switch_to.window(driver.window_handles[1])

        #time.sleep(1)

