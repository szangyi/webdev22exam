from turtle import up
from bottle import post, redirect, request, view, response
import uuid
import time
import g
import uuid
from time import gmtime, strftime
import os
import imghdr
import pymysql
from PIL import Image  


##############################
@post("/profile_image_default")
# @view("upload_profile_image")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

    ### DEFINE THE VARIABLES ###
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    image_id = str(uuid.uuid4())  
    image_name = "default_user_profile_image.jpg"

    ### VALIDATE ###
    image_id, error_id = g._is_uuid4(image_id)
    if error_id : return g._send(400, error_id)

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

    try:
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        # db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        # cur = db.cursor()

        ## current user
        sql_user = """ SELECT *
        FROM users 
        WHERE user_email =%s
        """
        cur.execute(sql_user,(user_email,))
        user = cur.fetchone()
        print("---------user")
        print(user)
    
        user_id = user['user_id']
        print("---------userid")
        print(user_id)

        ## add default image when user clicks skip uploading image
        sql = """INSERT INTO users_images (image_id, fk_user_id, image_ref) 
        VALUES (%s, %s, 'default_user_profile_image.jpg')
        """
        var = (image_id, user_id)
        cur.execute(sql, var)
        print("############################################# default image added")

        db.commit()
        
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()
    return redirect("/index_loggedin")

    ###################### RETURN ########################
    # if session is None:
    #     return redirect("/login")

    