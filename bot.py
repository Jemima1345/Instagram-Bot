from selenium import webdriver
import time
import os
from login_info import username
from login_info import password


class InstagramBot:
    def __init__(self, username, password):       
        self.driver = webdriver.Chrome('chromedriver')
        self.username = username
        self.password = password
        
        self.driver.get('https://www.instagram.com/')


my_bot = InstagramBot(username, password)
