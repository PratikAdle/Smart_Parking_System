# Smart Parking System
# Made By : 1) Arnav Khandekar (BT17ECE028)
#           2) Dhanraj Mahurkar (BT17ECE033)
#           3) Pratik Adle (BT17ECE034)
#           2) Ashwin Patil (BT17ECE036)


# Importing Required Libraries
import RPi.GPIO as GPIO
import time
import sqlite3
from ftplib import FTP
        

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Setting GPIO Pins
GPIO_TRIGGER1 = 4
GPIO_ECHO1 = 17
GPIO_TRIGGER2 = 27
GPIO_ECHO2 = 22
GPIO_TRIGGER3 =10
GPIO_ECHO3 =9


GPIO.setwarnings(False)

# Setting GPIO as input or output (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)

# Function for calculating distance from Car using Ultrasonic Sensor
def distance(GPIO_TRIGGER,GPIO_ECHO):
    # Setting Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiplying with the speed of sound in air (34300 cm/s)
    # and dividing by 2, because it travels towards obstacle and back to source
    distance = (TimeElapsed * 34300) / 2

    return distance


## Function for Displaying on LED Display
import RPi.GPIO as GPIO
import wiringpi as wiringpi  
import time

wiringpi.wiringPiSetupGpio()
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

wiringpi.pinMode(13,2)
wiringpi.pwmSetMode(0)
wiringpi.pwmSetClock(384)
wiringpi.pwmSetRange(1000)
wiringpi.pwmWrite(13,120)

GPIO.setup(14, GPIO.OUT) # LED a pin set as output
GPIO.setup(15, GPIO.OUT) # LED b pin set as output
GPIO.setup(18, GPIO.OUT) # LED c pin set as output
GPIO.setup(23, GPIO.OUT) # LED d pin set as output
GPIO.setup(24, GPIO.OUT) # LED e pin set as output
GPIO.setup(25, GPIO.OUT) # LED f pin set as output
GPIO.setup(8, GPIO.OUT)  # LED g pin set as output

# Display numbers on LED 7 Segment Display
def display_on_led(int):
    if int==0:
        num0()
        
    elif int==1:
        num1()
        
    elif int==2:
        num2()
        N=2
    elif int==3:
        num3()
    return;

# Display 0 on LED 7 Segment Display
def num0():
  GPIO.output(14, GPIO.HIGH) # LED a pin 
  GPIO.output(15, GPIO.HIGH) # LED b pin 
  GPIO.output(18, GPIO.HIGH) # LED c pin 
  GPIO.output(23, GPIO.HIGH) # LED d pin 
  GPIO.output(24, GPIO.HIGH) # LED e pin 
  GPIO.output(25, GPIO.HIGH) # LED f pin 
  GPIO.output(8, GPIO.LOW)   # LED g pin
  
# Display 1 on LED 7 Segment Display  
def num1():
  GPIO.output(14, GPIO.LOW) # LED a pin 
  GPIO.output(15, GPIO.HIGH) # LED b pin    
  GPIO.output(18, GPIO.HIGH) # LED c pin 
  GPIO.output(23, GPIO.LOW) # LED d pin 
  GPIO.output(24, GPIO.LOW) # LED e pin 
  GPIO.output(25, GPIO.LOW) # LED f pin 
  GPIO.output(8, GPIO.LOW)  # LED g pin
  
# Display 2 on LED 7 Segment Display  
def num2():
  GPIO.output(14, GPIO.HIGH) # LED a pin 
  GPIO.output(15, GPIO.HIGH) # LED b pin 
  GPIO.output(18, GPIO.LOW) # LED c pin 
  GPIO.output(23, GPIO.HIGH) # LED d pin 
  GPIO.output(24, GPIO.HIGH) # LED e pin 
  GPIO.output(25, GPIO.LOW) # LED f pin 
  GPIO.output(8, GPIO.HIGH)  # LED g pin

# Display 3 on LED 7 Segment Display
def num3():
  GPIO.output(14, GPIO.HIGH) # LED a pin 
  GPIO.output(15, GPIO.HIGH) # LED b pin 
  GPIO.output(18, GPIO.HIGH) # LED c pin 
  GPIO.output(23, GPIO.HIGH) # LED d pin 
  GPIO.output(24, GPIO.LOW) # LED e pin 
  GPIO.output(25, GPIO.LOW) # LED f pin 
  GPIO.output(8, GPIO.HIGH)  # LED g pin
  
  



