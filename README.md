# home-security-system
Edge Impulse keyword detection model for a personal home security system using Arduino Nano BLE 33.

### The Model
- Trained on EdgeImpulse to detect the keyword "recludo"
- When the model is started, the Purple LED on the board will blink for 5 seconds
- Say the keyword within the window where the Purple LED is ON during it's blink
    - The 1-1.5 second where the LED is Purple is when the model is recording your voice
    - The Purple LED will blink for 5 seconds, which is the window length you have to say the keyword
- Result:
    - If the keyword is detected successfully within the 5 second window, the Blue LED will blink 3 times
    - If the keyword is NOT detected within the 5 second window, the Red LED will blink 3 times
- Once the appropriate color LED is done blinking, the system will stay on for 3 seconds before going to Sleep
- Pressing the reset button on the board will restart the model again for another 5 seconds

### Running the model
- The final model is present within the "FINAL_Deployment" folder
- Connect your Arduino Board to your machine
- Open the "/FINAL_Deployment/nano_ble33_sense_microphone_V2/nano_ble33_sense_microphone_V2.ino" on Arduino IDE
- On Arduino IDE --> Sketch --> Include Library --> Add .ZIP Library... --> Select the "ei-home-security-system-arduino-1.0.16.zip" within the "FINAL_Deployment" folder
- Once zip has completed setup, upload the "nano_ble33_sense_microphone_V2.ino" to the board
- Once the model has been uploaded to the board, open Serial Monitor and test it is working - refer to the "The Model" section for the functionality

### Flow of sending message to Ubidots using MQTT
- Since the Board does not have a WiFi module, we use our personal machine as the middle-man, i.e. GDA
- Keyword spoken/not spoken in 5s --> Arduino detects keyword/no keyword --> Prints to serial --> GDA reads serial --> GDA sends MQTT message to Ubidots --> Ubidots shows it
- CDA   = Arduino Nano BLE 33
- GDA   = Machine that the Arduino is connected to, through USB
- Cloud = Ubidots

### Testing the Publish to Ubidots
- Open VS Code terminal into "/FINAL_Deployment/nano_ble33_sense_microphone_V2" folder
- Create a .env within this folder with "UBIDOTS_TOKEN" set to your token value
- Connect Arduino through USB
- Create vnenv: python3 -m venv "home-security-ubidots"
- Activate venv: source home-security-ubidots/bin/activate
- Install required libraries within venv:
    - python3 -m pip install pyserial paho-mqtt python-dotenv
- Run "python3 MqttUbidots.py" through the Terminal
- Use the Arduino Model:
    - If the keyword has been detected within 5 seconds of system start (while light is blinking purple), a "success" payload is prepared
    - If the keyword has NOT been detected within 5 seconds of system start (while light is blinking purple), a "failed" payload is prepared
- Once model is done, the terminal will notify that a payload is being sent to Ubidots
- On Ubidots, a new device called "home-security" will be created with the payload
    - Payload will have {"status":"success"} if the keyword was detected within the 5s window
    - Payload will have {"status":"failed"} if the keyword was NOT detected within the 5s window
