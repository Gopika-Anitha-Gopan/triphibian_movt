# Motor Control
This is a file that explains in brief, the python codes given in the folder [Motor_Control](https://github.com/Gopika-Anitha-Gopan/Triphy/tree/onging/Motor_Control).

## Table of Contents

* [BLDC Motor control with software PWM](#motor)
* [Code for moving the Bot](#move)

---

<a name="motor"></a>
### BLDC Motor control with software PWM

The [motor.py](https://github.com/Gopika-Anitha-Gopan/Triphy/blob/onging/Motor_Control/motor.py) is the python code which lets us control the BLDC motors with software PWM. PWM is a square wave signal that repeats itself at a certain frequency. Each PWM cycle is called a period, and the percentage of time the PWM signal is on during a given period determines the duty cycle. With PWM, we’re able to adjust a constant DC voltage to different voltage levels. This helps us control a motor at varying speeds.  
Using 'import RPi.GPIO as GPIO' we import the RPi.GPIO library and gives it the name GPIO.Then a function is __init__is defined.
####  __init__function :
Code | Explanation
-----|-------------
'GPIO.setmode(GPIO.BCM)' | with this we indicate whether we want to address the GPIOs via their GPIO number.
'GPIO.setmode(GPIO.BCM)' | setting up output ports of raspberry pi using RPi.GPIO.
'p = GPIO.PWM(self.pwmpin, 50)' | self.pwmpin – pin number/GPIO number ,50Hz' – frequency of the PWM
'p.start(0)'| Starts the PWM (0-Starting duty cycle)


####  move(self) function :
Code | Explanation
-----|------------
'p.ChangeDutyCycle(self.duty_cycle)'| Changes the duty cycle of the PWM (self.duty_cycle – new duty cycle)


####  forward(self) function : 
As long as the key corresponding to the forward movement is pressed this function is called which in turn calls move().


#### reverse(self) function
When this function is called it reverses direction and calls move() like forward().
'GPIO.output(self.reverse_pin, True)' - Can reverse only if motor is stoped, i.e., pwm = 0. Safety feature of ESC


#### slow(self) function :
Slows down the Bot


#### stop(self) function :
Helps in stopping the Bot
Code | Explanation
-----|-------------
 'p.stop()'| Stops the PWM
 'GPIO.cleanup()'| Cleans the GPIO
 
---

<a name="move"></a>
### Code for moving the Bot

The [move.py](https://github.com/Gopika-Anitha-Gopan/Triphy/blob/onging/Motor_Control/move.py) actually helps us in moving the Bot. Initially we import 'class BLDC' from motor.py and also curses. curses is a terminal control library for Unix-like systems, enabling the construction of text user interface (TUI) applications.  It is a library of functions that manage an application's display on character-cell terminals 

```python
'left_motor = BLDC('left', 2, 3)' 
```
The left motor is "connected" to the RaspberryPi which gives the PWM signals. Similarly the Right motor is also initialised.

#### main(window) function :
Firstly, we create a Dictionary by the name 'actions'.
The function tries to get input from the arrow keys via curses. 
After this block of code we see a while loop which gets input from the user.


#### Inside the while loop :
Here we wait for 1/10ths of a second for user to input ,and if the user fails to provide an input, -1 is returned. The if statement after it checks if the returned value is -1 or no.

```python
  while next_key == key:
```

The above code snippet keeps calling the action dictionary as long as the key is pressed. When the key is stopped pressing the motor is slowed down.(stops it actually). The next few blocks of code moves it in the direction corresponding to the key pressed.

```python
def forward():
```

The above code calls the function forward() in motor.py. Similarly reverse(), right(), left(), stop() are called accordingly. 
