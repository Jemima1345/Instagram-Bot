from bot import InstagramBot


my_bot = InstagramBot()
my_bot.like_comments_on_my_posts()
print('Done liking comments on my posts') #for crontab log
my_bot.like_posts_in_feed()
print('Done liking posts in feed') #for crontab log
my_bot.watch_stories()
print('Done watching stories \n') #for crontab log