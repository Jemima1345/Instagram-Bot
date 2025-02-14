from selenium import webdriver
import time
import datetime
import os
from configparser import ConfigParser
from selenium.common.exceptions import NoSuchElementException


##TODO: sometimes it doesn't scroll all the way down a list of users
##TODO: store a user who is followed from their page in the has_fllwd list


class InstagramBot:
    def __init__(self):       
        """
        Creates an instance of the InstagramBot class. Reads in the list of people it has followed 
        and logs into instagram
        """
        
        self.bot_fllwd = self.get_has_fllwd_list()
        
        config = ConfigParser()
        config_file = 'config.ini'
        config.read(config_file)    
        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']
        self.login_url = config['IG_URLS']['login_url']
        self.user_url = config['IG_URLS']['user_url']
        
        self.driver = webdriver.Chrome('/home/jemima/WingProjects/InstagramBot/chromedriver')
        now = datetime.datetime.now()
        print("Current date and time : ")
        print(now.strftime("%Y-%m-%d %H:%M:%S")) #for crontab log
        
        self.driver.get(self.login_url)
        time.sleep(2)
        self.log_in()
        
    
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
        time.sleep(2)
        
        not_now_btn1 = self.find_button("Not Now")
        not_now_btn1.click()
        time.sleep(1)
        #must redefine btn to avoid error
        not_now_btn2 = self.find_button("Not Now")
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
        
        SCROLL_PAUSE_TIME = 2
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
            
    
    def scroll_down(self):
        """
        Scrolls down slightly (not to the bottom of page)
        """
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        
        
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
        print(f'Users in list: {len(username_list)} {username_list}')
        return username_list
        
    
    def get_not_following_back(self):
        """
        Navigates to your page, finds who is not following you back, and puts them in a list
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
        print(f"Not following back: {not_following_back}")
        return not_following_back
    
    
    def unfollow_not_following_back(self, do_not_unfollow = None):
        """
        Unfollows everyone who is not following you back. Only unfollows 20 people on each
        function call to avoid getting banned on instagram
        If they don't pass in people not to unfollow, it will unfollow everyone
        
        Args:
        do_not_unfollow:list: people the user does not want to unfollow. Default is none
        """
        
        not_following_back = self.get_not_following_back()
        for person in do_not_unfollow:
            if person in not_following_back:
                not_following_back.remove(person)
        
        #unfollow everyone at once
        #for user in not_following_back:
            #self.nav_user(user)
            #self.unfollow_user()
        
        #unfollow max 20 people at once   
        if len(not_following_back) <= 20:
            for user in not_following_back:
                self.nav_user(user)
                self.unfollow_user()
        else:
            for counter, user in enumerate(not_following_back):
                if counter < 20: #counter starts from 0
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
        print(f'Manually followed: {manually_followed}') #not necessary
        return manually_followed
    
    
    def like_posts_in_feed(self):
        """
        Either likes 50 posts in my feed or stops after scrolling 3 times
        
        Note: Only like up to 350 per hour to avoid getting banned on instagram 
        """
        self.driver.get(self.login_url) #navigates to feed
        liked_posts = 0
        scroll_num = 1
        while liked_posts < 50 and scroll_num < 3:   
            while True:
                #scrolls down until it finds a post that has not been liked
                like_btns = self.driver.find_elements_by_xpath('//*[@aria-label = "Like"][@height = "24"]')
                #print(f"{len(like_btns)} like buttons found")
                if len(like_btns) > 0:
                    break
                if scroll_num == 3:
                    break                
                self.scroll_down()
                scroll_num += 1
                #print(scroll_num)
                     
            for btn in like_btns:
                if liked_posts == 50:
                    break
                btn.click()
                liked_posts += 1   
        print(f"Liked {liked_posts} posts")
        print(f"Scroll num: {scroll_num}")
        time.sleep(1)
    
    
    def open_post(self):
        """
        Opens first post when page containing posts is already open
        """
        POST_LOADING_TIME = 5
        post = self.driver.find_element_by_class_name("eLAPa")
        post.click()
        time.sleep(POST_LOADING_TIME)
        
    
    def like_all_comments(self):
        """
        Likes all the comments on a single post except comment replies. Infinite.
        Post must already be open
        """
        breaker = True
        while breaker:
            like_btns = self.driver.find_elements_by_xpath('//*[@aria-label = "Like"][@height = "12"]')
            print(f"{len(like_btns)} like buttons found")
            if len(like_btns) == 0:            
                try:
                    self.driver.find_element_by_xpath('//*[@aria-label = "Load more comments"]').click()
                except NoSuchElementException:
                    breaker = False #if there are no more comments to like, then stop
            for btn in like_btns:
                btn.click()
            time.sleep(1)        
            
            
    def like_comments_on_my_posts(self, post_num = 10):
        """
        Likes comments on my most recent posts. 10 by default 
        """
        self.nav_user(self.username)
        self.open_post()
        for post in range(0, post_num):
            self.like_all_comments()
            try:
                next_btn = self.driver.find_element_by_xpath('//*[text() = "Next"]')
                next_btn.click()
            except NoSuchElementException:
                break #if no next button is found, it has reached the last post
            time.sleep(1)
    
    
    def watch_stories(self):
        """
        Watches stories from people I follow (on my home page)
        """
        self.driver.get(self.login_url)
        story_btn = self.driver.find_element_by_class_name('OE3OK ')
        story_btn.click()
        time.sleep(1)
        while True:
            try:
                next_btn = self.driver.find_element_by_class_name('ow3u_')
                next_btn.click()
                time.sleep(0.5)
            except NoSuchElementException:
                break