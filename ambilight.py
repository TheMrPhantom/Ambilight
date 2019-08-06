# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from neopixel import *
 
# LED strip configuration:
LED_COUNT      = 186      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53 

X_STEP=5
Y_STEP=5
RES_X=59*X_STEP
RES_Y=34*Y_STEP
UPPER_BOUND=10
LOWER_BOUND=50
INTERPOLATION_SMOOTHNESS=8
BRIGHT_IMAGE=np.full((170, 295, 3), 255)

def toRGB(g,r,b):
	return Color(r,g,b)
 
 
#Initialize strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (RES_X, RES_Y)
camera.framerate = 90
camera.exposure_mode='fixedfps'
rawCapture = PiRGBArray(camera, size=(RES_X, RES_Y))
 
# allow the camera to warmup
time.sleep(0.1)

print("Started...")
t=millis = int(round(time.time() * 1000))
tavg=0
count=0
image=0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = np.add(np.multiply(np.divide(image,INTERPOLATION_SMOOTHNESS),INTERPOLATION_SMOOTHNESS-1),np.divide(frame.array,INTERPOLATION_SMOOTHNESS))
	#imageTemp=np.subtract(BRIGHT_IMAGE,image)
	#image=np.add(image,np.divide(imageTemp,10))
	for x in range(0,59):
		r=image[UPPER_BOUND][x*X_STEP][0]
                g=image[UPPER_BOUND][x*X_STEP][1]
                b=image[UPPER_BOUND][x*X_STEP][2]
		strip.setPixelColor(33+x, toRGB(r,g,b))
	for x in range(0,59):
		r=image[33*Y_STEP-LOWER_BOUND][x*X_STEP][0]
		g=image[33*Y_STEP-LOWER_BOUND][x*X_STEP][1]
		b=image[33*Y_STEP-LOWER_BOUND][x*X_STEP][2]
		strip.setPixelColor(59*2+33*2-x, toRGB(r,g,b))
	for x in range(0,34):
		r=image[x*Y_STEP][0][0]
		g=image[x*Y_STEP][0][1]
		b=image[x*Y_STEP][0][2]
		strip.setPixelColor(34-x, toRGB(r,g,b))
	for x in range(0,34):
		r=image[x*Y_STEP][58*X_STEP][0]
		g=image[x*Y_STEP][58*X_STEP][1]
		b=image[x*Y_STEP][58*X_STEP][2]
		strip.setPixelColor(33+59+x, toRGB(r,g,b))

	strip.show()
	temp= int(round(time.time() * 1000))
	print(temp-t)
	tavg+=temp-t
	count+=1
	if count>20:
		print("\t"+str(tavg/count))
		count=0
		tavg=0
	t=temp
#	cv2.imwrite("test.jpg",frame.array)
#	exit()
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)


