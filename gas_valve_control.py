import os
import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import logging

# Set up logging
logging.basicConfig(filename='gas_valve_control.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_gpio():
    """Set up GPIO pins for gas sensor and relay."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config['gas_sensor_pin'], GPIO.IN)
    GPIO.setup(config['relay_pin'], GPIO.OUT)

def close_gas_valve():
    """Close the gas valve and log the action."""
    GPIO.output(config['relay_pin'], GPIO.HIGH)
    logging.info("Gas valve closed")

def send_notification():
    """Send email notification if configured."""
    if all(config.get(key) for key in ['email_sender', 'email_password', 'email_receiver']):
        subject = 'Gas Leak Alert'
        body = 'Gas has been detected. The gas valve has been closed.'

        message = MIMEMultipart()
        message['From'] = config['email_sender']
        message['To'] = config['email_receiver']
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(config['email_server'], config['email_port']) as server:
                server.starttls()
                server.login(config['email_sender'], config['email_password'])
                server.sendmail(config['email_sender'], config['email_receiver'], message.as_string())

            logging.info("Email notification sent")
        except Exception as e:
            logging.error(f"Error sending email notification: {str(e)}")

def main_loop():
    """Main loop for gas sensor monitoring."""
    try:
        while True:
            gas_value = GPIO.input(config['gas_sensor_pin'])
            threshold = config['gas_threshold']

            if gas_value > threshold:
                close_gas_valve()
                logging.warning("Gas detected! Closing the gas valve.")

                if gas_value > config['notification_threshold']:
                    send_notification()
                    logging.info("Gas concentration exceeds notification threshold.")
            else:
                logging.info("Gas levels normal.")

            time.sleep(config['sleep_duration'])

    except KeyboardInterrupt:
        logging.info("Keyboard interrupt. Cleaning up GPIO.")
        GPIO.cleanup()

if __name__ == "__main__":
    # Load configuration from a YAML file
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Set up logging to both console and file
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_handler)

    # Start the main process
    setup_gpio()
    main_loop()
