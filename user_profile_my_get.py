# from urllib import response
from bottle import get, view, request, redirect, response
import g
import pymysql


##############################
@get("/user_profile_my")
@view("user_profile_my")
def _():
    try:
        ### DEFINE THE VARIABLES ###
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)

        ### VALIDATE ###


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        # sql_user=""" SELECT * FROM users WHERE user_email =%s"""
        # cur.execute(sql_user, (user_email,))
        # user = cur.fetchone()
        # print("---------user")
        # print(user)

        ##### tweets by user
        sql = """SELECT * 
        FROM tweets 
        JOIN users
        WHERE tweets.tweet_user_email = users.user_email
        AND users.user_email = %s
        ORDER BY tweet_created_at  DESC
        """
        cur.execute(sql, (user_email,))
        tweets = cur.fetchall() 

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
        
        return dict(
            tweets=tweets,
            user=user,
            user_email=user_email,
            tabs=g.TABS_LOGGEDIN,
            people=g.PEOPLE,
            trends=g.TRENDS
            )

    except Exception as ex:
        print(ex)
    finally:
        db.close()