if __name__ == '__main__':
    try:
        while True:
            #dist = distance()
            A = '1'
            B = '0'
            C = '1'
            Count=-1
            dist1 = distance(GPIO_TRIGGER1,GPIO_ECHO1)
            
            state1 = 0
        
            # If distance between sensor 1 and car is less than 10 cm
            # then parking space A is filled
            if dist1 < 10:
                print ("A : In use")
                A="A is Filled"
                
            else :
                print ("A : Empty")
                A="A is Vacant"
            
            
            # If distance between sensor 2 and car is less than 10 cm
            # then parking space B is filled
            dist2 = distance(GPIO_TRIGGER2,GPIO_ECHO2)
            if dist2 < 10:
                print ("B : In use")
                B="B is Filled"
            else :
                print ("B : Empty")
                B="B is Vacant"
            
            
            # If distance between sensor 1 and car is less than 10 cm
            # then parking space A is filled
            dist3 = distance(GPIO_TRIGGER3,GPIO_ECHO3)  
            if dist3 < 10:
                print ("C : In use")
                C="C is Filled"
            else :
                print ("C : Empty")
                C="C is Vacant" 



   
            # All 3 spaces vacant
            if ((A != "A is Filled" and B != "B is Filled") and C != "C is Filled" ) :
                wiringpi.pwmWrite(13,75)
                display_on_led(3)
                Count = 3

            # 2 spaces vacant
            if (((A == "A is Filled" and B != "B is Filled") and C != "C is Filled") or ((A != "A is Filled" and B == "B is Filled") and C != "C is Filled") or ((A != "A is Filled" and B != "B is Filled") and C == "C is Filled") ):
                wiringpi.pwmWrite(13,75)
                display_on_led(2)
                Count = 2

            # 1 space vacant
            if (((A == "A is Filled" and B == "B is Filled") and C != "C is Filled") or ((A == "A is Filled" and B != "B is Filled") and C == "C is Filled") or ((A != "A is Filled" and B == "B is Filled") and C == "C is Filled") ):
                wiringpi.pwmWrite(13,75)
                display_on_led(1)
                Count = 1

            # no vacant space
            if ((A == "A is Filled" and B == "B is Filled") and C == "C is Filled" ) :
                wiringpi.pwmWrite(13,75)
                display_on_led(0)
                Count = 0

            print("--------------------------------------------------------------------------")
            time.sleep(2)

                      
        #Stop checking status by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

# Now send the status of availabilty of Parking space to the database

    
# Send data to database using FTP
import webbrowser

f = open('index.html','w')

message = """<!DOCTYPE html> 
<html> 
  
<head> 
    <style> 
        table, th, td{ 
            border: 3px solid black;
            border-collapse:collapse;
            padding:5px;
            margin-left:5px
            background-color:white;
            color:black;
            
            
        }
        body {
  font-family: Arial, Helvetica, sans-serif;
  background-color: black;
}

* {
  box-sizing: border-box;
}

/* Add padding to containers */
.container {
  padding: 16px;
  background-color: white;
}

/* Full-width input fields */
input[type=text], input[type=password] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}

input[type=text]:focus, input[type=password]:focus {
  background-color: #ddd;
  outline: none;
}

/* Overwrite default styles of hr */
hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}

/* Set a style for the submit button */
.registerbtn {
  background-color: red;
  color: white;
  padding: 16px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}

.registerbtn:hover {
  opacity: 1;
}

/* Add a blue text color to links */
a {
  color: dodgerblue;
}

/* Set a grey background color and center the text of the "sign in" section */
.signin {
  background-color: #f1f1f1;
  text-align: center;
}
    </style> 
</head> 
  
<body> 
    
    <form action="#">
  <div class="container">
    <table style="width:100%;margin-top:50px;"> 
        <tr> 
            <th>PARKING SPACE A</th> 
            <th>PARKING SPACE B</th> 
            <th>PARKING SPACE C</th>
            <th>No of parking spaces available</th> 
        </tr> 
        <tr> 
            <td>"""+A+"""</td> 
            <td>"""+B+"""</td> 
            <td>"""+C+ """</td>
            <td>"""+str(Count)+ """</td> 
        </tr> 
        
    </table>
    <h1>Book your slot</h1>
    <p>Please fill in this form to book a slot.</p>
    <hr>
    <label for="name"><b>Name</b></label>
    <input type="text" placeholder="Enter your name" name="name" required>

    <label for="email"><b>Email</b></label>
    <input type="text" placeholder="Enter Email" name="email" required>

    <label for="psw"><b>PARKING SPACE TO BE BOOKED</b></label>
    <input type="text" placeholder="Enter PARKING SPACE TO BE BOOKED" name="psw" required>

    <label for="psw-repeat"><b>Time</b></label>
    <input type="text" placeholder="enter time slot" name="psw-repeat" required>
    <hr>
    <p>By booking a slot you agree to our <a href="#">Terms & Privacy</a>.</p>

    <button type="submit" class="registerbtn">BOOK NOW</button>
  </div>
  
  <div class="container signin">
    <p>Already booked? <a href="#">Sign in</a>.</p>
  </div>
</form>

</body></html> """



f.write(message)

        
f.close()


#Change path to reflect file location

ftp=FTP('ftpupload.net')
ftp.login('epiz_24608721','XskwtNCPA8',21)
ftp.cwd('/htdocs')
ftp.storbinary('STOR index.html', open('index.html', 'rb'),21)

ftp.quit()



