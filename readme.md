#Tunts.Rocks Challenge
Author: Leonardo Assis Gaspar

## Descripition

This project was created for the Tunts.Rocks callenge. Follow the instructions
below on how to install and use it.

## Instalation

### Step 1(optional): Create a virtual environment
- Install virtualenv:
`pip install virtualenv`

- Create a new environment:
`python3 -m venv myenv`

- Activate the environment just created:
On Windowns:
`.\myenv\Scripts\activate`
On Linux or MacOs:
`source myenv/bin/activate`

### Step 2: Install dependencies

- Use te following command to install all necessary dependencies for this
project:
`pip install -r requirements.txt`

### Step 3: Guarantee access

- Make sure you have your credential file in the same directory as the 'src.py'
file;
- Check if your credential file is called 'credentials.json', if it isn't you
need to change it in the 'config.py' where it says 'credentials.json';
- Also while in the 'config.py' file, paste your spreadsheet id where it says
'paste_your_id_here'.