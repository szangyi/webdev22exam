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
# from PIL import Image  



##############################
@post("/profile_image")
def _():
    ### DEFINE THE VARIABLES ###
    user_id = request.forms.get("user_id")
    image_id = str(uuid.uuid4())  
    upload = request.files.get("upload")
    name, ext = os.path.splitext(upload.filename) # .png .jpeg .zip .mp4
    if ext == ".jpg": ext = ".jpeg"
    image_name = f"{image_id}{ext}" # Create new image name
    upload.save(f"images/{image_name}")

    ### VALIDATE ###
    image_id, error_id = g._is_uuid4(image_id)
    if error_id : return g._send(400, error_id)
    imghdr_extension = imghdr.what(f"images/{image_name}")
    if ext != f".{imghdr_extension}":
        print("not an image")
        os.remove(f"images/{image_name}")
        return redirect("/profile_image?error=wrong_filetype")
        # return "image not allowed"

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

        sql = """INSERT INTO users_images (image_id, fk_user_id, image_ref) 
        VALUES (%s, %s, %s)
        """
        var = (image_id, user_id, image_name)
        cur.execute(sql, var)
        db.commit()
     
        
    except Exception as ex:
        print("------------")
        print("error2")
        print(ex)
    finally:
        db.close()
        return redirect("/index_loggedin")

    ###################### RETURN ########################
    # if session is None:
    #     return redirect("/login")

    