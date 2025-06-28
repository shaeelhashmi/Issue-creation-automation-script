## Overview:
This is an automation script that copies issues from a repository and makes the issues in another repository, it can differentiate same issues on the basis of their titles
## Techstack:
* Python
* Selenium
## Getting Started:
### Pre-requisites:
* Make sure you have python installed in your pc.
### Video Demonstration:
Watch the video to see the website in action.Video link [here](https://www.youtube.com/watch?v=1PL5lTWOEAU)
### Installation:
To run this project locally follow the following steps:
* You can install the zip file of the project from [here](https://github.com/shaeelhashmi/Issue-creation-automation-script)
* If you have Git installed, type the following command in your terminal:
```
git clone https://github.com/shaeelhashmi/Issue-creation-automation-script
```
* Then run 
```
cd Issue-creation-automation-script
```
* Once in the project directory run the following command to download the necessary packages
```
pip install -r requirements.txt
```
* Or you can install it using git:
```
git clone https://github.com/shaeelhashmi/shaeelhashmi/Issue-creation-automation-script
```
### Setting up envirnment:
Create a .env file and add the following things in it:<br>
* Repo_for_Making_Issues: GitHub repository URL where new issues will be created.

* Repo_for_Copying_Issues: GitHub repository URL from where issues will be copied.

* FireFox_Profile_Path: Path to your custom Firefox profile (used for maintaining login sessions with Selenium).

* Gecko_Driver_Path: Path to the GeckoDriver executable used by Selenium with Firefox.

* Total_Issues: The number of issues you want to copy or create. Set it to 0 if using dynamic detection.
### Execution:
Once all the steps are completed,type the following command in your terminal:
```
python issues.py
```
