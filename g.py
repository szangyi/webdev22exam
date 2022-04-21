from bottle import response, redirect
import re


REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

COOKIE_SECRET = "my secret key"

SESSIONS = []

##############################

TABS_LOGGEDIN = [
  {"icon": "fa fa-home", "title": "Home", "id":"home", "href":"./index"},
  {"icon": "fa fa-user", "title": "Profile", "id": "profile", "href":"./user_profile_my"},
  {"icon": "fa fa-gear", "title": "Settings", "id": "settings", "href":"./settings"},
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



############################## VALIDATION

def _send(status = 400, error_message = "unknown error"):
  response.status = status
  # return redirect(f"/signup?error=user_first_name")
  return {"info":error_message}
  # return redirect("/")

def _is_item_name(text=None, language="en"):
  min, max = 2, 20
  errors = {
    "en":f"item_name {text} {min} to {max} characters. No spaces", 
    "dk":f"item_name {min} til {max} tegn. Uden mellemrum",
    "sp":f"item_name {min} a {max} charácters. Sin espacios",
  }
  if not text: return None, errors[language]
  text = re.sub("[\n\t]*", "", text)
  text = re.sub(" +", " ", text)
  text = text.strip()
  if len(text) < min or len(text) > max : return None, errors[language]
  # if " " in text : return None, errors[language]
  text = text.capitalize()
  return text, None
