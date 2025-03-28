from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
import re
def show_labels(browser):
        CreateLabelButtonBox = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/main/react-app/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]"))
        )
        CreateLabelButton = CreateLabelButtonBox.find_element(By.TAG_NAME, "button")
        CreateLabelButton.click()
def get_label_button(browser):
    try:
        show_labels(browser)
        time.sleep(5)
        Repo_labels_Box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[2]"))
        )
        Repo_labels = Repo_labels_Box.find_elements(By.TAG_NAME, "li")
        return Repo_labels
    except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException) as e:
        print(f"Error finding label button: {e}")
        return []


def rgba_to_hex(rgba):
    # Extract the RGBA values using regex
    match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgba)
    if match:
        r, g, b = match.groups()
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    return rgba


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
repo_for_making_issues="https://github.com/patriciaperez90/script-for-food"
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
labels_set = {}
total_elements=10
while elementCount < total_elements and i<=length:
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
            try:
                labelBox=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div/main/react-app/div/div/div/div/div[7]/div/div[2]/div/div[2]/div[2]/div")
                labelsLinks=labelBox.find_elements(By.TAG_NAME,"a")
                labels=[]
                for label in labelsLinks:
                    span=label.find_element(By.TAG_NAME,"span")
                    bg_color = span.value_of_css_property("background-color")
                    text=label.find_element(By.CLASS_NAME,"prc-Text-Text-0ima0").text
                    text=text.strip()
                    labels.append(text)
                    labels_set[text] = rgba_to_hex(bg_color)
                print(labels)
            except selenium.common.exceptions.NoSuchElementException:
                labels=[]
            if title in already_made_issues_set:
                raise Exception("Already made issue")
            labels = [label.lower() for label in labels]
            dictionary[title] = (description, labels)
            
            elementCount+=1
            if elementCount>=total_elements:
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
# Creating labels
Repo_labels=get_label_button(browser)
print(len(Repo_labels))
lowerCase_labels_set = {}
for label in labels_set:
    lowerCase_labels_set[label.lower()] = label
for label in Repo_labels:
    text=label.find_element(By.CLASS_NAME,"prc-Text-Text-0ima0").text
    text=text.strip()
    text=text.lower()
    print(text)
    if text in lowerCase_labels_set:
        print("Deleting label",text)
        
        del labels_set[lowerCase_labels_set[text]]
        del lowerCase_labels_set[text]
browser.execute_script(f"window.open('{repo_for_making_issues}/issues/labels', '_blank');")
browser.switch_to.window(browser.window_handles[-1])
for label in labels_set:
    print("Creating label",label)
    time.sleep(5)
    labelCreationButtonBox=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div/main/turbo-frame/div/div/div/div[1]/div[3]")
    labelCreationButton=labelCreationButtonBox.find_element(By.TAG_NAME,"button")
    labelCreationButton.click()
    time.sleep(5)
    labelCreationBox=WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/main/turbo-frame/div/div/div/form/div[2]"))
    )
    labelName=labelCreationBox.find_element(By.ID,"label-name-")
    labelName.clear()
    labelName.send_keys(label)
    labelColor=labelCreationBox.find_element(By.ID,"label-color-")
    labelColor.clear()
    labelColor.send_keys(labels_set[label])
    ButtonBox=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div/main/turbo-frame/div/div/div/form/div[2]/div")
    Button=ButtonBox.find_elements(By.TAG_NAME,"button")[1]
    Button.click()
    time.sleep(5)
browser.close()
browser.switch_to.window(browser.window_handles[0])

## Creating issues


checkbox=browser.find_element(By.ID,":r1i:")
if not checkbox.is_selected():
    checkbox.click()
for key in dictionary:
    browser.refresh()
    time.sleep(5)
    ## Creating labels
    show_labels(browser)
    time.sleep(5)
    labels_to_make=dictionary[key][1]
    for label_to_make in labels_to_make:
        try:
            input_Box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[2]/div[1]"
            ))
            )
            input = input_Box.find_element(By.TAG_NAME, "input")
            input.click()
            input.clear()
            input.send_keys(label_to_make)
            time.sleep(3)
            labelBox=browser.find_element(By.XPATH,"/html/body/div[4]/div[3]/div/div/div[2]/div[2]")
            labels=labelBox.find_elements(By.TAG_NAME,"li")
            
            for label in labels:
                

                text=label.find_element(By.CLASS_NAME,"prc-Text-Text-0ima0").text
                text=text.strip()
                text=text.lower()
                if text in dictionary[key][1]:
                    element=label.find_element(By.CLASS_NAME,"prc-ActionList-MultiSelectCheckbox-nK6PJ")
                    browser.execute_script("arguments[0].click();", element)
                    time.sleep(2)
                    break
        except Exception as e:
            print(e)

        
    time.sleep(5)
    TitleBoxBox=browser.find_element(By.CLASS_NAME,"CreateIssueFormTitle-module__container--jYx17")
    TitleArea=TitleBoxBox.find_element(By.TAG_NAME,"input")
    TitleArea.click()
    TitleArea.send_keys(key)
    time.sleep(3)
    print(key)
    textBoxBox=browser.find_element(By.CLASS_NAME,"CreateIssueForm-module__commentBox--yWrlH")
    textArea=textBoxBox.find_element(By.TAG_NAME,"textarea")
    textArea.click()
    textArea.send_keys(dictionary[key][0])
    print(dictionary[key])
    print("Creating issue",key)
    button=browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/main/react-app/div/div/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button[2]")
    button.click()
    time.sleep(5)
time.sleep(5)
browser.quit()