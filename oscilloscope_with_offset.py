import machine
import ssd1306
import time
from machine import ADC, Pin, I2C


# Display size
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64


# Basic Osilliscope using Raspberry Pi Pico and
# SSD1306 128x64 oled 
# Includes DC offset circuit 

# Configure I2C communication with specific pins
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) 

# Initialize the display
oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)

# Initialize the microphone analog input ADC on pin 28
mic_pin = 28
mic = ADC(Pin(mic_pin))


# Generate grid coordinates
coordinate_list = []
for x_coord in range(8,128,8):  # X range from 10 to 19
    for y_coord in range(8,64,8):  # Y range from 10 to 19
        coordinate_list.append((x_coord, y_coord)) # Store coordinates as tuples
        
  
# Define function to display grid and surrounding rectangle 
def plot_coordinates(coordinates, oled):
    oled.fill(0) # Clear the display buffer (fill with black)

#     Plot grid
    for coord in coordinates:
        x, y = coord
        oled.pixel(x, y, 1) # Set the pixel to white

#     Plot boarder 
    oled.rect(0,0,128,64,1)
    
    
    
def plot_waveform():
    oled.fill(0) # Clear the display buffer
    plot_coordinates(coordinate_list, oled)
    # Store waveform points
    points = []
    # Adjust number of samples to match display width for simple mapping
    num_samples = DISPLAY_WIDTH

    for i in range(num_samples):
        # Read the raw microphone value (0 to 65535 on Pico, or 0 to 4095 on ESP32)
        raw_value = mic.read_u16()
#       Calculate voltage from raw_value using potential divider (1.65V)
#       and scale up for display
        voltage = (1.65-(raw_value*3.3/65535))*250
        y = (DISPLAY_HEIGHT-32 + voltage)
        points.append(int(y))
    

# Draw the waveform lines
    for i in range(1, num_samples):
# Draw a line from the previous point (x-1) to the current point (x)
        oled.line(i - 1, points[i - 1], i, points[i], 1) #
        


#  Main loop
while True:   
    plot_waveform()
    # Control update speed
    time.sleep(0.05)
    oled.show()
