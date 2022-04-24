from bottle import post, redirect, request, view, response
import g
import uuid
import time
from time import gmtime, strftime
import pymysql

##############################
@post("/tweet_add")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_session_id = request.get_cookie("uuid4")
    tweet_id = str(uuid.uuid4())  
    tweet_text = request.forms.get("tweet_text")
    tweet_created_at = strftime("%a, %d %b %Y %H:%M", gmtime())
    tweet_updated_at = strftime("%a, %d %b %Y %H:%M", gmtime())
    tweet_user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)

################ VALIDATE ################
    tweet_text, error = g._is_item_tweet(tweet_text)
    if error : 
        print("ERROR")
        return g._send(400, error)

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
        INSERT INTO tweets (tweet_id, tweet_text, tweet_created_at, tweet_updated_at, tweet_user_email ) 
        VALUES (%s, %s, %s, %s, %s)
        """
        var = (tweet_id, tweet_text, tweet_created_at, tweet_updated_at, tweet_user_email)
        cur.execute(sql, var)
        db.commit()
        print("tweet created successfully")
        response.status = 201
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()
    
################ RETURN ################
    return redirect("/index_loggedin")