from bottle import post, redirect, request, view
import time
from time import gmtime, strftime
import g
import pymysql

##############################

@post("/tweet_update/<tweet_id>")
@view("user_profile")
def _(tweet_id):
    ### DEFINE VARIABLES ###
    user_session_id = request.get_cookie("uuid4")
    tweet_id = request.forms.get("tweet_id")
    tweet_text_update = request.forms.get("tweet_text")
    tweet_created_at = request.forms.get("tweet_created_at")
    tweet_updated_at = strftime("%a, %d %b %Y %H:%M", gmtime())
    tweet_user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)

    ### VALIDATE ###
    tweet_text, error = g._is_item_tweet(request.forms.get("tweet_text"))
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
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        # db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        # cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output

        sql = """ 
            UPDATE tweets 
            SET tweet_text =%s,
            tweet_updated_at =%s
            WHERE tweet_id=%s
            """       

        var = (tweet_text_update, tweet_updated_at, tweet_id)
        cur.execute(sql, var)
        db.commit()
        # response.status = 201
        
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()
    return redirect("/user_profile_my")