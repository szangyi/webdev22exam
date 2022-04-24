from bottle import post, request, redirect, response
import re
import uuid
import g
import jwt
import pymysql
import time


##############################
@post("/login")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")    
    user_session_id = str(uuid.uuid4())
    user_created_at = str(int(time.time()))

################ VALIDATE ################
    user_email, error_e = g._is_item_email(user_email)
    if error_e : return g._send(400, error_e)
    user_password, error_pw = g._is_item_textlong(user_password)
    if error_pw : return g._send(400, error_pw)
    
    try:
        print("production mode")
        import production
        db_config = g.DB_PROD
    except Exception as ex:
        print("development mode")
        print(ex)
        db_config = g.DB_DEV

    try:
################ CONNECT TO DB AND EXECUTE ################
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        ## current user
        sql = """
        SELECT * 
        FROM users 
        WHERE user_email =%s 
        AND user_password=%s """
        var = (user_email, user_password)
        cur.execute(sql, var)
        user = cur.fetchone()
        print("################user logeddin")
        print(user)

        ## current user + current user's image
        sql_user=""" 
        SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user_image = cur.fetchone()
        response.status = 200
    except Exception as ex:
        print(ex)

################ RETURN ################
    if not user:
        print("#"*12)
        print("no match")
        return redirect(f"/login?error=wrong_usercredentials")

    try: 
################ COOKIE ################
        encoded_jwt = jwt.encode({"uuid4": user_session_id, "user_email":user_email}, "secret key", algorithm="HS256")
        response.set_cookie("user_email", user_email, secret=g.COOKIE_SECRET)
        response.set_cookie("encoded_jwt", encoded_jwt)
        response.set_cookie("uuid4", user_session_id)
    except Exception as ex:
        print(ex)
    finally:
        db.close()

################ RETURN ################
    user_password = user_password.lower() # lowercase Adminpassword string
    if user_email == "admin@admin.com" and user_password == "adminpassword":
        return redirect("/index_admin")
    if user:
        if not user_image:
            redirect("/profile_image")
        else:
            redirect("index_loggedin")
   

  
