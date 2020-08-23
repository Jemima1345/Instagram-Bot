from bot import InstagramBot


my_bot = InstagramBot()
user = "guitarcenter"
my_bot.nav_user(user)
my_bot.open_users_list('followers')
my_bot.follow_multiple_users(20)

my_bot.save_has_fllwd_list()
print('Done following people \n') #for crontab log
