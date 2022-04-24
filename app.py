from bottle import default_app, get, response, static_file, run, request
import git
import pymysql


##############################
@get("/app.css")
def _():
  return static_file("app.css", root=".")

##############################
@get("/css/custom.css")
def _():
  return static_file("custom.css", root="./css")

##############################
@get("/js/app.js")
def _():
  return static_file("app.js", root="./js")

##############################
@get("/js/validator.js")
def _():
  return static_file("validator.js", root="./js")

##############################
@get("/images/<image_name>")
def _(image_name):
  print(image_name)
  return static_file(image_name, root="./images")


##############################
import home_get_loggedin    # GET  
import home_get_admin       # GET  
import home_get             # GET  
import home_get_loggedout   # GET  
import signup_get           # GET   
import login_get            # GET
import logout_get           # GET
import user_profile_my_get  # GET
import user_profile_any_get  # GET
import profile_image_get    #GET
import user_update_get

import signup_post          # POST
import login_post           # POST
import tweet_add_post       # POST
import tweet_delete_post    # POST
import tweet_update_post    # POST
import profile_image_post   # POST
import profile_image_delete_post   # POST
import profile_image_default_post   # POST
import profile_image_update_post   # POST
import user_update_post


@app.route('/update_server', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('path/to/git_repo')
            origin = repo.remotes.origin
origin.pull()



##############################
try:
  print("production mode")
  import production
  db_config = {
    "host":"szangyi.mysql.eu.pythonanywhere-services.com", 
    "user":"szangyi", 
    "password":"sedHuq-piwdyh-xergy9", 
    "database":"szangyi$twitter", 
    "cursorclass":pymysql.cursors.DictCursor
  }
except Exception as ex:
  print("development mode")
  print(ex)
  db_config = {
    "host":"localhost", 
    "port":8889,
    "user":"root", 
    "password":"root", 
    "database":"twitter", 
    "cursorclass":pymysql.cursors.DictCursor
  }

db = pymysql.connect(**db_config)
cur = db.cursor()


##############################
try:
  print("production mode")
  import production
  application = default_app()
except Exception as ex:
  print("development mode")
  print(ex)  
  run(host="127.0.0.1", port=1111, debug=True, reloader=True, server="paste")
