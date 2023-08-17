# raspTrading
![logo](raspTrading-logo.png)

## What is the history behind this project?
I created this project to explore trading and the risk involved, based on the idea of opening and closing orders based solely on price. The original idea was inspired by the [OverVolt](https://www.youtube.com/watch?v=4ZXVNi9VeWE&pp=ygUNb3ZlcnZvbHQgY2N4dA%3D%3D) video; however, I adjusted my target audience and added scalability to make it more general. 

## Is it a necessary tool?
In my view, it is not necessary to use this tool alone when it comes to trading, as one needs to use comprehensive approaches accompanied by meticulous analysis, especially in the volatile cryptocurrency market.

## How does one install this tool and what are the requirements?
To start with, you'll need a Raspberry Pi, regardless of the version you have. Secondly, you'll need a lever and a 16x2 LCD screen (or another type of screen, but the code is optimized for 16x2 LCD). Additionally, you may want to add a button to enable simplified actions (which needs to be implemented in the code).

## What are the requirements for starting the code without any errors?
To start the code, you just need to run the requirements file. The [CCXT](https://github.com/ccxt/ccxt) and RPi.GPIO libraries need to be installed to manage the Raspberry board. However, the latter may not be present in the operating system you are using on the Raspberry.

## Raspberry's GPIO board
The Raspberry's GPIO board operates in two modes; we use the "board" mode and connect the four digital pins (33 to 37) and the GND '39' for this purpose.
[GPIO Board](https://openclipart.org/image/800px/280972)
