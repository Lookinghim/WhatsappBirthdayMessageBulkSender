import subprocess
import time
import logging
import os
import signal
import psutil
import pandas as pd
from datetime import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from config import CHROME_PROFILE_NAME, EXCEL_FILE_PATH, SCHEDULED_TIME

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppBot:
    def __init__(self):
        self.chrome_process = None
        self.driver = None
        self.user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
        self.profile_directory = CHROME_PROFILE_NAME

    def kill_chrome_processes(self):
        logging.info("Killing any existing Chrome processes...")
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome' in proc.info['name'].lower():
                try:
                    os.kill(proc.info['pid'], signal.SIGTERM)
                    logging.info(f"Killed Chrome process with PID {proc.info['pid']}")
                except ProcessLookupError:
                    pass
        time.sleep(2)  # Wait for processes to terminate

    def start_chrome(self):
        self.kill_chrome_processes()
        
        chrome_path = self.find_chrome_executable()
        if not chrome_path:
            logging.error("Chrome executable not found. Please install Google Chrome and try again.")
            return False

        chrome_command = [
            chrome_path,
            f"--user-data-dir={self.user_data_dir}",
            f"--profile-directory={self.profile_directory}",
            "--remote-debugging-port=9222",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized"
        ]
        
        max_attempts = 3
        for attempt in range(max_attempts):
            logging.info(f"Starting Chrome (Attempt {attempt + 1}/{max_attempts})...")
            try:
                self.chrome_process = subprocess.Popen(chrome_command)
                time.sleep(5)  # Give Chrome some time to start
                
                if self.is_chrome_running():
                    logging.info("Chrome started successfully.")
                    return True
                else:
                    logging.warning("Chrome failed to start. Retrying...")
            except Exception as e:
                logging.error(f"Error starting Chrome: {str(e)}")
        
        logging.error("Failed to start Chrome after multiple attempts.")
        return False

    def find_chrome_executable(self):
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            r"/usr/bin/google-chrome",
            r"/usr/bin/google-chrome-stable"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def is_chrome_running(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome' in proc.info['name'].lower():
                return True
        return False

    def connect_to_chrome(self):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                logging.info(f"Attempting to connect to Chrome (Attempt {attempt + 1}/{max_attempts})...")
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logging.info("Successfully connected to Chrome instance.")
                return True
            except WebDriverException as e:
                logging.error(f"Failed to connect to Chrome: {str(e)}")
                if attempt < max_attempts - 1:
                    logging.info("Retrying in 10 seconds...")
                    time.sleep(10)
                else:
                    logging.error("Failed to connect to Chrome after multiple attempts.")
                    return False

    def open_whatsapp_web(self):
        try:
            logging.info("Attempting to open WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            logging.info("Waiting for WhatsApp Web to load...")
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            logging.info("WhatsApp Web loaded successfully!")
            return True
        except Exception as e:
            logging.error(f"Error opening WhatsApp Web: {str(e)}")
            return False

    def send_message(self, phone_number, message):
        try:
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            logging.info(f"Navigating to: {url}")
            self.driver.get(url)

            logging.info("Waiting for message input box...")
            input_box = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )

            input_box.send_keys(Keys.ENTER)
            
            # Wait for the message to be sent
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="msg-check"]'))
            )
            
            logging.info(f"Message sent to {phone_number}")
            time.sleep(5)  # Wait a bit before sending the next message
            return True
        except Exception as e:
            logging.error(f"Failed to send message to {phone_number}. Error: {str(e)}")
            return False

    def is_birthday_today(self, birthday):
        try:
            birthday_date = datetime.strptime(birthday, '%d/%m')
            today = datetime.now()
            return (birthday_date.month == today.month and birthday_date.day == today.day)
        except ValueError as e:
            logging.error(f"Invalid birthday format: {birthday}. Error: {str(e)}")
            return False

    def send_bulk_messages(self, excel_file):
        try:
            df = pd.read_excel(excel_file)
        
            required_columns = ['phone number (including country code)', 'message', 'birthday']
            if not all(column in df.columns for column in required_columns):
                logging.error(f"Excel file must contain columns: {required_columns}")
                print(f"Please make sure your Excel file has these exact column names: {required_columns}")
                return

            total_records = len(df)
            successful = 0
            failed = 0
            skipped = 0

            print(f"\nChecking {total_records} records for birthdays today...")
            today = datetime.now().strftime('%d/%m')
            print(f"Today's date: {today}")
        
            for index, row in df.iterrows():
                phone_number = str(row['phone number (including country code)'])
                message = str(row['message'])
                birthday = str(row['birthday'])
            
                print(f"\nProcessing record {index + 1} of {total_records}")
                print(f"Contact: {phone_number}, Birthday: {birthday}")
            
                if self.is_birthday_today(birthday):
                    print("✓ It's their birthday today! Sending message...")
                    if self.send_message(phone_number, message):
                        successful += 1
                        print(f"✓ Message sent successfully to {phone_number}")
                    else:
                        failed += 1
                        print(f"✗ Failed to send message to {phone_number}")
                else:
                    skipped += 1
                    print(f"- Skipped {phone_number} (not their birthday)")

            print(f"\nBulk messaging complete:")
            print(f"✓ Successfully sent: {successful}")
            print(f"✗ Failed to send: {failed}")
            print(f"- Skipped (not birthday): {skipped}")
            print(f"Total records processed: {total_records}")
        
            logging.info(f"Bulk messaging complete. Successful: {successful}, Failed: {failed}, Skipped: {skipped}")
        except Exception as e:
            logging.error(f"Error in bulk messaging: {str(e)}")
            print(f"\nError reading Excel file: {str(e)}")
            print("Please make sure:")
            print("1. The Excel file is not open in another program")
            print("2. The column names match exactly: 'phone number (including country code)', 'message', and 'birthday'")
            print("3. Birthday dates are in the format dd/mm (e.g., 25/12)")
            print("4. You have permission to access the file")

    def close(self):
        logging.info("Closing the browser...")
        if self.driver:
            self.driver.quit()
        if self.chrome_process:
            self.chrome_process.terminate()
        self.kill_chrome_processes()

def run_daily_job():
    logging.info("Starting daily WhatsApp automation job...")
    bot = WhatsAppBot()
    try:
        if bot.start_chrome() and bot.connect_to_chrome() and bot.open_whatsapp_web():
            bot.send_bulk_messages(EXCEL_FILE_PATH)
        else:
            logging.error("Failed to initialize WhatsApp automation. Check Chrome and WhatsApp Web.")
    except Exception as e:
        logging.error(f"An error occurred during the daily job: {str(e)}")
    finally:
        bot.close()
        logging.info("Daily job completed.")

def main():
    print("Welcome to WhatsApp Automation!")
    print(f"This script will run automatically every day at {SCHEDULED_TIME}.")
    print("Make sure you keep this script running.")
    
    # Schedule the job to run daily at the specified time
    schedule.every().day.at(SCHEDULED_TIME).do(run_daily_job)
    
    print(f"WhatsApp automation scheduled to run daily at {SCHEDULED_TIME}")
    print(f"Using Excel file: {EXCEL_FILE_PATH}")
    print("Press Ctrl+C to stop the script.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")

if __name__ == "__main__":
    main()

