# Service-Monitor
## Monitoring Services On A Machine 
### About The Project
This project is about monitoring services on a machine (computer), capturing the logs of the running services, representing any changes between samples of every two consecutive samples of capturing and between specific two samples (manual mode).
### Program Structure
- The program checks which operating system is used (Win\Linux).
- Afterwards, the program requires the user to input a number which represents the time interval between the samples in seconds.
- Then, the capturing process starts, and two log files are created:
  - serverList.txt : list of all the running servers at each time stamp.
  - Status_Log.txt: list of all changes occurred between consecutive samples.
- __Monitor__ mode is active all the time when the program is running.
  - Whenever a change occurred it will be shown in our GUI window.
- __Manual Mode__ is activated when the user inputs two specific time stamps. 
  - When this is activated, the changes between the chosen time stamps will appear in the GUI window (if there are any changes).
### External Libraries
- Psutil
  - __IMPORTANT NOTE__: to be able to run the project you should install the psutil package via your favorite     package installer.
  - The pip command is: pip install psutil
  - Used for functions that provide access to operating system's services.
- Hashlib
  - Used for algorithms of hashing.
- Time, datetime
  - An api containing many useful time functions.
- Tkinter
  - Used for the GUI class.
- Platform
  - Used to recognize the OS (if it's win or linux).
- Subprocess
  - We Used it to get information about services in Linux.
- Thread
  - Used for the GUI windows.
### Classes & Data Structures
- Module named "main" – there are the main functions of the program (the algorithms).
- Class named "GUI" – the view of the program.
- List of services.
- Dictionary to store the services in a 'key' : 'value' format of 'service name' : 'status'.
### Security
At the main functions of monitor mode and manual mode we check if a file was changed from outside, if it is a warning will appear:
![image](https://user-images.githubusercontent.com/93203695/182890147-afdc4a3b-9091-48a7-a084-af6d06a580bd.png)
### GUI
All the interactions with the program performed using the GUI windows.
- __Usage__
  - Here the user needs to enter a number:
  ![image](https://user-images.githubusercontent.com/93203695/182890440-81ff7991-5854-4775-9e75-959e83c56332.png)
  - In this window, all the changes between samples are shown:
  ![image](https://user-images.githubusercontent.com/93203695/182890595-e49e4cc2-1bdb-43a8-842f-8fb677b12a1e.png)

  - If manual mode is desired, the user needs to enter at the bottom of the window two dates in the correct format:
  ![image](https://user-images.githubusercontent.com/93203695/182890672-8d549d15-c9ef-4e96-b15c-4a3112bb6288.png)

  - Then, if there are any changes occurred, it will be represented in the window:
  ![image](https://user-images.githubusercontent.com/93203695/182890737-bdd6986d-d54c-4fdd-97df-196835b8fa9d.png)

  - To exit the program the user can press the red X button on the upper right corner.
  
  
