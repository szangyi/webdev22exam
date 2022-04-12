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
@post("/upload_profile_image")
# @view("upload_profile_image")
def _():
    try:

        ### DEFINE THE VARIABLES ###
        # response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        # user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
        user_id = request.forms.get("user_id")

        image_id = str(uuid.uuid4())  
        upload = request.files.get("upload")
        print("####upload")
        print(upload)
        name, ext = os.path.splitext(upload.filename) # .png .jpeg .zip .mp4
        image_name = f"{image_id}{ext}" # Create new image name
        upload.save(f"images/{image_name}")   # Save the image

        ### VALIDATE ###
        # Validate extension
        # if file_extension not in (".png", ".jpeg", ".jpg"):
        #     return "image not allowed"


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        sql = """INSERT INTO users_images (image_id, fk_user_id, image_ref) 
        VALUES (%s, %s, %s)
        """
        var = (image_id, user_id, image_name)
        cur.execute(sql, var)
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

    