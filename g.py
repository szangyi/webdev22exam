
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

COOKIE_SECRET = "my secret key"

SESSIONS = []

TWEETS = []



##############################

TABS_LOGGEDIN = [
  {"icon": "fa fa-home", "title": "Home", "id":"home", "href":"./index"},
  {"icon": "fa fa-user", "title": "Profile", "id": "profile", "href":"./user_profile"},
]

TABS_LOGGEDOUT = [
  {"icon": "fa fa-home", "title": "Home", "id":"home"},
]

PEOPLE = [
  {"src": "stephie.png", "name": "Stephie Jensen", "handle": "@sjensen"},
  {"src": "monk.jpg", "name": "Adrian Monk", "handle": "@detective :)"},
  {"src": "kevin.jpg", "name": "Kevin Hart", "handle": "@miniRock"}
]

TRENDS = [
  {"top": "Music", "title": "We Won", "bottom": "135K Tweets"},
  {"top": "Pop", "title": "Blue Ivy", "bottom": "40k tweets"},
  {"top": "Trending in US", "title": "Denim Day", "bottom": "40k tweets"},
]