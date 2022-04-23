from bottle import get, request, view, response
import g
import pymysql


##############################
@get("/profile_image")
@view("profile_image_upload")
def _():
    try:
        ### DEFINE THE VARIABLES ###
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
        error = request.params.get("error")


        ### VALIDATE ###

        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        sql_user=""" SELECT * FROM users WHERE user_email =%s"""
        cur.execute(sql_user, (user_email,))
        db.commit()
        user = cur.fetchone()
        print("---------user")
        print(user)



        return dict(
            user=user,
            error=error
        )


    except Exception as ex:
        print(ex)
    finally:
        db.close()