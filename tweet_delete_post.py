from bottle import post, redirect, request, view
import time
from time import gmtime, strftime
import pymysql

##############################

@post("/tweet_delete/<tweet_id>")
@view("user_profile")
def _(tweet_id):
    try:

        ### DEFINE VARIABLES ###
        user_session_id = request.get_cookie("uuid4")

        tweet_id = request.forms.get("tweet_id")

        ### VALIDATE ###
        # if len(tweet_title) < 1:
        #     return redirect(f"tweets?error=tweet_title&tweet_desc={tweet_desc}&tweet_title={tweet_title}")
        # if len(tweet_desc) < 1:
        #     return redirect(f"tweets?error=tweet_desc&tweet_title={tweet_title}&tweet_desc={tweet_desc}")
        

        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output
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
    return redirect("/user_profile")