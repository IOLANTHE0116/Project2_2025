import smtplib
import time
import schedule
from email.message import EmailMessage
from gpiozero import Button
from datetime import datetime

# CONFIGURATION - UPDATE THESE VALUES
SMTP_SERVER = "smtp.qq.com"       # QQ Mail SMTP server
SMTP_PORT = 587                   # QQ Mail SMTP port
FROM_EMAIL = "3599127710@qq.com"  # Sender email
FROM_PASSWORD = "ViatinUriel"     # Sender email app password
TO_EMAIL = "2948174837@qq.com"    # Recipient email
SENSOR_PIN = 17                   # GPIO pin connected to sensor's digital output

# SENSOR SETUP
sensor = Button(SENSOR_PIN, pull_up=True, bounce_time=0.2)
water_needed = not sensor.is_pressed  # Initial status

# SENSOR CALLBACK FUNCTIONS
def on_water_detected():
    """Triggered when moisture detected (sensor pressed)"""
    global water_needed
    water_needed = False
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Moisture detected: Plant is hydrated")

def on_no_water():
    """Triggered when dry soil detected (sensor released)"""
    global water_needed
    water_needed = True
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Dry soil detected: Plant needs water")

# Attach callbacks to sensor events
sensor.when_pressed = on_water_detected
sensor.when_released = on_no_water

# EMAIL FUNCTION
def send_plant_status():
    """Sends email with current plant status"""
    try:
        # Create message object
        msg = EmailMessage()
        
        # Get current time
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        date_str = current_time.strftime('%Y-%m-%d')  # Date only for body
        
        # Determine status based on sensor reading
        if water_needed:
            status = "Plant needs watering！！"
        else:
            status = "Plant does Not need watering."
        
        # Set email content as per your request
        body = f"""Plant Status Report
Timestamp：{date_str} Current Condition：{status}"""
        
        msg.set_content(body)
        
        # Set email headers with required format
        time_str = current_time.strftime('%H:%M')
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = f"【Plant Dally】 {status} {time_str}"
        
        # Send email via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.send_message(msg)
            print(f"[{timestamp}] Status email sent: {status}")
            
        return True
    
    except Exception as e:
        print(f"[{timestamp}] Email failed: {str(e)}")
        return False

# SCHEDULED MONITORING
def setup_schedule():
    """Configure daily email schedule at 7:00, 16:00, 19:00"""
    schedule_times = ["07:00", "16:00", "19:00"]  # Your requested times
    for t in schedule_times:
        schedule.every().day.at(t).do(send_plant_status)
        print(f"Scheduled status check at {t} daily")

# MAIN EXECUTION
if __name__ == "__main__":
    print("\n===== Plant Moisture Monitoring System =====")
    print(f"Notification Recipient: {TO_EMAIL}")
    print(f"Using sensor on GPIO {SENSOR_PIN}")
    print("Scheduled times: 07:00, 16:00, 19:00")
    
    setup_schedule()
    print("\nSystem running. Press Ctrl+C to exit.\n")
    
    # Initial status check
    current_status = "NEEDS WATER" if water_needed else "OK"
    print(f"Initial Status: {current_status}")
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nSystem stopped by user")
