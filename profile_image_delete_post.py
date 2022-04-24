from turtle import up
from bottle import post, redirect, request, view, response
import uuid
import time
import g
import uuid
import os
import imghdr
import pymysql
from PIL import Image  


##############################
@post("/profile_image_delete")
@view("settings")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    
    ### DEFINE THE VARIABLES ###
    user_id = request.forms.get("user_id")
    image_name_prev = request.forms.get("user_image_ref")
    os.remove(f"images/{image_name_prev}") # remove old
    image_name_default = "default_user_profile_image.jpg" # use default

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

        sql = """ 
            UPDATE users_images 
            SET image_ref =%s
            WHERE fk_user_id=%s
        """       

        var = (image_name_default, user_id)
        cur.execute(sql, var)

        db.commit()
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        return redirect("/settings")
    

    ### RETURN ###
    # if session is None:
    #     return redirect("/login")

    