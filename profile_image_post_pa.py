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


@post("/profile_image")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

    ################ DEFINE THE VARIABLES ################
    user_id = request.forms.get("user_id")
    image_id = str(uuid.uuid4())  
    upload = request.files.get("upload")
    name, ext = os.path.splitext(upload.filename) # .png .jpeg .zip .mp4
    if ext == ".jpg": ext = ".jpeg"
    image_name = f"{image_id}{ext}" # Create new image name

    import production
    db_config = g.DB_PROD

    upload.save(f"/home/szangyi/webdev22exam/images/{image_name}")

################ VALIDATE ################
    image_id, error_id = g._is_uuid4(image_id)
    if error_id : return g._send(400, error_id)
    imghdr_extension = imghdr.what(f"/home/szangyi/webdev22exam/images/{image_name}")
    if ext != f".{imghdr_extension}":
        print("not an image")
        os.remove(f"/home/szangyi/webdev22exam/images/{image_name}")
        return redirect("/profile_image?error=wrong_filetype")

    try:
################ CONNECT TO DB AND EXECUTE ################
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        sql = """INSERT INTO users_images (image_id, fk_user_id, image_ref) 
        VALUES (%s, %s, %s)
        """
        var = (image_id, user_id, image_name)
        cur.execute(sql, var)
        db.commit()
        response.status = 201
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()
        return redirect("/index_loggedin")

    