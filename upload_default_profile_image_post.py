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
@post("/upload_default_profile_image")
# @view("upload_profile_image")
def _():
    try:

        ### DEFINE THE VARIABLES ###
        # response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)

        image_id = str(uuid.uuid4())  
        image_name = "default_user_profile_image.jpg"


        ### VALIDATE ###
        # Validate extension
        # if file_extension not in (".png", ".jpeg", ".jpg"):
        #     return "image not allowed"


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

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

    