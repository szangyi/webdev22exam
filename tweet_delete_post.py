from bottle import post, redirect, request, view
import time
import pymysql
import g

##############################

@post("/tweet_delete/<tweet_id>")
@view("user_profile")
def _(tweet_id):
    try:
        ### DEFINE VARIABLES ###
        user_session_id = request.get_cookie("uuid4")
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
        tweet_id = request.forms.get("tweet_id")

        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        sql = """ DELETE FROM tweets 
        WHERE tweet_id=%s
        """
        var = (tweet_id)
        cur.execute(sql, var)

        db.commit()
        print("------------")
        print("tweet is deleted", tweet_id)
        # response.status = 201
        
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()
    
    if user_email == "admin@admin.com":
        return redirect("/index_admin")
    else:
        return redirect("/user_profile_my")