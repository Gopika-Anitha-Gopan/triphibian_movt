# Motor.py
Here, we are using Hardware Pulse Width Modulation for the control of speeds of the motors. So in the below piece of the code, I am importing the module called 'os' which connects my code to the terminal commands.
So when i do `os.system("sudo pigpiod")` it is a command written to the terminal such that the module "pigpiod" will be loaded.
The module 'time' is imported to wait in between the execution of different functionalities of the code.
`import RPi.GPIO as GPIO` is used to integrate the pins(pin numbers) of the Raspberry Pi board
```Python
# BLDC Motor control with hardware pwm

import os
import time
os.system("sudo pigpiod")
time.sleep(1)
import RPi.GPIO as GPIO
import pigpio
pi = pigpio.pi();

```
Here we are creating a class called BLDC, which has the following functions 
   `__init__(self, name, PWM_pin, reverse_pin)`, which is a constructor that takes in the the pwm pin number, name of the motor and the reverse pin number of the ESC
       it sets the pulsewidth of the pwm to zero
    ```Python
         GPIO.setmode(GPIO.BCM)
         GPIO.setup(self.reverse_pin, GPIO.OUT)
     ```
       the above piece of code sets up the gpio pins  and sets the numbering scheme to Broadcom GPIO numbers (BCM)
```Python
     def move(self):
        #pi.set_servo_pulsewidth(self.pwmpin, self.pulse_width)
        print(f"in move {self.pulse_width}")
        print("inside move function")
```

     
   * in the function `move(self)`, we just set the pulse width of the motors.
   
```Python
   def increase(self):
        if self.pulse_width == 0:
            #GPIO.output(self.reverse_pin, False)
            print("reversed-false and increase")
        self.pulse_width += 10
        if self.pulse_width > 2000:
            self.pulse_width = 2000

        self.move()
```
we need to make the reverse pin of the ESC false for the motors to move forward. 
we try to increase the pulsewidth of the pwm pin (which is actually the speed of the motors) by 10 .The     maximum pulse width can be 2000, when we reach there(the maximum speed), the speed remains constant there 

```Python
def decrease(self):
        if self.pulse_width == 0:
            #GPIO.output(self.reverse_pin, False)
            print("reversed-false and increase")
        if self.pulse_width < 1000:
            self.pulse_width = 1000
        self.move()
        self.pulse_width -= 10

        print("inside slow")

```
slows down the motors by reducing the PWM

```Python
       def reverse_inc(self):
        if self.pulse_width == 0:
            #GPIO.output(self.reverse_pin, True)
            self.pulse_width += 1 # such that when increase() is called, the reverse pin doesnt set to false
            print("reversed-true and increase")
        self.increase()
```
we can only reverse the direction of the motor when the speed(pulse width of pwm) becomes zero. it increases pulse_width in reverse direction

```Python
   def reverse_dec(self):
        if self.pulse_width == 0:
            #GPIO.output(self.reverse_pin, True)
            self.pulse_width += 1
            print("reversed-true and decrease")
        self.decrease()
```
it decreses pulse_width in reverse direction

```Python 
      def pause(self):
         elf.pulse_width = 0
         pi.set_servo_pulsewidth(self.pwmpin, self.pulse_width)
```
temporarily stops the motors by making pulsewidth zero

```Python
    def stop(self):
      pi.set_servo_pulsewidth(self.pwmpin, 0)
      GPIO.cleanup()
 ```
does an overall clean up and stops all the prev running functions and stops  all the motors 
___   
    
# Land_Motion.py
```Python
from motor_hardware import BLDC
from pynput.keyboard import Listener
import time

```
We are initially importing the BLDC class we created in motor_hardware.py
For the keyboard contol of the bot, we are using the 'pynput' module of pyhton which seems to be comfortable than the 'keyboard' module of python
And as usual, the 'time' module for sleep

```Python
# Note: GPIO Pin numbers are random and should be BCM numbering.
left_motor = BLDC('left', 2, 3)
right_motor = BLDC('right', 5,6)

```
Defining the left and right motors by mentioning their GPIO pin numbers and their PWM pins
and make their speeds zero initially
```Python
def forward_inc():
    left_motor.increase()
    right_motor.increase()
    time.sleep(0.05)  # Wait for signal to reach motor

```
Forward motion is deined when both the motors spin in the same direction and move with the same speed. We need some time to pause after the functioned is called for the signal to reach the motor. the speed of motors is increased too.

