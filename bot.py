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
        time.sleep(2)
        
    
    def log_in(self):
        """
        The bot logs into instagram and clicks not now to prevent storing log in info 
        and again to prevent turning on notifications
        """

        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input[@class="_2hvTZ pexuQ zyHYP"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input[@class="_2hvTZ pexuQ zyHYP"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        time.sleep(2)

        
my_bot = InstagramBot(username, password)
my_bot.log_in()
