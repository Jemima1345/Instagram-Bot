from bot import InstagramBot

my_bot = InstagramBot()

my_bot.watch_stories()


#TODO: fix scrolling issues
#user = "guitar.stuff239"
#my_bot.nav_user(user)
#my_bot.open_users_list('followers')
#my_bot.get_users_in_list()
#my_bot.open_users_list('following')
#my_bot.get_users_in_list()

#user = "fuzzinating"
#my_bot.nav_user(user)
#my_bot.open_users_list('followers')
#my_bot.get_users_in_list()
#my_bot.open_users_list('following')
#my_bot.get_users_in_list()

my_bot.save_has_fllwd_list()