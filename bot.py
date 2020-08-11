from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
import os
from configparser import ConfigParser


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
        #self.users_followers_url = config['IG_URLS']['users_followers_url']
        
        self.driver = webdriver.Chrome('chromedriver')
        self.driver.get(self.login_url)
        time.sleep(2)
        
    
    def log_in(self):
        """
        The bot logs into instagram and clicks not now to prevent storing log in info 
        and again to prevent turning on notifications
        """
        
        username_input = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input[@class="_2hvTZ pexuQ zyHYP"]')
        username_input.send_keys(self.username)
        password_input = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input[@class="_2hvTZ pexuQ zyHYP"]')
        password_input.send_keys(self.password)
        login_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
        login_btn.click()
        time.sleep(3)
        
        not_now_btn1 = self.driver.find_element_by_xpath('//*[text() = "Not Now"]')
        not_now_btn1.click()
        #must redefine btn to avoid error
        not_now_btn2 = self.driver.find_element_by_xpath('//*[text() = "Not Now"]')
        not_now_btn2.click()
        time.sleep(1)
        
        #The following also works
        #not_now_btn1 = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        #not_now_btn1.click()
        #not_now_btn2 = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        #not_now_btn2.click()
        #time.sleep(1)
        
        
    def nav_user(self, user):
        """
        Navigates to a specified user's page
        """
        self.driver.get(self.user_url.format(user))
        time.sleep(1)
        
        
    def follow_user(self):
        """
        Follows a user when on their page
        """
        #follow_btn = self.driver.find_element_by_xpath('//*[contains(@class,"_6VtSN")')
        #follow_btn = self.driver.find_element_by_xpath("//button[contains(text(),'Follow')")
        
        #follow_btn = self.driver.find_element_by_xpath('//*[@class="_5f5mN       jIbKX  _6VtSN     yZn4P   "]') #also works
        follow_btn = self.driver.find_element_by_xpath('//*[text() = "Follow"]')
        follow_btn.click()
        time.sleep(2)

    
    def open_users_followers(self): #, user):
        """
        Opens a user's follower list when the user's page is already open
        """
        #self.driver.get(self.users_followers_url.format(user))
        followers_btn = self.driver.find_element_by_partial_link_text("followers")
        followers_btn.click()
        time.sleep(2)

        
my_bot = InstagramBot()
my_bot.log_in()

account = "guitarcenter"
my_bot.nav_user(account)

#TODO: if it finds the follow button, follow user
#my_bot.follow_user()


my_bot.open_users_followers()
my_bot.follow_user()