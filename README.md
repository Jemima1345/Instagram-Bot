# Instagram-Bot

Bot that interacts on instagram like a normal user would and helps you gain followers


## Motivation

Instagram can be very time consuming. The bot saves you time by doing everything you typically would on instagram


## Framework used

Created using Python 3.8 and the Selenium Package


## Features

- Likes comments on your posts
- Watches stories from people you follow
- Scrolls through your feed and likes posts 
- Infinitely scrolls down a user's page to load media
- Follows the followers of a user who is popular in your niche
- Unfollows users who do not follow back, except the ones you specify not to unfollow
- Finds the number of followers a user has and the number of people a user is following
- Scripts are scheduled to run automatically using crontab (spaced out to avoid getting banned on instagram)
  - general_interaction.py - MTRF at 12pm
  - follow_people.py - sun,wed at 12pm, 1pm, 2pm, 3pm, 4pm
  - unfollow_not_fb.py - wed,sat at 6am, 7am, 8am, 9am, 10am

## Credits

- https://github.com/jg-fisher/instagram-bot/tree/2ba72ee2efff4324d1e6dea064a9234ab6da530f
- https://github.com/aj-4/ig-followers
