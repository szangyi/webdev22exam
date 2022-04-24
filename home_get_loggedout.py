from telnetlib import STATUS
from bottle import get, view, request, response, redirect
import g
import pymysql

## lot to fix here, but first lets work on the tweet post
##############################




@get("/index_loggedout")
@view("index_loggedout")
def _():
    ### DEFINE THE VARIABLES ###
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_session_id = request.get_cookie("uuid4")
    print("--usersession cookie")
    print(user_session_id)
    print("*******not logged in")

    # try:
    #     print("production mode")
    #     import production
    #     db_config = {
    #     "host":"szangyi.mysql.eu.pythonanywhere-services.com", 
    #     "user":"szangyi", 
    #     "password":"sedHuq-piwdyh-xergy9", 
    #     "database":"szangyi$twitter", 
    #     "cursorclass":pymysql.cursors.DictCursor
    #     }

    # except Exception as ex:
    #     print("development mode")
    #     print(ex)
    #     db_config = {
    #     "host":"localhost", 
    #     "port":8889,
    #     "user":"root", 
    #     "password":"root", 
    #     "database":"twitter", 
    #     "cursorclass":pymysql.cursors.DictCursor
    #     }



    try:
        print("production mode")
        import production
        db_config = g.DB_PROD

    except Exception as ex:
        print("development mode")
        print(ex)
        db_config = g.DB_dev

    try:
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        # tweets + user info + tweet user image
        # db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        # cur = db.cursor() 
        sql_tweets = """SELECT * 
        FROM tweets 
        JOIN users
        ON tweets.tweet_user_email = users.user_email
        JOIN users_images
        ON users.user_id = users_images.fk_user_id
        ORDER BY tweet_created_at  DESC
        """
        cur.execute(sql_tweets)
        tweets = cur.fetchall() 
    
        db.commit()

        ### RETURN ###
        return dict(
            tweets=tweets,
            tabs=g.TABS_LOGGEDOUT,
            people=g.PEOPLE,
            trends=g.TRENDS
            )
    except Exception as ex:
        print(ex)
    finally:
        db.close()

    


