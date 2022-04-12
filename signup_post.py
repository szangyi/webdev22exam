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
    
        
        # return redirect(f"signup-ok?user-firstname={user_first_name}&user-lastname={user_last_name}&user-email={user_email}&user-password={user_password}")


        ### VALIDATE ###

        # if not request.forms.get("user_name"):
        #   return redirect(f"/signup?error=user_name")
        # user_name = request.forms.get("user_name")
        # if not request.forms.get("user_lastname"):
        #   return redirect(f"/signup?error=user_lastname&user_name={user_name}")
        # user_lastname = request.forms.get("user_lastname")
        # if not request.forms.get("user_email"):
        #   return redirect(f"/signup?error=user_email&user_name={user_name}&user_lastname={user_lastname}")
        # user_email = request.forms.get("user_email")
        # if not request.forms.get("user_password"):
        #   return redirect(f"/signup?error=user_password&user_name={user_name}&user_lastname={user_lastname}&user_email={user_email}")
        # user_password = request.forms.get("user_password")


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
        print(type(ex))
        print(ex)
    finally:
        db.close()

    return redirect("/login")

  