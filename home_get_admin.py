from bottle import get, view, request, response, redirect
import g
import pymysql

## lot to fix here, but first lets work on the tweet post
##############################




@get("/index_admin")
@view("index_admin")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    # error = request.params.get("error")
    try:
        ### DEFINE THE VARIABLES ###
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
        # print("----useremail")
        # print(user_email)
        user_session_id = request.get_cookie("uuid4")
        # tweet_text = request.forms.get("tweet_text")

        ### VALIDATE ###


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() 

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
        ### RETURN ###
        ##add error to dict
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
    finally:
        db.close()
    


