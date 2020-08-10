from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
import os
from configparser import ConfigParser
#from login_info import username
#from login_info import password


class InstagramBot:
    def __init__(self):       
        """
        Creates an instance of the InstagramBot class  
        """
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument('--no-sandbox')
        
        config = ConfigParser()
        config_file = 'config.ini'
        config.read(config_file)    
        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']
        self.login_url = config['IG_URLS']['login_url']
        self.user_url = config['IG_URLS']['user_url']
        self.users_followers_url = config['IG_URLS']['users_followers_url']
        
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.get(self.login_url)
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
        time.sleep(1)
       
        
    def nav_user(self, user):
        """
        Navigates to a specified user's page
        """
        self.driver.get(self.user_url.format(user))
        
        
    def open_users_followers(self, user):
        """
        Navigates to a specified user's follower list
        """
        self.driver.get(self.users_followers_url.format(user))
        time.sleep(2)

        
my_bot = InstagramBot()
my_bot.log_in()

account = "guitarcenter"
#my_bot.nav_user(account)
my_bot.open_users_followers(account)
