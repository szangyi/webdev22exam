from bottle import get, view, request, response, redirect
import g
import pymysql


@get("/index_loggedin")
@view("index_loggedin")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    user_session_id = request.get_cookie("uuid4")

################ COOKIE ################
    prev_url = request.url
    response.set_cookie("prev_url", prev_url)


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


        ## tweets + user info + tweet user image + follows
        sql = """
        SELECT * 
        FROM tweets 
        JOIN users
        ON tweets.tweet_user_email = users.user_email
        JOIN users_images
        ON users.user_id = users_images.fk_user_id
        JOIN follows
        ON users.user_email = follows.user_email_receiver
        WHERE user_email_initiator =%s
        AND status = "1"
        ORDER BY tweet_created_at_epoch  DESC
        """
        cur.execute(sql, (user_email,))
        tweets = cur.fetchall() 
        print("tweets")
        print(tweets)
        tweets_length = len([el for el in tweets])
        print("tweets couuuunnt")
        print(tweets_length)
        # print("---------tweets")
        # print(tweets)
        
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
        # print("---------user")
        # print(user)

        ## people to follow
        sql_people = """
        SELECT * FROM users
        WHERE user_email NOT IN
	        (SELECT user_email_receiver 
            FROM follows
            WHERE status = 1)
        AND user_email != "admin@admin.com"
        ORDER BY RAND()
        LIMIT 3
        """
        cur.execute(sql_people)
        people = cur.fetchall()
        print("people to follow:")
        print(people)


        db.commit()
        response.status = 200

################ RETURN ################
        return dict(
            tweets=tweets,
            user=user,
            tweets_length=tweets_length,
            tabs=g.TABS_LOGGEDIN,
            people=people,
            trends=g.TRENDS,
            )
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()