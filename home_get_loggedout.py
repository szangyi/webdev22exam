from telnetlib import STATUS
from bottle import get, view, request, response, redirect
import g
import pymysql


@get("/index_loggedout")
@view("index_loggedout")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_session_id = request.get_cookie("uuid4")

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

        # tweets + user info + tweet user image
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
        response.status = 200

################ RETURN ################
        return dict(
            tweets=tweets,
            tabs=g.TABS_LOGGEDOUT,
            people=g.PEOPLE,
            trends=g.TRENDS
            )
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()
    


