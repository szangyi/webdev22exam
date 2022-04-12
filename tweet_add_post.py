from bottle import post, redirect, request, view, response
import g
import uuid
import time
from time import gmtime, strftime
import pymysql

##############################
@post("/tweet_add")
# @view("index")
def _():
    try:

        ### DEFINE VARIABLES ###
        user_session_id = request.get_cookie("uuid4")
        tweet_id = str(uuid.uuid4())  
        tweet_text = request.forms.get("tweet_text")
        # tweet_created_at = str(int(time.time()))
        # tweet_updated_at = str(int(time.time()))
        tweet_created_at = strftime("%a, %d %b %Y %H:%M", gmtime())
        tweet_updated_at = strftime("%a, %d %b %Y %H:%M", gmtime())
        tweet_user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)

  
        # user_session_id = request.get_cookie("user_session_id")


        tweet = {
            "tweet_id" : tweet_id, 
            "tweet_text" : tweet_text,
            "tweet_created_at": tweet_created_at,
            "tweet_updated_at": tweet_updated_at,
            "tweet_user_email": tweet_user_email,
            # "iat" : strftime("%a, %d %b %Y %H:%M", gmtime())
            }


        ### VALIDATE ###
        # if len(tweet_title) < 1:
        #     return redirect(f"tweets?error=tweet_title&tweet_desc={tweet_desc}&tweet_title={tweet_title}")
        # if len(tweet_desc) < 1:
        #     return redirect(f"tweets?error=tweet_desc&tweet_title={tweet_title}&tweet_desc={tweet_desc}")
        

        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output
        sql = """INSERT INTO tweets (tweet_id, tweet_text, tweet_created_at, tweet_updated_at, tweet_user_email ) VALUES (%s, %s, %s, %s, %s)"""
        var = (tweet_id, tweet_text, tweet_created_at, tweet_updated_at, tweet_user_email)
        cur.execute(sql, var)
        db.commit()
        print("------------")
        print("tweet created successfully")
        print(tweet)
        response.status = 201
        
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()
    return redirect("/index_loggedin")

    ###################### RETURN ########################
    # if session is None:
    #     return redirect("/login")

    