from bottle import get, view, request, response, redirect
import g
import pymysql


@get("/index_loggedin")
@view("index_loggedin")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    ### DEFINE THE VARIABLES ###
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    user_session_id = request.get_cookie("uuid4")

    ### VALIDATE ###

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
        # cur = db.cursor() 

        sql_sessions=""" 
        SELECT * 
        FROM sessions 
        WHERE session_id =%s"""
        cur.execute(sql_sessions, (user_session_id,))
        session = cur.fetchone()
        print(session)

        ## tweets + user info + tweet user image
        sql = """
        SELECT * 
        FROM tweets 
        JOIN users
        ON tweets.tweet_user_email = users.user_email
        JOIN users_images
        ON users.user_id = users_images.fk_user_id
        ORDER BY tweet_created_at  DESC
        """
        cur.execute(sql)
        tweets = cur.fetchall() 
        print("---------tweets")
        print(tweets)
        
        ## current user + current user's image
        sql_user="""
        SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user = cur.fetchone()
        print("---------user")
        print(user)


        db.commit()

    except Exception as ex:
        print(ex)
    finally:
        db.close()

    ### RETURN ###
    return dict(
        tweets=tweets,
        user=user,
        tabs=g.TABS_LOGGEDIN,
        people=g.PEOPLE,
        trends=g.TRENDS
        )

