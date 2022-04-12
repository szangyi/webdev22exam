# from urllib import response
from bottle import get, view, request, redirect, response
import g
import pymysql


##############################
@get("/user_profile")
@view("user_profile")
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




# @get("/index")
# @view("index")
# def _():
#     response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
#     # error = request.params.get("error")
#     try:
#         ### DEFINE THE VARIABLES ###
#         # user_first_name = request.get_cookie("user_first_name", secret=g.COOKIE_SECRET)
#         # print("----userfirstname")
#         # print(user_first_name)
#         # user_last_name = request.get_cookie("user_last_name", secret=g.COOKIE_SECRET)
#         # user_nick_name = request.get_cookie("user_nick_name", secret=g.COOKIE_SECRET)
#         user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
#         print("----useremail")
#         print(user_email)
#         # user_session_id = request.get_cookie("uuid4")
#         tweet_text = request.forms.get("tweet_text")


#         ### VALIDATE ###


#         ### CONNECT TO DB AND EXECUTE ###
#         db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
#         # cur = db.cursor(buffered=True) #cursorClass in PyMyPy by default generates Dictionary as output
#         cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output
#         sql = """SELECT * FROM tweets WHERE tweet_user_email =%s """
#         cur.execute(sql, (user_email))
#         tweets = cur.fetchall() 
#         db.commit()
#         print("tweets are there")
#     except Exception as ex:
#         print(ex)
#     finally:
#         db.close()
    

#     ### RETURN ###
#     ##add error to dict
#     return dict(
#         # user_first_name=user_first_name,
#         # user_last_name=user_last_name,
#         # user_nick_name=user_nick_name,
#         user_email=user_email,
#         tweet_text=tweet_text,
#         tweets=tweets,
#         )