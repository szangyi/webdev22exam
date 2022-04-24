from bottle import post, redirect, response, request, view
import time
import pymysql
import g

##############################

@post("/tweet_delete/<tweet_id>")
@view("user_profile")
def _(tweet_id):
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_session_id = request.get_cookie("uuid4")
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    tweet_id = request.forms.get("tweet_id")

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

        sql = """ DELETE FROM tweets 
        WHERE tweet_id=%s
        """
        var = (tweet_id)
        cur.execute(sql, var)

        db.commit()
        print("------------")
        print("tweet is deleted", tweet_id)
        response.status = 201
    except Exception as ex:
        print("------------")
        print("error")
        print(ex)
    finally:
        db.close()

################ RETURN ################
    if user_email == "admin@admin.com":
        return redirect("/index_admin")
    else:
        return redirect("/user_profile_my")