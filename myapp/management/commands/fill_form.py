# myapp/management/commands/fill_form.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from PIL import Image

class Command(BaseCommand):
    help = 'Fill out Google Form and send confirmation email'

    def handle(self, *args, **kwargs):
        # Set up Selenium and fill out the form
        browser = webdriver.Chrome()
        browser.get("https://docs.google.com/forms/d/e/1FAIpQLSdUCd3UWQ3VOgeg0ZzNeT-xzNawU8AJ7Xidml-w1vhfBcvBWQ/viewform")
        time.sleep(1)

        # Fill out the form
        form_data = {
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input': 'Ashwanthram',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input': '8056160053',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input': 'ashwanth0110@gmail.com',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/textarea': 'No32,thiruvalluvar street,metha nagar,chennai-600031',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input': '600031',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input': '01-10-2003',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input': 'male',
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input': 'GNFPYC',
        }

        for xpath, value in form_data.items():
            element = browser.find_element(By.XPATH, xpath)
            element.send_keys(value)
            time.sleep(1)

        # Submit the form
        submit_button = browser.find_elements(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit_button[0].click()
        time.sleep(5)

        # Take a screenshot of the confirmation page
        screenshot_path = 'confirmation_screenshot.png'
        browser.save_screenshot(screenshot_path)

        # Close the browser
        browser.quit()

        # Send email with the screenshot
        self.send_email(screenshot_path)

    def send_email(self, screenshot_path):
        subject = 'Python (Selenium) Assignment - Ashwanthram'
        message = 'find the attached screenshot here.'
        email = EmailMessage(
            subject,
            message,
            'ash01102003@gmail.com',
            ['tech@themedius.ai'],
            cc=['HR@themedius.ai']
        )

        # Attach the screenshot
        with open(screenshot_path, 'rb') as f:
            email.attach('confirmation_screenshot.png', f.read(), 'image/png')

        email.send()

