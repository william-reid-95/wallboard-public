#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import time
from getpass import getpass

# This script automates naviagtion to the Amazon connect report with the relvant data for the wallboard.

debug = True #print extra info for debugging if needed

chosen_email = False
login_as_admin = False

if login_as_admin: #bypass login process for testing
    chosen_email = True
    username = "xxxx"
    password = "xxxx"

if login_as_admin == False:
    while chosen_email == False:

        print("welcome to the wallboard application, please choose a user:\n")

        username = input("Email: ")

    print("\nEnter password (note: characters are hidden)")
    password = getpass()


### Configure webdriver ###
options = Options()
#options.headless = True #enable/disable visiblity of the chrome instance
#options.add_argument('--headless')
options.add_argument('--window-size=800,600')
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

PATH = "chromedriver.exe" #filepath of chrome webdriver
driver = webdriver.Chrome(PATH,options=options)

### Start script ###
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

metrics_found = False
metrics_attempts = 0
while metrics_found == False:
    metrics_attempts += 1 
    print(f"attempt: {metrics_attempts}")
    if metrics_attempts >= 50:
        print("Finding metrics menu timed out... ")
        print("Closing...")
        driver.quit()
        exit()

    print("waiting 2 seconds")
    time.sleep(2)
    print("Finding Metrics Menu now...")
    try:
        metrics = WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/ul/li[2]/div/button")))
        print("hovering")
        hover = ActionChains(driver).move_to_element(metrics)
        hover.perform()
        metrics_found = True
        break

    except:
        print("could not hover metrics button!")



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
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-saved-reports/div/div[1]/button[2]"))
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
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-saved-reports/div/div[2]/div/div[1]/div/input"))
    )
    
except:
    print("Searching metrics timed out... ")
    print("Closing...")
    driver.quit()
    exit()
    

#metrics_search.click()
time.sleep(1)
metrics_search.send_keys("Hobart")
time.sleep(1)

open_windows = driver.window_handles
for window in open_windows: #switches to the first avaible window that is not the current window
  if window != driver.current_window_handle:
    driver.switch_to.window(window)
    print("switching window to: ")
    print(driver.title)

print("Opening Hobart Agents and Queues...")

time.sleep(5)

try:
    data_page_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-saved-reports/div/div[3]/table/tbody/tr[2]/td[1]/div/a/span"))
    )
    
except:
    print("Opening Hobart Agents and Queues timed out... ")
    print("Closing...")
    driver.quit()
    exit()

time.sleep(5)
data_page_link.click()

print("Finding Historical Metrics Button...")

try:
    historical_metrics = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-saved-reports/div/div[1]/button[3]"))
        
    )
    
except:
    print("Finding Historical Metrics Button timed out... ")
    print("Closing...")
    driver.quit()
    exit()

historical_metrics.click()

try:
    historical_metrics_search = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-saved-reports/div/div[2]/div/div[1]/div/input"))
    )
    
except:
    print("Searching historical metrics timed out... ")
    print("Closing...")
    driver.quit()
    exit()

time.sleep(1)
historical_metrics_search.send_keys("Hobart")
time.sleep(2)

print("Opening Hobart - Bill (WB)...")

try:
    historical_data_page_link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-saved-reports/div/div[3]/table/tbody/tr[1]/td[1]/div/a/span"))
    )
    
except:
    print("Opening Hobart - Bill (WB) metrics timed out...")
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

print("waiting 5 seconds for data to load...")
time.sleep(5)

print("done waiting, reading data...")

reading_data = True

driver.switch_to.window(driver.window_handles[1])

#download csv functions (called in main script)

def swap_window():
    '''Switches to the first avaible window that is not the current window'''
    open_windows = driver.window_handles
    for window in open_windows:
        if window != driver.current_window_handle:
            driver.switch_to.window(window)
            print("switching window to: ")
            print(driver.title)

def pull_npt():

    if(debug): print('downloading npt csv')

    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(1)
    try:
        options_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div[1]/div/div/div/div/span"))
        )
    except:
        pass

    options_button.click()
    try:
        csv_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div[1]/div/div/ul/li[2]/a"))
        )
    except:
        pass
    
    csv_button.click()

    if(debug): print('finished downloading npt csv')


def pull_data():

    if(debug): print('downloading agent csv')

    driver.switch_to.window(driver.window_handles[1]) # ensures we are on the first page before reading data
    driver.refresh()
    time.sleep(1)
    #downlaod csv
    try:
        options_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/main/lily-real-time-metrics/div/div[1]/div/div[2]/button/span[1]"))
        )
    except:
        pass

    options_button.click()

    try:
        csv_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/ul/li[3]"))
        )
    except:
        pass
    
    csv_button.click()

    if(debug): print('finished downloading agent npt csv')


pull_data()