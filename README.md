# LOST AND FOUND FOX - fingerprint-locker-with-weight-sensor
Final project of the Design and System Thinking course - Summer 2022 at Fulbright Univeersity Vietnam

In this project, our group built a lost and found box for Fulbright students to centralize and save time on the lost - found process. 

**Overview**

With the fingerprint locker, only Fulbright students and people that have registered can open the box, making it security. In order to recognize whether user put an item in or take an item out, we add a weight sensor (load cell 50kg) to record the weight status of the box. Then, all the data will be processed and stored into a csv file (using Python).

**Composition**
- Arduino Uno Compatible
- Solenoid Lock LY-03 with relay
- AS608 Fingerprint Sensor 
- Loadcell 50Kg and ADC 24bit Loadcell HX711

How to use the box

**1.1. User registeration**

- Description: In order to use the box, user must register the fingerprint. Then, the admin needs to update the user's information file.
- Instruction:
  - Step 1: Download the "Adafruit Fingerprint Sensor Library" and add to the Arduino library
  - Step 2: Open Arduino IDE --> Choose "File" --> Choose "Examples" --> Choose "Adafruit Fingerprint Sensor Library" --> Open "enroll" file
  - Step 3: Enroll fingerprint and update the user's information database (Format: [user_information.csv](https://github.com/ngantran03/fingerprint-locker-with-weight-sensor/files/9542356/user_information.csv))

**1.2. Operating**
- User journey: User scans fingerprints --> Fingerprint sensor verifies --> If yes --> The solenoid lock unlocks and the loadcell print out the weight status --> Delay for 10 seconds --> The solenoid lock locks (User can still close the door even when the lock is locked)
- Instruction:
  - Step 1: Download the "fingerprint_locker_weight_sensor.ino" file and the HX711 library (instruction in the "fingerprint_locker_weight_sensor.ino")
  - Step 2: Upload the code to Arduino using USB cable
  - Step 3: Download the "data processing and storing.py" file
  - Step 4: Run the "data processing and storing.py" file
  - Step 5: Start the user journey

**1.3. Data processing and storing**
- Description: 
  - Data processing:
    - Match the fingerprint ID from Arduino output with the user's information in the user's information database
    - Since we do not know when the box is closed, my way of retrieving the weight status after closing the box of the first user is using the wight status before opening of the second user 
  - Data storing:
    - After a certain number of loops (as we define when running the Python code), the output will be stored in a csv file
