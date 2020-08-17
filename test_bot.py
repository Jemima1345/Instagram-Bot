from bot import InstagramBot

my_bot = InstagramBot()

user = "guitarcenter"
my_bot.nav_user(user)
my_bot.get_users_in_list('followers')
#my_bot.follow_multiple_users(3)

#special_people = ['guitarcenter', 'billy.musgrave'] #people I don't want to unfollow
#special_accounts = my_bot.find_manually_followed()
##prevents nested list
#for account in special_accounts:
    #special_people.append(account)
#print(f'Special accounts: {special_accounts}')
#print(f'Special people: {special_people}')
#my_bot.unfollow_not_following_back(special_people)

#my_bot.nav_user('guitarcenter')
#follower_num = my_bot.get_follow_num('followers')
#print(follower_num)

#my_bot.infinite_page_scroll()
#my_bot.open_users_list('followers')
#my_bot.infinite_list_scroll()
#time.sleep(60)

#my_bot.save_has_fllwd_list()