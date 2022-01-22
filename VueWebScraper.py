import json
import smtplib
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def send_email(mail_content, receiver_addresses):
    sender_address = 'ayushnpatel@gmail.com'
    sender_pass = os.getenv('EMAIL_PASSWORD')
    for receiver_address in receiver_addresses:
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Vue 2 Bedroom Available'
        message.attach(MIMEText(mail_content, 'plain'))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()

        session.sendmail(sender_address, receiver_address, text)
    session.quit()

def lambda_handler(*args, **kwargs):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.thevuenj.com/floorplans")

    for i in range(0,15):
        button = driver.find_element(By.XPATH, "//*[@id=\"collapse-tab"+str(i)+"\"]/div/div[3]/a")
        
        if ("2bedroom" in button.get_attribute('textContent').lower()) or "2 bedroom" in button.get_attribute('textContent').lower():
            if ("availability" in button.get_attribute('textContent').lower()) or "available" in button.get_attribute('textContent').lower():
                send_email("Vue 2 Bedroom Available", [os.getenv('RECEIVER_ADDRESS_1'), os.getenv('RECEIVER_ADDRESS_2')])
                return {
                    'statusCode': 200,
                    'body': json.dumps('Successfully scraped Vue Website!')
                }
    driver.quit()
    return {
        'statusCode': 201,
        'body': json.dumps('Failed to find 2 bedroom apartment available.')
    }
