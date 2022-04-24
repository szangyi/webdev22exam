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


@post("/profile_image_delete")
@view("settings")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_session_id = request.get_cookie("uuid4")

    try:
        print("production mode")
        import production
        db_config = g.DB_PROD
    
################ DEFINE THE VARIABLES ################
        user_id = request.forms.get("user_id")
        image_name_prev = request.forms.get("user_image_ref")
        os.remove(f"/home/szangyi/webdev22exam/images/{image_name_prev}") # remove old
        image_name_default = "default_user_profile_image.jpg" # use default
    except Exception as ex:
        print("development mode")
        print(ex)
        db_config = g.DB_DEV

################ DEFINE THE VARIABLES ################
        user_id = request.forms.get("user_id")
        image_name_prev = request.forms.get("user_image_ref")
        os.remove(f"images/{image_name_prev}") # remove old
        image_name_default = "default_user_profile_image.jpg" # use default

    try:
################ CONNECT TO DB AND EXECUTE ################
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        sql = """ 
            UPDATE users_images 
            SET image_ref =%s
            WHERE fk_user_id=%s
        """       

        var = (image_name_default, user_id)
        cur.execute(sql, var)

        db.commit()
        response.status = 201
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()
        return redirect("/settings")

    