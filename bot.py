from selenium import webdriver
import time
import os
from configparser import ConfigParser


##TODO: fix get_follow_num error scenario 
##TODO: store a user who is followed from their page in the has_fllwd list


class InstagramBot:
    def __init__(self):       
        """
        Creates an instance of the InstagramBot class. Reads in the list of people it has followed 
        """
        
        self.bot_fllwd = self.get_has_fllwd_list()
        
        config = ConfigParser()
        config_file = 'config.ini'
        config.read(config_file)    
        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']
        
        self.login_url = config['IG_URLS']['login_url']
        self.user_url = config['IG_URLS']['user_url']
        #self.users_followers_url = config['IG_URLS']['users_followers_url']
        
        self.driver = webdriver.Chrome('/home/jemima/WingProjects/InstagramBot/chromedriver')
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
            print('Not a valid list. Can only open "followers" or "following" list')
            users_list = input("Enter a user's list to open: ")
            self.open_users_list(users_list)
        
    
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
            
            if username not in self.bot_fllwd: 
                follow_btn = self.find_button("Follow")
                follow_btn.click()
                self.bot_fllwd.append(username)
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
            has_fllwd_string = "\n".join(self.bot_fllwd)
            file.write(has_fllwd_string)
        
    
    def infinite_list_scroll(self):
        """
        Scrolls to the bottom of following/ follower list
        """
        #self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        #time.sleep(2)
        
        SCROLL_PAUSE_TIME = 1
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        old_height = self.driver.execute_script('arguments[0].scrollTop', scroll_box) #top of list
        
        while True:
            new_height = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                                                       return arguments[0].scrollHeight""", scroll_box) 
            time.sleep(SCROLL_PAUSE_TIME)
            if new_height == old_height: #cannot scroll anymore
                break       
            old_height = new_height

        
    def infinite_page_scroll(self):
        """
        Scrolls down to the bottom of a page when the page is already open
        Doesn't work for scrolling down following/ follower list
        """
        
        SCROLL_PAUSE_TIME = 4
        old_ht = self.driver.execute_script('return document.body.scrollHeight;')
        
        while True:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(SCROLL_PAUSE_TIME)
            new_ht = self.driver.execute_script('return document.body.scrollHeight;')
            if old_ht == new_ht:
                break
            old_ht = new_ht
            
    
    def get_users_in_list(self):
        """
        Gets all the usernames of people in instagram following/ follower list and puts them in a list
        Only works when the following/ follower list is open
        """
        username_list = []
        user_id_list = self.driver.find_elements_by_xpath('//*[@class = "FPmhX notranslate  _0imsa "]')
        for user in user_id_list:
            username = user.get_attribute('title')
            username_list.append(username)
        print (len(username_list), username_list)
        return username_list
        
    
    def get_not_following_back(self):
        """
        Finds who is not following you back and puts them in a list
        """
        not_following_back = []
        self.nav_user(self.username)
        self.open_users_list('following')
        self.infinite_list_scroll()
        following = self.get_users_in_list()
        self.close_users_list()
        
        self.open_users_list('followers')
        self.infinite_list_scroll()
        followers = self.get_users_in_list()
        
        for user in following:
            if user not in followers:
                not_following_back.append(user)
        print(not_following_back)
        return not_following_back
    
    
    def unfollow_not_following_back(self, not_following_back, do_not_unfollow):
        """
        Unfollows everyone who is not following you back
        """
        for person in do_not_unfollow:
            not_following_back.remove(person)
        
        for user in not_following_back:
            self.nav_user(user)
            self.unfollow_user()
            
    
    def unfollow_everyone(self):
        """
        Unfollows everyone that you're following
        TODO: This is inefficient. Unfollow them directly from your following list without 
        saving their names in a list or navigating to their page
        """

        following = self.get_users_in_list('following')
        for user in following:
            self.nav_user(user)
            self.unfollow_user(user)
            

    def get_follow_num(self, follow_type):
        """
        Finds how many followers a user has or the number of people a user is following
        
        Args:
        follow_type:str: specifies if to get number of 'followers' or 'following'
        """
        
        if follow_type == "followers" or follow_type == "following":
            follow_box = self.driver.find_element_by_partial_link_text("{}".format(follow_type))
            follow_num_statement = follow_box.text #.text gives the Name of the link text
            follow_num = follow_num_statement.split(" ")[0]
            #print(follow_num)
            return follow_num   
        else:
            print('Cannot get follow num for that follow type. Must enter either "followers" or "following"')
            follow_type = input('Enter a follow type: ')
            follow_num = self.get_follow_num(follow_type)  
            return follow_num
        
     
    def find_manually_followed(self):
        """
        Finds users who were followed manually instead of through the bot and puts them in a list
        """
        self.nav_user(self.username)
        self.open_users_list('following')
        following = self.get_users_in_list()
       
        manually_followed = []
        for user in following: 
            if user not in self.bot_fllwd:
                manually_followed.append(user)
        return manually_followed
    
          
my_bot = InstagramBot()
my_bot.log_in()

#user = "guitarcenter"
#my_bot.nav_user(user)
#my_bot.open_users_list('followers')
#my_bot.follow_multiple_users(3)

#bad_people = my_bot.get_not_following_back()
#special_people = ['guitarcenter', 'billy.musgrave'] #people I don't want to unfollow
#special_accounts = my_bot.find_manually_followed()
##prevents nested list
#for account in special_accounts:
    #special_people.append(account)
#print(special_accounts)
#print(special_people)
#my_bot.unfollow_not_following_back(bad_people, special_people)

my_bot.nav_user('guitarcenter')
follower_num = my_bot.get_follow_num('followers')
print(follower_num)

#my_bot.infinite_page_scroll()
#my_bot.open_users_list('followers')
#my_bot.infinite_list_scroll()
#time.sleep(60)

#my_bot.save_has_fllwd_list()