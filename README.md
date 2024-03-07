# Human Kindness Foundation

## Creating the environment

**Backend Environment**
1. Install Anaconda if you haven't already (https://www.anaconda.com/download).
    - You can check if you have it installed already by running `conda --version` in the terminal. Alternatively, you can check that `(base)` is before every line in your terminal.
2. Create the environment by running `conda env create -n hkf -f environment.yml`. This should create the `hkf` environment in anaconda.
3. Activate the `hkf` environment by running `conda activate hkf`. You will need to do this for every new terminal session.

**Frontend Environment**
1. Run `cd frontend/hkf-react`
2. Run `npm i`. This will download all the packages you need to run the frontend. You will need to run this command agan if we ever add any new packages to the frontend (unlikely).

## Running the Application

1. Open up a new terminal (on VS Code, do this by clicking Terminal &rarr; New terminal).
2. Input `cd frontend/hkf-react` to enter the frontend codebase.
3. Run `npm i` (installs any new packages, can omit if done recently) then `npm start`. You should see be able to see our user interface after this step.
4. Open up another terminal session for the backend. *Do not reuse or close the previous one.*
5. Ensure the backend environment is running by entering `conda activate hkf` in the new terminal
6. Run `python backend/server.py` to start the backend.

Following these steps should let you run the application on your computer. You can test this by uploading **backend/Sample TX Data.xlsx** to the frontend and clicking **Find Addresses**. This should give you a new spreadsheet with updated addresses.
