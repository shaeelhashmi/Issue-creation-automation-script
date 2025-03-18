from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to geckodriver
gecko_path = "C:/Users/Shaeel/Downloads/geckodriver-v0.36.0-win64/geckodriver.exe"

# Path to your existing Firefox profile
firefox_profile_path = "C:/Users/Shaeel/AppData/Roaming/Mozilla/Firefox/Profiles/0y94p5y9.default-release"

# Configure Firefox options
options = Options()
options.add_argument("-profile")
options.add_argument(firefox_profile_path)

# Set up the Firefox driver with the profile
service = Service(gecko_path)
browser = webdriver.Firefox(service=service, options=options)
browser.get("https://github.com/shaeelhashmi/Issue-testing/issues")
time.sleep(5)
already_made_issues=browser.find_elements(By.CLASS_NAME,"IssueRow-module__row--XmR1f")
# Create a hash set to store already made issues
already_made_issues_set = set()

# Add all the already made issues to the hash set
for issue in already_made_issues:
    text=issue.find_element(By.TAG_NAME,"a").text
    print(text)
    already_made_issues_set.add(text)

browser.execute_script(f"window.open('https://github.com/shaeelhashmi/Issue-testing/issues/new?template=BLANK_ISSUE', '_blank');")
browser.close()
browser.switch_to.window(browser.window_handles[0])
time.sleep(5)
print("Visiting......")
dictionary={}
elementCount=0
while elementCount < 10:
    browser.execute_script(f"window.open('https://github.com/enatega/food-delivery-multivendor/issues?page=1', '_blank');")
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(5)
    elem=browser.find_elements(By.CLASS_NAME,"IssueRow-module__row--XmR1f")
    for element in elem:
        try:
            link=element.find_element(By.TAG_NAME,"a").get_attribute("href")
            browser.execute_script(f"window.open('{link}', '_blank');")
            browser.switch_to.window(browser.window_handles[-1])
            
            description = WebDriverWait(browser, 40).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/main/react-app/div/div/div/div/div[7]/div/div[1]/div[1]/div/div/div/div/div[2]/div[1]"))
            ).get_attribute("outerHTML")
            title=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div/main/react-app/div/div/div/div/div[1]/div/div/div[1]/h1/bdi").text
            if title in already_made_issues_set:
                raise Exception("Already made issue")
            dictionary[title] = description
            
            elementCount+=1
            if elementCount>=10:
                break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])

    browser.close()
    
    browser.switch_to.window(browser.window_handles[0])

print(len(dictionary))

checkbox=browser.find_element(By.ID,":r1i:")
if not checkbox.is_selected():
    checkbox.click()
for key in dictionary:
    browser.find_element(By.ID,":r1:").send_keys(key)
    browser.find_element(By.ID,":r6:").send_keys(dictionary[key])
    button=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/react-app/div/div/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button[2]")
    button.click()
    time.sleep(5)

time.sleep(10)
browser.quit()

