from bottle import default_app, delete, error, get, request, response, static_file, run


##############################
@get("/app.css")
def _():
  return static_file("app.css", root=".")

##############################
# @get("/style.css")
# def _():
#   return static_file("style.css", root="./style")

##############################
@get("/app.js")
def _():
  return static_file("app.js", root=".")

##############################
@get("/validator.js")
def _():
  return static_file("validator.js", root=".")

##############################
@get("/images/<image_name>")
def _(image_name):
  print(image_name)
  return static_file(image_name, root="./images")


##############################
import home_get_loggedin    # GET  
import home_get             # GET  
import home_get_loggedout   # GET  
import signup_get           # GET   
import login_get            # GET
import logout_get           # GET
import user_profile_get     # GET
import upload_profile_image_get  #GET

import signup_post          # POST
import login_post           # POST
import tweet_add_post       # POST
import tweet_delete_post    # POST
import tweet_update_post    # POST
import upload_profile_image_post  #POST
import upload_default_profile_image_post  #POST



##############################
try:
  import production
  application = default_app()
except Exception as ex:
  run(host="127.0.0.1", port=1111, debug=True, reloader=True, server="paste")




