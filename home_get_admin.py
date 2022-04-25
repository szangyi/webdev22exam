from bottle import get, view, request, response, redirect
import g
import pymysql


@get("/index_admin")
@view("index_admin")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
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

        ## tweets + user info + tweet user image
        sql = """
        SELECT * 
        FROM tweets 
        JOIN users
        ON tweets.tweet_user_email = users.user_email
        JOIN users_images
        ON users.user_id = users_images.fk_user_id
        ORDER BY tweet_created_at_epoch  DESC
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

        db.commit()
        response.status = 200

################ RETURN ################
        return dict(
            tweets=tweets,
            user=user,
            user_email=user_email,
            tabs=g.TABS_ADMIN,
            people=g.PEOPLE,
            trends=g.TRENDS
            )
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()
    


