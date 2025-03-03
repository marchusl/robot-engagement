# QTRobot - HTX Group Ideation Exercise Demo - MED7 Group 2 - Fall 2024
Repository for the project “Adaptive Media Systems” at 7. Semester Medialogy, Fall 2024 

Created by
- Marcus (Marchusl), Markus (Tannez), Mathias (MatDevelopment) and Rasmus (RasmusKanne)

![Visual](Images/QTRobotTitlePic.png)

## Overview of Project
The idea of the project is to create an ideation exercise facilitated by the QTRobot by utilizing ChatGPT APIs. The current implementation was intended to incorporate an engagement detection model to test how such an implementation would affect the experience of having a group discussion with the robot, but ended up not being ready for the deadline of the project so it is scripted based on user input.

Features:
- The robot uses the microphone input of the users to generate LLM based responses through ChatGPT
- It remembers what each participant said during their round to more accurately come up with questions related to the current participant and context of the discussion.

## Running It
1. Clone or Download the project to an external computer other than the robot
2. Download relevant python packages (OpenAI + PyAudio)
3. Setup ChatGPT API key environment variable in windows (Name it “OPENAI_API_KEY”)
4. Make sure both the computer and the robot is connected to the same WiFi 
5. Run the “main.py” script on the external computer
6. Replace the “SERVER” variable in the “Client_test.py” script on the robot to the IP address shown on the external computers console
7. Run the “Client_test.py” script on the robot and wait for confirmation that it connected
8. Press “space” on the external computer to start the exercise

## Project Parts

### Scripts
- main.py - The main script which structures the experience and calls function in a specific order
- ServerScript.py - Handles the communication between the external computer and the robot, by sending string commands through socket streaming
- Client_Test.py - Receives and processes commands from the computer to run ROS commands like talking, changing the screen, gesturing, etc.

## Configurations

### Connecting the Robot to the WiFi
Before anything is done, you need to ensure that the robot and the pc that you are working with are connected to the same network. The process of connecting the robot to the internet is described in LUXAI’s documentation [LuxAI.com/docs](https://docs.luxai.com/docs/intro_code), but to try and simplify the process we will describe it here:

#### 1. QTrobot’s QTPC and QTRP 
The robot consists of two PC’s: QTPC (the one you work on via mouse and keyboard) and QTRP. The network connection is part of the QTRP which you have to connect to within the terminal of the QTPC. To access the QTRP you have to follow these steps

#### 2. Accessing QTRP
In the terminal, write the following code to access the QTRP:

*ssh developer@192.168.100.1*

The password to enter is *qtrobot*, all in small caps. (NOTE: You won’t be able to see what you write, when entering the password)

#### 3. Accessing Network configuration file
Once you are on the QTRP, you have to enter the following file path and then access the *wpa_supplicant-wlan0* configuration file using the *sudo nano* command:

*cd /etc/wpa_supplicant*
*sudo nano wpa_supplicant-wlan0.conf*

#### 4. The config file
If you don’t already see this text within the configuration file, then write it in:

*country=LU*
*ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev*
*update_config=1*

*network={
    ssid="<your_router_SSID>"
    psk="<your_router_passphrase>"         
}*

The only thing you have to specify is “your router SSID” (Name of the network you want to connect to) and “your router passphrases” (Password to the network)

Once written save the file with CTRL+S and then exit with CTRL+X

#### 5. Restart Client
Write this in the console to restart the network, so that the PC can connect to the new network:

*sudo systemctl restart qt_wlan0_client.service*

#### 6. Verify connection
To see if you are connected you can try to ping google, by writing the following:

*ping www.google.com*

You should see messages printed in the console that indicate it is pinging google. Use CTRL+C to make it stop pinging

#### 7. Make connection permanent
To make the connection permanent, write the following lines in the command line:

*sudo systemctl enable qt_wlan0_client.service*

*sudo systemctl disable qt_wlan0_ap.service*

You are now ready to go back to the QTPC to continue your work. (you can close the console and open it again, or make a new tab in the console to return to the QTPC. Alternatively you can write *ssh developer@QTPC* and again write the password *qtrobot*)
