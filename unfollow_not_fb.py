from bot import InstagramBot


my_bot = InstagramBot()
special_people = ['guitarcenter', 'billy.musgrave', 'maciejguitarist'] #people I don't want to unfollow
special_accounts = my_bot.find_manually_followed()

#prevents nested list
for account in special_accounts:
    special_people.append(account)
    
my_bot.unfollow_not_following_back(special_people)
my_bot.save_has_fllwd_list() #not necessary

print('Done unfollowing people') #for crontab log