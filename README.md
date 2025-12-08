# home-security-system
Edge Impulse keyword detection model for a personal home security system using Arduino Nano BLE 33.

### The Model
- Trained on EdgeImpulse to detect the keyword "recludo"
- When the model is running, the Red LED on the board will blink
- Say the keyword within the window where the Red LED is ON
- If the keyword is detected successfully, the Blue LED will blink 3 times
- Once the Blue LED is done blinking, the system will stay on for 3 seconds before going to Sleep
- Pressing the reset button on the board will restart the model again

### Running the model
- The final model is present within the "FINAL_Deployment" folder
- Connect your Arduino Board to your machine
- Open the "/FINAL_Deployment/nano_ble33_sense_microphone_V2/nano_ble33_sense_microphone_V2.ino" on Arduino IDE
- On Arduino IDE --> Sketch --> Include Library --> Add .ZIP Library... --> Select the "ei-home-security-system-arduino-1.0.16.zip" within the "FINAL_Deployment" folder
- Once zip has completed setup, Upload the "nano_ble33_sense_microphone_V2.ino" to the board
- Once the model has been uploaded to the board, open Serial Monitor and test it is working - refer to the "The Model" section for the functionality

### Flow of sending message to Ubidots using MQTT
- Since the Board does not have a WiFi module, we use our personal machine as the middleman, i.e. GDA
- Keyword spoken --> Arduino detects keyword --> Prints to serial --> PC/Mac reads serial --> PC/Mac sends MQTT message to Ubidots --> Ubidots shows it
- CDA   = Arduino Nano BLE 33
- GDA   = Machine that the Arduino is connected to, through USB
- Cloud = Ubidots

### Testing the Publish to Ubidots
- Open VS Code terminal into "/FINAL_Deployment/nano_ble33_sense_microphone_V2" folder
- Create a .env within this folder with "UBIDOTS_TOKEN" set to your token value
- Connect Arduino through USB
- Activate venv: "source home-security-ubidots/bin/activate"
- Run "python3 MqttUbidots.py" through the Terminal
- Say the keyword for the Arduino to detect
- Once the keyword has been detected, the terminal will notify that a payload is being sent to Ubidots
- On Ubidots, a new device called "home-security" will be created with the payload
