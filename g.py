from bottle import response, redirect, view, route
import re


REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

COOKIE_SECRET = "my secret key"

SESSIONS = []

EMAIL_PW = "xaqba0-xyjfyh-dodcEj"
APP_PW = "msllctgtbeflvlvm"
# APP_PW = "msll ctgt befl vlvm"

##############################

TABS_LOGGEDIN = [
  {"icon": "fa fa-home", "title": "Home", "id":"home", "href":"./index"},
  {"icon": "fa fa-user", "title": "Profile", "id": "profile", "href":"./user_profile_my"},
  {"icon": "fa fa-gear", "title": "Settings", "id": "settings", "href":"./settings"},
]

TABS_LOGGEDOUT = [
  {"icon": "fa fa-home", "title": "Home", "id":"home", "href":"./index"},
]

TABS_ADMIN = [
  {"icon": "fa fa-home", "title": "Home", "id":"home", "href":"./index_admin"},
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



############################## VALIDATION

def _send(status = 400, error_message = "unknown error"):
  response.status = status
  print("SEND 400000000")
  return {"info":error_message}

def _is_item_tweet(text=None):
  min, max = 1, 280
  error = f"item_name {min} to {max} characters. No spaces"
  if not text: return None, error
  text = re.sub("[\n\t]*", "", text)
  text = re.sub(" +", " ", text)
  text = text.strip()
  if len(text) < min or len(text) > max : return None, error
  text = text.capitalize()
  return text, None

def _is_item_textshort(text=None):
  min, max = 2, 20
  error = f"item_name {min} to {max} characters. No spaces"
  if not text: return None, error
  text = re.sub("[\n\t]*", "", text)
  text = re.sub(" +", " ", text)
  text = text.strip()
  if len(text) < min or len(text) > max : return None, error
  text = text.capitalize()
  return text, None

def _is_item_textmedium(text=None, language="en"):
  min, max = 5, 15
  error = f"item_name {min} to {max} characters. No spaces"
  if not text: return None, error
  text = re.sub("[\n\t]*", "", text)
  text = re.sub(" +", " ", text)
  text = text.strip()
  if len(text) < min or len(text) > max : return None, error
  # if " " in text : return None, errors[language]
  text = text.capitalize()
  return text, None

def _is_item_textlong(text=None, language="en"):
  min, max = 10, 100
  error = f"item_name {min} to {max} characters. No spaces"
  if not text: return None, error
  text = re.sub("[\n\t]*", "", text)
  text = re.sub(" +", " ", text)
  text = text.strip()
  if len(text) < min or len(text) > max : return None, error
  text = text.capitalize()
  return text, None

def _is_item_email(text=None):
  error = f"A valid e-mail format is: 'example@email.com'. No spaces"
  if not text : return None, error
  regex_email = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
  if not re.match(regex_email, text) : return None, error
  return text, None

def _is_uuid4(text=None, language="en"):
  error = "id must be a valid uuid"
  if not text: return None, error
  regex_uuid4 = "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
  if not re.match(regex_uuid4, text) : return None, error
  return text, None
