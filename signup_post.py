from bottle import post, request, redirect
import uuid
import re
import g
import time
from time import gmtime, strftime
import pymysql

##############################
@post("/signup")
def _():
    try:
        
        user_first_name, error = g._is_item_name(request.forms.get("user_first_name"))
        if error : return g._send(400, error)

        ### DEFINE VARIABLES ###
        user_id = str(uuid.uuid4())
        user_first_name = request.forms.get("user_first_name")
        user_last_name = request.forms.get("user_last_name")
        user_nick_name = request.forms.get("user_nick_name")
        user_email = request.forms.get("user_email")
        user_password = request.forms.get("user_password")
        user_created_at = strftime("%a, %d %b %Y %H:%M", gmtime())

        user = {
        "user_id":user_id, 
        "user_first_name":user_first_name, 
        "user_last_name":user_last_name, 
        "user_nick_name":user_nick_name, 
        "user_email":user_email,
        "user_password":user_password,
        "user_created_at":user_created_at
        }

        print("user:")
        print(user)
        return redirect("/login")
    except Exception as ex:
        print(ex)


        ### VALIDATE ###
    # if not user_first_name:
    #     return redirect(f"/signup?error=user_first_name&user_last_name={user_last_name or ''}&user_nick_name={user_nick_name or ''}&user_email={user_email or ''}")
    # if not user_last_name:
    #     return redirect(f"/signup?error=user_last_name&user_first_name={user_first_name or ''}&user_nick_name={user_nick_name or ''}&user_email={user_email or ''}")
    # if not user_nick_name:
    #     return redirect(f"/signup?error=user_nick_name&user_first_name={user_first_name or ''}&user_last_name={user_last_name or ''}&user_email={user_email or ''}")
    # if not user_email:
    #     return redirect(f"/signup?error=user_email&user_first_name={user_first_name or ''}&user_last_name={user_last_name or ''}&user_nick_name={user_nick_name or ''}")
    # if not user_password:
    #     return redirect(f"/signup?error=user_password&user_name={user_first_name or ''}&user_last_name={user_last_name or ''}&user_nick_name={user_nick_name or ''}&user_email={user_email or ''}")


    try: 
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output
        sql = """INSERT INTO users (user_id, user_first_name, user_last_name, user_nick_name, user_email, user_password, user_created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        var = (user_id, user_first_name, user_last_name, user_nick_name, user_email, user_password, user_created_at)
        
        cur.execute(sql, var)
        db.commit()
        print("user created successfully", user)
    except Exception as ex:
        print(ex)
    finally:
        db.close()

    

  