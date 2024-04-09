import pandas as pd

profiles_path = "founders_rdy2code_sb1.xlsx"

# Load the Pitchbook profiles from the personid column
profiles = pd.read_excel(profiles_path)

# Use selenium to go to the Pitchbook profile and get their Linkedin url from it
# Save the Linkedin url to a new column in the profiles dataframe
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from browsermobproxy import Server

service = Service(executable_path="/Users/rishabjain/bin/chromedriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=selenium1")  # To persist login information

bmp_path = '/Users/rishabjain/bin/browsermob-proxy-2.1.4/bin/browsermob-proxy'  # Adjust this to your BrowserMob Proxy installation path
server = Server(bmp_path)
server.start()
proxy = server.create_proxy()

chrome_options.add_argument(f'--proxy-server={proxy.proxy}')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

# Get the linkedin_urls from the profiles
linkedins = []
for i in range(len(profiles)):
    linkedins.append(profiles["linkedin_url"][i])

# create an empty text file as backup to store the linkedin urls
with open("linkedin_urls.txt", "w") as f:
    pass

def wait_for_new_tab(driver, timeout=60):
    starting_tabs = len(driver.window_handles)
    WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) > starting_tabs)
    return driver.window_handles[-1]  # Return the new tab handle

with webdriver.Chrome(service=service, options=chrome_options) as driver:
    driver.get("https://my.pitchbook.com/loginAction.do?action=sso&defaultName=")  # Start by logging in to PitchBook
    input("Log in if needed, then press Enter to continue...")
    try:
        # remove profiles from profiles who already have linkedin urls
        profiles = profiles[profiles['linkedin_url'].isnull()]

        for profile_id in profiles["personid"]:
            url = f"https://my.pitchbook.com/profile/{profile_id}/person/profile#contact-info"
            driver.get(url)

            # Wait for user to manually click on the LinkedIn button, which opens a new tab
            print("Please click the LinkedIn button. Waiting for new tab...")
            
            new_tab_handle = wait_for_new_tab(driver)
            driver.switch_to.window(new_tab_handle)  # Switch to the LinkedIn tab
            
            linkedin_url = driver.current_url
            linkedins.append(linkedin_url)
            print(f"Extracted LinkedIn URL: {linkedin_url}")

            # Save the LinkedIn URL to a text file as a backup
            with open("linkedin_urls.txt", "a") as f:
                f.write(f"{linkedin_url}\n")

            driver.close()  # Close the LinkedIn tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window
    except:
        # record the linkedins found so far to the excel, dont overwrite the already filled ones
        profiles['linkedin_url'] = linkedins

# Assuming 'profiles' DataFrame already exists
profiles['linkedin_url'] = linkedins
profiles.to_excel("founders_rdy2code_sb1.xlsx", index=False)