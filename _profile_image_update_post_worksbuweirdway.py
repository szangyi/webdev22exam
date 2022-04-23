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

    ### DEFINE THE VARIABLES ###
    image_id = request.forms.get("user_image_id") 
    upload = request.files.get("upload")
    name, new_ext = os.path.splitext(upload.filename) # .png .jpeg .zip .mp4
    if new_ext == ".jpg": ext = ".jpeg"
    image_name = f"{image_id}{new_ext}" # Create new image name
    print("imagenaaaame")
    print(image_name)
    upload.save(f"images/{image_name}", overwrite=True)
    ### VALIDATE ###
    imghdr_extension = imghdr.what(f"images/{image_name}")
    if new_ext != f".{imghdr_extension}":
        print("not an image")
        os.remove(f"images/{image_name}")
        return redirect("/settings?error=wrong_filetype")
    else:
        os.remove(f"images/{image_name}")


    try:
        ### DEFINE THE VARIABLES ###
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

        image_name_prev = request.forms.get("user_image_ref")
        name, prev_ext = os.path.splitext(image_name_prev) # get previous image's extension and overwrite the new one with it
        ext = prev_ext
        image_id = request.forms.get("user_image_id") 
        upload = request.files.get("upload")
        image_name = f"{image_id}{ext}" # Create new image name
        upload.save(f"images/{image_name}", overwrite=True)   # Save the image

        ### VALIDATE ###
        # Validate extension
        # if file_extension not in (".png", ".jpeg", ".jpg"):
        #     return "image not allowed"

    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        return redirect("/settings")
    

    ### RETURN ###
    # if session is None:
    #     return redirect("/login")

    