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
@post("/profile_image_update")
@view("settings")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

    print("production mode")
    import production
    db_config = g.DB_PROD

################ DEFINE THE VARIABLES ################
    user_id = request.forms.get("user_id")
    image_id_updated = str(uuid.uuid4())
    upload = request.files.get("upload")
    name, ext_updated = os.path.splitext(upload.filename)
    if ext_updated == ".jpg": ext_updated = ".jpeg"
    image_name_updated = f"{image_id_updated}{ext_updated}"
    print(image_name_updated)
    upload.save(f"/home/szangyi/webdev22exam/images/{image_name_updated}", overwrite=True)

############### VALIDATE ################
    image_id_updated, error_id = g._is_uuid4(image_id_updated)
    if error_id : return g._send(400, error_id)
    imghdr_extension = imghdr.what(f"/home/szangyi/webdev22exam/images/{image_name_updated}")
    if ext_updated != f".{imghdr_extension}":
        # NOT A VALID FILETYPE
        print("not an image")
        os.remove(f"/home/szangyi/webdev22exam/images/{image_name_updated}")
        return redirect(f"/settings?error=wrong_filetype")
    else:
        # VALID FILETYPE
        print("definitely an image")
        image_name_prev = request.forms.get("user_image_ref")
        if image_name_prev != "default_user_profile_image.jpg":
            os.remove(f"/home/szangyi/webdev22exam/images/{image_name_prev}")  #OLD image - remove from local
        upload.save(f"/home/szangyi/webdev22exam/images/{image_name_updated}", overwrite=True) #NEW IMAGE - save to local

    try:
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        sql = """
            UPDATE users_images
            SET image_id =%s,
            image_ref =%s
            WHERE fk_user_id=%s
        """

        var = (image_id_updated, image_name_updated, user_id)
        cur.execute(sql, var)
        db.commit()
        response.status = 200
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()
        return redirect("/settings")
