from bot import InstagramBot

my_bot = InstagramBot
bad_people = my_bot.get_not_following_back()
special_people = ['guitarcenter', 'billy.musgrave'] #people I don't want to unfollow
special_accounts = my_bot.find_manually_followed()

#prevents nested list
for account in special_accounts:
    special_people.append(account)
my_bot.unfollow_not_following_back(bad_people, special_people)

#print(special_accounts)
#print(special_people)