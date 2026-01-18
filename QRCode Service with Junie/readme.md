##      QRCode Service with Junie

This project was built with the AI assistant JetBrain Junie as a plugin to the Jetbrain IntelliJ IDE.


### Summary

The app generated provides an API to create QR codes with the parameters you add. 
You can also save the QR code on your local disk.

the AI assistant has created the source code and the gradle environment.


### To test the project
* download the project on your local drive, including src/,  gradle/, and the gradle files

* The project has been developed using Kotlin, so you need Java 1.8 installed to run the project

* you can start the API by typing: `gradlew run` in your terminal/CMD

* Once the API is running you can access at `http://localhost:12345/health` to check that everything is working
  you should see a message saying `service is running`

* to create a QR code:  
  `http://localhost:12345/qr?size=300&type=jpeg&contents=HelloWorld`

  to create and save a QR code:  
  `http://localhost:12345/qr/save?size=300&type=jpeg&contents=banana`
