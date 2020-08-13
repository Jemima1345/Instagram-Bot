from selenium import webdriver
import time
import os
from configparser import ConfigParser


##TODO: scroll_down_list gets caught. does not keep loading and scrolling
##TODO: infinite scroll down user's page
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
            print('Not a valid user list')   
        
    
    def close_users_list(self):
        """
        Closes either a user's following or follower box if it's already open
        """
        self.driver.find_element_by_xpath('//*[@aria-label = "Close"]').click()
    
    
    def follow_multiple_users(self, follow_num):
        """
        Follows several users out of a list of users (if it has never followed them before) 
        and stores them in the list of people it has followed.
        Does not work for following a user when on their page (user_id is different)
        
        Args:
        follow_num:int: Number of users to follow
        """

        for user_num in range(0, follow_num):
            user_id = self.driver.find_element_by_xpath('(//*[@class = "FPmhX notranslate  _0imsa "])[{}]'.format(user_num+1))
            username = user_id.get_attribute('title')    
            
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
        
    
    def scroll_down_list(self):
        """
        Scrolls to the bottom of following/ follower list
        """
        #self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        #time.sleep(2)
        
        scroll_pause_time = 1
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        old_height = self.driver.execute_script("arguments[0].scrollTop", scroll_box)
        
        while True:
            new_height = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                                                       return arguments[0].scrollHeight""", scroll_box) 
            time.sleep(scroll_pause_time)
            if new_height == old_height: #cannot scroll anymore
                break       
            old_height = new_height

        
    def scroll_down_page(self):
        """
        Scrolls down to the bottom of a page
        Doesn't work for scrolling down following/ follower list
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
        
    
    def get_user_list(self):
        """
        Gets all the usernames of people in instagram following/ follower list and puts them in a list
        """
        username_list = []
        user_id_list = self.driver.find_elements_by_xpath('//*[@class = "FPmhX notranslate  _0imsa "]')
        for user in user_id_list:
            username = user.get_attribute('title')
            username_list.append(username)
        print (username_list)
        return username_list
        
    
    def get_unfollowers(self):
        """
        Finds who is not following you back and puts them in a list
        """
        self.nav_user(self.username)
        self.open_users_list('following')
        self.scroll_down_list()
        following = self.get_user_list()
        
        self.close_users_list()
        
        self.open_users_list('followers')
        scroll_down_list()
        followers = self.get_user_list()
        
    
my_bot = InstagramBot()
my_bot.log_in()

my_bot.get_unfollowers()

#account = "guitarcenter"
#my_bot.nav_user(my_account)
#my_bot.open_users_list('followers')
#my_bot.follow_multiple_users(3)

#my_bot.nav_user('art_gallery_666')
#my_bot.open_users_list('following')
#my_bot.scroll_down_list()
#time.sleep(60)


#my_bot.save_has_fllwd_list()