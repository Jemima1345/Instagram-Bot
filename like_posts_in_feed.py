from bot import InstagramBot

my_bot = InstagramBot()
#my_bot.driver.get(my_bot.login_url) #goes to home page (following)
my_bot.like_posts_in_feed()
print('Done liking posts \n') #for crontab log