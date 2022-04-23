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
    ### DEFINE THE VARIABLES ###
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")    
    user_session_id = str(uuid.uuid4())
    user_created_at = str(int(time.time()))


    ### VALIDATE ###
    user_email, error_e = g._is_item_email(user_email)
    if error_e : return g._send(400, error_e)
    user_password, error_pw = g._is_item_textlong(user_password)
    if error_pw : return g._send(400, error_pw)
       
    try:
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output

        # current user
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

        # current user + current user's image
        sql_user=""" 
        SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user_image = cur.fetchone()
        print("---------userimage")
        print(user_image)

    except Exception as ex:
        print("---error:")
        print(ex)

    ## RETURN ###
    if not user:
        print("#"*12)
        print("no match")
        return redirect(f"/login?error=wrong_usercredentials")

    try: 
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        ### COOKIE ###
        encoded_jwt = jwt.encode({"uuid4": user_session_id, "user_email":user_email}, "secret key", algorithm="HS256")
        response.set_cookie("user_email", user_email, secret=g.COOKIE_SECRET)
        response.set_cookie("encoded_jwt", encoded_jwt)
        response.set_cookie("uuid4", user_session_id)
        # g.SESSIONS.append(user_session_id)

        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output

        #### sessions
        sql_session= """ 
        INSERT INTO sessions (session_id, session_user_email, session_created_at) 
        VALUES (%s,%s,%s)  
        """
        val_session = (user_session_id, user_email, user_created_at)
        cur.execute(sql_session, val_session)
        print("Session is added")

        db.commit()
    except Exception as ex:
        print("---error:")
        print(ex)
    finally:
        db.close()


    user_password = user_password.lower() # lowercase Adminpassword string
    if user_email == "admin@admin.com" and user_password == "adminpassword":
        print("-----admin")
        return redirect("/index_admin")
    if user:
        if not user_image:
            redirect("/profile_image")
        else:
            redirect("index_loggedin")
   

  
