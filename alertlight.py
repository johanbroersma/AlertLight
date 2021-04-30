import I2C_LCD_driver
from time import *
from signal import pause
from gpiozero import LED
import webhook_listener

mylcd = I2C_LCD_driver.lcd()
special_char = ["'", '{', '}']
light = LED(20)
light.on()
str_pad = " " * 16
alert = False
args = ""
kwargs = ""

def process_post_request(request, *args, **kwargs):
    global alert
    global message
    message = str(kwargs)
    if "down" in args:
        alert = True
    else:
        alert = False
        
#    print(
#        "Received request:\n"
#        + "Args (url path): {}\n".format(args)
#        + "Keyword Args (url parameters): {}\n".format(kwargs)
#    )    
    
webhooks = webhook_listener.Listener(handlers={"POST": process_post_request})
webhooks.start()    

try:
    print('Ready...')
    while True:
        
        if alert == True:
            light.off()
            for i in special_char:
                message = message.replace(i, '')
                output = [message[i:i+16] for i in range(0, len(message), 16)]
            message = message[:len(message)-2]
            message_line1 = message[:16]
            message_line2 = message[16:]    
            mylcd.lcd_display_string(message_line1, 1)
            message_line2 = str_pad + message_line2
            
            for i in range (0, len(message_line2)):
                lcd_text = message_line2[i:(i+16)]
                mylcd.lcd_display_string(lcd_text,2)
                sleep(0.2)
                mylcd.lcd_display_string(str_pad,2)   
            mylcd.lcd_clear()
            
        if alert == False:
            light.on()
            message_line1 = "No alerts"
            message_line2 = "detected"
            mylcd.lcd_display_string(message_line1, 1)
            mylcd.lcd_display_string(message_line2, 2)

    
except KeyboardInterrupt:
    pass
    
finally:
    mylcd.lcd_clear()