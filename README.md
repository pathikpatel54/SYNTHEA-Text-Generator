# SYNTHEA-Text-Generator

# Instruction Manual for Accessing Text Generation:

1. Download Python 3:

If you don't already have Python 3 installed on your computer, you'll need to download it. You can download Python 3 from the official website at https://www.python.org/downloads/. Select the version that is appropriate for your operating system, and then follow the installation instructions.

2. Extract the project zip file:

Once the project zip file is downloaded, you can extract it to a location on your computer. You can do this by right-clicking on the zip file and selecting "Extract All" or by using a program like WinZip or 7-Zip.

3. Open the Terminal/Command Prompt:

Open the Terminal on your computer by searching for "Terminal/Command Prompt" in your operating system's search bar or by pressing the "Command + Space" keys and then typing "Terminal" in the search bar.

4. Navigate to the project directory:

Use the "cd" command in the Terminal to navigate to the directory where you extracted the project files. For example, if the project files are in the "Downloads" folder, you would type "cd Downloads" in the Terminal.

5. Run the project files:

Once you have successfully navigated to the project directory, you can run the project files using Python 3. This can be done by typing "python3 main.py" in the Terminal. This will execute the main Python file for the project.

6. Enter login credentials:

Once you have executed main.py in project folder, you can enter your login credentials to access the database.

7. Verify the results:

Once the result generation is complete, you can verify the results by checking the output folder. The output folder should contain the generated results, and you can check them to ensure that they are correct.

The project contains template.json file that define the templates used in the database project. Each template is defined step by step in the template.json files. 

Here is a step-by-step description of the different sections and templates of the JSON file:

## Templates#1: 

- "PATIENT_DEMOGRAPHICS" which includes three keys named "part_1", "part_2", and "part_3". 

- "part_1" key contains a list of 10 different strings which are used to represent the basic information of a patient including their first name, last name, age, gender, address, and city. These strings contain placeholders such as "{:FIRST_NAME:}", "{:LAST_NAME:}", "{:AGE:}", "{:GENDER:}", "{:ADDRESS:}", and "{:CITY:}" which will be replaced with actual values when generating the patient's information.

- "part_2" key contains a list of two different strings which are used to represent the marital status of a patient. These strings contain a placeholder named "{:MARITAL:}" which will be replaced with actual values when generating the patient's information. This part will only be included for patients who provide their marital status.

- "part_3" key contains a list of two different strings which are used to represent the race information of a patient. These strings contain a placeholder named "{:RACE:}" which will be replaced with actual values when generating the patient's information. This part will only be included for patients who provide their race information.

The code can be used to generate patient demographic information by selecting one of the strings from "part_1" key and filling in the placeholders with actual values. If the patient provides their marital status, one of the strings from "part_2" key can be selected and the "{:MARITAL:}" placeholder can be
