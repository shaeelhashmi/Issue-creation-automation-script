
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions


def getPagesLength(browser):
    try:
        element=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/react-app/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/nav")
        pages=element.find_elements(By.TAG_NAME,"a")
        return len(pages)-2
    except selenium.common.exceptions.NoSuchElementException:
        return 1
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
repo_for_making_issues="https://github.com/shaeelhashmi/Issue-testing"
repo_for_copying_issues="https://github.com/enatega/food-delivery-multivendor"
browser.get(f"{repo_for_making_issues}/issues")
time.sleep(5)
already_made_issues=[]
length=getPagesLength(browser)
print(length)

j=1
already_made_issues_set = set()
while j<=length:
    print(f"Page {j}")
    browser.get(f"{repo_for_making_issues}/issues?page={j}")
    time.sleep(5)
    already_made_issues=browser.find_elements(By.CLASS_NAME,"IssueRow-module__row--XmR1f")
    for issue in already_made_issues:
        text=issue.find_element(By.TAG_NAME,"a").text
        already_made_issues_set.add(text)

    print(len(already_made_issues))
    j+=1

time.sleep(5)
print("Visiting......")
dictionary={}
elementCount=0

browser.execute_script(f"window.open('{repo_for_copying_issues}/issues?page=1', '_blank');")

browser.switch_to.window(browser.window_handles[-1])

time.sleep(5)


length=getPagesLength(browser)
print(length)

browser.close()

browser.switch_to.window(browser.window_handles[0])

i=1

while elementCount < 10 and i<=length:
    print(f"Page {i}")
    browser.execute_script(f"window.open('{repo_for_copying_issues}/issues?page={i}', '_blank');")

    browser.switch_to.window(browser.window_handles[-1])

    time.sleep(5)

    elem=browser.find_elements(By.CLASS_NAME,"IssueRow-module__row--XmR1f")

    for element in elem:

        try:

            link=element.find_element(By.TAG_NAME,"a").get_attribute("href")

            browser.execute_script(f"window.open('{link}', '_blank');")

            browser.switch_to.window(browser.window_handles[-1])

            time.sleep(5)

            description = WebDriverWait(browser, 40).until(
                EC.presence_of_element_located((By.CLASS_NAME, "markdown-body"))
            ).get_attribute("outerHTML")

            print("Description read")

            title= WebDriverWait(browser, 40).until(
                EC.presence_of_element_located((By.TAG_NAME, "bdi"))
            ).text

            print("title read")
            labelBox=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div/main/react-app/div/div/div/div/div[7]/div/div[2]/div/div[2]/div[2]/div")
            labelsLinks=labelBox.find_elements(By.TAG_NAME,"a")
            labels=[]
            for label in labelsLinks:
                span=label.find_element(By.TAG_NAME,"span")
                bg_color = span.value_of_css_property("background-color")  
                labels.append((label.text, bg_color))
            print(labels)
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
    i+=1
    browser.switch_to.window(browser.window_handles[0])

print(len(dictionary))
browser.execute_script(f"window.open('{repo_for_making_issues}/issues/new?template=BLANK_ISSUE', '_blank');")
browser.close()
browser.switch_to.window(browser.window_handles[0])
time.sleep(5)
checkbox=browser.find_element(By.ID,":r1i:")
if not checkbox.is_selected():
    checkbox.click()

for key in dictionary:
    TitleBoxBox=browser.find_element(By.CLASS_NAME,"CreateIssueFormTitle-module__container--jYx17")
    print(TitleBoxBox.text)
    TitleBoxBox.find_element(By.TAG_NAME,"input").send_keys(key)
    time.sleep(3)
    print(key)
    textBoxBox=browser.find_element(By.CLASS_NAME,"CreateIssueForm-module__commentBox--yWrlH")
    textArea=textBoxBox.find_element(By.TAG_NAME,"textarea")
    textArea.click()
    textArea.send_keys(dictionary[key])
    print(dictionary[key])
    print("Creating issue",key)
    button=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/react-app/div/div/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button[2]")
    button.click()
    time.sleep(5)

browser.quit()