```Python
def forward_dec():
    left_motor.decrease()
    right_motor.decrease()
    time.sleep(0.05)
```
both the motors slow down while the bot still moves in the forward direction

```Python
def backward_inc():
    left_motor.reverse_inc()
    right_motor.reverse_inc()
    time.sleep(0.05)
```
The bot moves Backward when both the motors spin in the opposite direction and with same  increasing speed

```Python
def backward_dec():
    left_motor.reverse_dec()
    right_motor.reverse_dec()
    time.sleep(0.05)
```
The bot moves Backward when both the motors spin in the opposite direction and with same decreasing speed

```Python
def left_inc():
    left_motor.reverse_inc()
    right_motor.increase()
    time.sleep(0.05)
```
makes the bot move left with increasing speed
```Python
def left_dec():
    left_motor.reverse_dec()
    right_motor.decrease()
    time.sleep(0.05)
```
makes the bot move left with decreasing speed

```Python
def right_inc():
    left_motor.increase()
    right_motor.reverse_inc()
    time.sleep(0.05)
```
makes the bot move right with increasing speed

```Python
def right_dec():
    left_motor.decrease()
    right_motor.reverse_dec()
    time.sleep(0.05)
```
makes the bot move right with decreasing speed

* To understand the left and right motionsof the bot, we need to know about the concept called 'differential drive'  which means the  Velocity difference between two motors drive the robot in any required path and direction. 
* For the robot to move left :
  spinnig the right wheel forward and left wheel reverse in the same speed makes the robot spin around its vertical axis in the left deirection(anti clock as seen from above). Even making a 360 degree turn is possible in this motion
* For the robot to move right:
  spinning the right wheel backward and left wheel forward gives us the required motion
```Python
def stop():
    left_motor.stop()
    right_motor.stop()
```
this function completely stops the robot and does a GPIO cleanup
```Python
def pause():
    left_motor.pause()
    right_motor.pause()
    time.sleep(0.05)

```
it just pauses(makes pulse width zero) or halts the motion of both the motors

```Python
def on_release(key):
    if key != key.esc :
        slow()
with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()
```
In the above piece of code we adding Listener from the python modue 'pynput' which listens or senses the key we have pressed.
on_press(key) and on_release(key) are the functions performed when the keys are pressed and released as their names suggest.
* Our program does the following:
  * Up arrow - Forward
  * Down arrow - Backward
  * Left arrow - Left
  * Right arrow - Right
  * Esc - Stop
  * When a key among the arrows is pressed, the robot moves to whatever the motion key is pressed and the longer you press, the faster it moves untill the max speed is reached and from there it is constant speed. Once you release the key, the speeds becomes zero.
  * When you press Esc button, the whole program comes to a halt.
___

# BLDC_Test.py
RPIO is an advanced GPIO module for the Raspberry Pi. It contains a lot of functions defined in it, which can be used to control motors, servos, etc using Raspberry Pi.
---

This is a piece of code to test the BLDC and configure it for use. 
First of all, we are importing the required libraries.
``` python
from RPIO import PWM
import time
```

Next, we are defining the "main" function. It uses the hardware PWM and intializes the PWM. It then gives us a choice to either calibrate or run the motor. When running 
the motor for the first time, it should be calibrated for efficient use. 

To calibrate we first set the PWM to max and then connect battery. We  wait until we hear a confirmation. 

After that, we set the PWM to min and again wait to hear confirmation.

When these 2 steps are done, the motor is Calibrated.

This is the code running for calibration:
``` python
def calibrate():
```
Once calibrated, the motor is ready to run.

The code executed while running is:
``` python
def test_run():
```

This code is just a test run. It increases the pulse width to max gradually and then decreases it to 0.( this is done in the 2 while loop blocks)

The set_servo() function sets is used to change the pulsewidth of the PWM. During callibration, we set the minumum and maximum values that servo can take. This is done by the 2 lines of code,
``` python
esc.set_servo(motor_pin, min_value)
```
``` python
esc.set_servo(motor_pin, max_value)
```
