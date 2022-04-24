# from urllib import response
from bottle import get, view, request, redirect, response
import g
import pymysql


##############################
@get("/user_profile_any")
@view("user_profile_any")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    user_any_email = request.params.get("user_any_email")
    user_session_id = request.get_cookie("uuid4")
    print(user_any_email)

    if user_email == user_any_email:
        return redirect("/user_profile_my")
    
    if not user_session_id:
        return redirect("/login")

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

        ## tweets by user
        sql = """SELECT * 
        FROM tweets 
        JOIN users
        WHERE tweets.tweet_user_email = users.user_email
        AND users.user_email = %s
        ORDER BY tweet_created_at  DESC
        """
        cur.execute(sql, (user_any_email,))
        tweets = cur.fetchall() 

        ## current user + current user's image
        sql_user=""" SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user = cur.fetchone()

        ## any user + current any's image
        sql_user_any=""" SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user_any, (user_any_email,))
        user_any = cur.fetchone()

        db.commit()
        
################ RETURN ################
        return dict(
            tweets=tweets,
            user=user,
            user_any=user_any,
            user_email=user_email,
            user_any_email=user_any_email,
            tabs=g.TABS_LOGGEDIN,
            people=g.PEOPLE,
            trends=g.TRENDS
            )
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()