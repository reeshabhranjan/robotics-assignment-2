# Robotics Assignment 2
##### Reeshabh Kumar Ranjan (2017086)

#### Configuration File
For this assignment, I have included a [configuration file](config.json). You can open this file and specify your values as needed. It is in JSON syntax. Do note that for APF, the number of ROIs (region of influence) must match the number of obstacles.

#### Program dependencies
This program is written using Python version 3.8.6. On downloading this project, first create a virtual environment using the command:

`python3 -m venv venv`

This will create a virtual environment named `venv`.

Depending on the platform, you need to activate this virtual environment. For Linux, you can do it using

`source venv/bin/activate`

Once you are in the virtual environment, install the dependencies using

`pip install -r requirements.txt`.

#### Running the program

Now, you can simply run the program using

`python main.py`

Once the program finishes execution, you will see a directory named plots created inside the present working directory. Inside that you will find three plots corresponding to each case in this assignment.
