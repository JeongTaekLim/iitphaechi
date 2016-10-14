import RPi.GPIO as GPIO
strLeft = "left"
strRight = "right"
strTime = "time"
leftPinList=[33, 35, 37]
rightPinList=[36, 38, 40]
pinList = [rightPinList,leftPinList]
forwardOutput=[GPIO.HIGH, GPIO.LOW, GPIO.HIGH]
parkOutput=[GPIO.LOW, GPIO.LOW, GPIO.LOW]
reverseOutput=[GPIO.HIGH, GPIO.HIGH, GPIO.LOW]

