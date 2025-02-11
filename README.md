# Whatsapp_Automation_Send_Message

This project provides a Python script to automate sending messages on WhatsApp Web using your existing Chrome browser session.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Important Notes](#important-notes)
6. [Troubleshooting](#troubleshooting)
7. [Disclaimer](#disclaimer)

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. Clone this repository:
```plaintext
https://github.com/Lookinghim/WhatsappBirthdayMessageBulkSender.git
```

2. Create a virtual environment (optional but recommended):

```plaintext
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```


3. Install the required packages:

```plaintext
pip install -r requirements.txt
```

## Configuration

1. Open `config.py` and update the following variables:

1. `CHROME_PROFILE_NAME`: The name of your Chrome profile (e.g., "Default" or "Profile 1")
2. `EXCEL_FILE_PATH`: The path to your Excel file containing contact information
3. `SCHEDULED_TIME`: The time you want the script to run daily (format: "HH:MM")



2. Prepare your Excel file with the following columns:

1. `phone number (including country code)`
2. `message`
3. `birthday` (format: DD/MM)


Example Excel file content:

| phone number (including country code) | message | birthday
|-----|-----|-----
| +1234567890 | Happy birthday! 🎉 | 15/03
| +9876543210 | Wishing you a great day! | 22/07





## Usage

1. Ensure you're logged into WhatsApp Web in your Chrome profile before running the script.
2. Run the main script:

```plaintext
python whatsapp_automation.py
```


3. The script will run continuously, executing the scheduled task daily at the specified time.
4. To stop the script, press Ctrl+C in the terminal where it's running.


## Important Notes

- Keep your computer on and the script running for the scheduled task to work.
- Do not interact with the Chrome window while the script is sending messages.
- The script uses your existing WhatsApp Web session, so make sure you're logged in.
- Messages will only be sent to contacts whose birthday matches the current date.
- Ensure your Excel file is always up-to-date with the correct information.


## Troubleshooting

If you encounter any issues:

1. Chrome visibility problems:

1. Run the `test_chrome_visibility.py` script to check if Chrome is working correctly with Selenium.
2. Ensure ChromeDriver version matches your Chrome browser version.



2. WhatsApp Web not loading:

1. Check your internet connection.
2. Verify that you're logged into WhatsApp Web in the specified Chrome profile.



3. Messages not sending:

1. Double-check the phone numbers in your Excel file, ensuring they include the country code.
2. Verify that the Excel file is not open in another program while the script is running.



4. Script crashes or stops unexpectedly:

1. Check the log file for error messages.
2. Ensure all required packages are installed correctly.
3. Verify that your Chrome profile path is correct in the `config.py` file.



5. Scheduled task not running:

1. Make sure your computer doesn't go to sleep at the scheduled time.
2. Check that the `SCHEDULED_TIME` in `config.py` is set correctly.





If problems persist, try the following:

- Clear your Chrome browser cache and cookies.
- Reinstall Chrome and ChromeDriver.
- Check for any updates to the project or its dependencies.


## Disclaimer

This script is for educational purposes only. Use it responsibly and in accordance with WhatsApp's terms of service. The authors are not responsible for any misuse or any consequences arising from the use of this script.

- This tool is not officially associated with WhatsApp or any of its affiliates.
- Automated messaging may violate WhatsApp's terms of service. Use at your own risk.
- Be mindful of local laws and regulations regarding automated messaging and data privacy.
- Do not use this script for spam or any malicious purposes.
- The authors are not responsible for any account suspensions or bans resulting from the use of this script.


By using this script, you agree to these terms and take full responsibility for its use.
