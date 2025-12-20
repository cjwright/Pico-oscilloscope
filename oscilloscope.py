import machine
import ssd1306
import time
from machine import ADC, Pin, I2C

#import gfx


# --- Configuration ---
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64


# Configure I2C communication (adjust pins based on your board)
# Example for Raspberry Pi Pico
# i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# Example for ESP32
# i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) # Update with your specific pins

# Initialize the display
oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)

# graphics = gfx.GFX(DISPLAY_WIDTH, DISPLAY_HEIGHT, oled.pixel)


# Initialize the microphone analog input (adjust pin as necessary, e.g., GP26 for Pico ADC0)
mic_pin = 28
mic = ADC(Pin(mic_pin))
 
 
 
 
# Define grid coordinates

coordinate_list = []
for x_coord in range(8,128,8):  # X range from 10 to 19
    for y_coord in range(8,64,8):  # Y range from 10 to 19
        coordinate_list.append((x_coord, y_coord)) # Store coordinates as tuples
        
        
def plot_coordinates(coordinates, display_obj):
    display_obj.fill(0) # Clear the display buffer (fill with black)
    
    for coord in coordinates:
        x, y = coord
        # Use the pixel() method: display.pixel(x, y, color)
        # Color can be 0 (off/black) or 1 (on/white)
        if 0 <= x < DISPLAY_WIDTH and 0 <= y < DISPLAY_HEIGHT: # Basic boundary check
            display_obj.pixel(x, y, 1) # Set the pixel to white
    oled.rect(0,0,128,64,1)        
#     display_obj.show() # Update the physical display with the buffer's contents

# Run the plot function
#print(f"Plotting {len(coordinate_list)} pixels...")
plot_coordinates(coordinate_list, oled)


 
# --- Waveform Plotting Function ---
def plot_waveform():
    oled.fill(0) # Clear the display buffer
    plot_coordinates(coordinate_list, oled)
#     oled.rect(0,0,128,64,1)
    # Store waveform points
    points = []
    # Adjust number of samples to match display width for simple mapping
    num_samples = DISPLAY_WIDTH

    for i in range(num_samples):
        # Read the raw microphone value (0 to 65535 on Pico, or 0 to 4095 on ESP32)
        raw_value = mic.read_u16()
#         print(raw_value)
        # Map the raw value to a Y-coordinate on the screen (0 to 63)
        y = int(raw_value / 3535 * DISPLAY_HEIGHT)
        # Invert the Y value as screen coordinates start from the top left
        y = DISPLAY_HEIGHT - 10 - y
#         print(raw_value)
        points.append(y)
        # A small delay might be needed depending on the sample rate desired
        time.sleep_us(20) 

    # Draw the waveform lines
    for i in range(1, num_samples):
        # Draw a line from the previous point (x-1) to the current point (x)
        oled.line(i - 1, points[i - 1], i, points[i], 1) #
#         time.sleep(0.5)
    # Update the physical display
    oled.show()








# --- Main Loop ---
while True:
    plot_waveform()
    # Control update speed
    time.sleep(0.05)
    
