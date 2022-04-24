# from urllib import response
from bottle import get, view, request, redirect, response, post
import g
import pymysql
import uuid
import time 
import jwt


##############################
@post("/user_update")
@view("settings")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

    ### DEFINE THE VARIABLES ###
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    user_id = request.forms.get("user_id")
    user_session_id = str(uuid.uuid4())
    user_created_at = str(int(time.time()))
    user_first_name_update = request.forms.get("user_first_name")
    user_last_name_update = request.forms.get("user_last_name")
    user_nick_name_update = request.forms.get("user_nick_name")
    user_email_update = request.forms.get("user_email")
    user_password_update = request.forms.get("user_password")
    
    ### VALIDATE ###
    user_id, error_id = g._is_uuid4(user_id)
    if error_id : return g._send(400, error_id)
    user_session_id, error_sessionid = g._is_uuid4(user_session_id)
    if error_sessionid : return g._send(400, error_sessionid)
    user_first_name_update, error_fn = g._is_item_textshort(user_first_name_update)
    if error_fn : return g._send(400, error_fn)
    user_last_name_update, error_ln = g._is_item_textshort(user_last_name_update)
    if error_ln : return g._send(400, error_ln)
    user_nick_name_update, error_nn = g._is_item_textmedium(user_nick_name_update)
    if error_nn : return g._send(400, error_nn)
    user_email_update, error_e = g._is_item_email(user_email_update)
    if error_e : return g._send(400, error_e)
    user_password_update, error_pw = g._is_item_textlong(user_password_update)
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
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        # db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        # cur = db.cursor()

        #### sessions
        sql_session= """ 
        INSERT INTO sessions (session_id, session_user_email, session_created_at) 
        VALUES (%s,%s,%s)  
        """
        val_session = (user_session_id, user_email,user_created_at )
        cur.execute(sql_session, val_session)

        ##### update user
        sql_user_update=""" 
            UPDATE users 
            SET user_first_name =%s,
            user_last_name =%s,
            user_nick_name =%s,
            user_email =%s,
            user_password =%s
            WHERE user_id=%s
            """   

        var = (user_first_name_update, user_last_name_update, user_nick_name_update, user_email_update, user_password_update, user_id)   
        cur.execute(sql_user_update, var)

        ### COOKIE ###
        encoded_jwt = jwt.encode({"uuid4": user_session_id, "user_email":user_email_update}, "secret key", algorithm="HS256")
        response.set_cookie("user_email", user_email_update, secret=g.COOKIE_SECRET)
        response.set_cookie("encoded_jwt", encoded_jwt)

        ##### current user + current user's image
        sql_user=""" SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user = cur.fetchone()

        db.commit()
    except Exception as ex:
        print(ex)
        # return g._send(500, g._errors["en_server_error"])
    finally:
        db.close()
    
    return redirect("/settings")