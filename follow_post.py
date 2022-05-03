from bottle import post, redirect, request, view, response
import g
import uuid
import time
from time import gmtime, strftime
from datetime import datetime
import pymysql

##############################
@post("/follow")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    follow_id = str(uuid.uuid4())  
    user_email_initiator = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    user_email_receiver = request.forms.get("user_email_receiver")
    user_session_id = request.get_cookie("uuid4")
    prev_url = request.get_cookie("prev_url")

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

        sql = """
        INSERT INTO follows (follow_id, user_email_initiator, user_email_receiver, status) 
        VALUES (%s, %s, %s, 1)
        """
        var = (follow_id, user_email_initiator, user_email_receiver)
        cur.execute(sql, var)
        db.commit()
        print("new follow")
        response.status = 201
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()
    
################ RETURN ################
    return redirect(prev_url)