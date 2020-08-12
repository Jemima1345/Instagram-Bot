from selenium import webdriver
import time
import os
from configparser import ConfigParser


##TODO: 
##TODO: store a user who is followed from their page in the has_fllwd list


class InstagramBot:
    def __init__(self):       
        """
        Creates an instance of the InstagramBot class. Reads in the list of people it has followed 
        """
        
        self.has_fllwd = self.get_has_fllwd_list()
        
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
        time.sleep(2)
        #must redefine btn to avoid error
        not_now_btn2 = self.driver.find_element_by_xpath('//*[text() = "Not Now"]')
        not_now_btn2.click()
        time.sleep(1)
        
        
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
        #follow_btn = self.driver.find_element_by_xpath('//*[text() = "Follow"]')
        follow_btn = self.find_button("Follow")
        follow_btn.click()
        time.sleep(1)
        
        
    def unfollow_user(self):
        """
        Unfollows a user when on their page
        """
        
        unfollow_btn = self.driver.find_element_by_xpath('//*[@aria-label = "Following"]')
        unfollow_btn.click()
        confirm_unfollow_btn = self.find_button("Unfollow")
        confirm_unfollow_btn.click()
        time.sleep(1)
        
    
    def open_users_list(self, users_list):
        """
        Opens either a user's follower or following list when the user's page is already open
        
        Args:
        users_list:str: Which list to open (followers/ following)
        """  
        
        if users_list == "followers" or users_list == "following":
            list_btn = self.driver.find_element_by_partial_link_text("{}".format(users_list))
            list_btn.click()
            time.sleep(2) 
        else:
            print('Not a valid list')
        
    
    def open_users_followers(self): #, user):
        """
        Opens a user's follower list when the user's page is already open
        """
        #self.driver.get(self.users_followers_url.format(user))
        followers_btn = self.driver.find_element_by_partial_link_text("followers")
        followers_btn.click()
        time.sleep(2)
        
    
    def open_users_following(self):
        """
        Opens a user's following list when the user's page is already open
        """
        following_btn = self.driver.find_element_by_partial_link_text("following")
        following_btn.click()
        time.sleep(2)        
        
        
    def follow_multiple_users(self, follow_num):
        """
        Follows several users out of a list of users (if it has never followed them before) 
        and stores them in the list of people it has followed.
        Does not work for following a user when on their page (name_id is different)
        
        Args:
        follow_num:int: Number of users to follow
        """

        for user_num in range(0, follow_num):
            name_id = self.driver.find_element_by_xpath('(//*[@class = "FPmhX notranslate  _0imsa "])[{}]'.format(user_num+1))
            username = name_id.get_attribute('title')    
            
            if username not in self.has_fllwd: 
                follow_btn = self.find_button("Follow")
                follow_btn.click()
                self.has_fllwd.append(username)
                time.sleep(1)   
            else:
                print('User has been followed before')

    
    def find_button(self, button):
        """
        Finds buttons by text. Does not work for unfollow button when on the user's page
        """
        
        btn = self.driver.find_element_by_xpath('//*[text() = "{}"]'.format(button))
        return btn
    
    
    def get_has_fllwd_list(self):
        """
        Reads in the list of people it has followed
        """
        with open('list.txt', 'r') as file:
            has_fllwd_string = file.read()
            has_fllwd_list = has_fllwd_string.split("\n")
            return has_fllwd_list
        
        
    def save_has_fllwd_list(self):
        """
        Saves the updated list of people it has followed into a txt file
        """
        with open('list.txt', 'w') as file:
            has_fllwd_string = "\n".join(self.has_fllwd)
            file.write(has_fllwd_string)
            
    
    def scroll_down(self):
        """
        Scrolls down to the bottom of page
        """
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        
    
my_bot = InstagramBot()
my_bot.log_in()

#account = "guitarcenter"
#my_bot.nav_user(account)
#my_bot.open_users_list('followers')
#my_bot.follow_multiple_users(3)

my_bot.nav_user('guitar.stuff239')
my_bot.open_users_list('following')
my_bot.scroll_down()

#my_bot.nav_user('ana.hinojosa.12')


my_bot.save_has_fllwd_list()