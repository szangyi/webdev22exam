# from urllib import response
from bottle import get, view, request, redirect, response
import g
import pymysql


##############################
@get("/settings")
@view("settings")
def _():
    try:
        ### DEFINE THE VARIABLES ###
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
       
        print(user_email)

        ### VALIDATE ###


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

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
            user_email=user_email,
            user=user,
            tabs=g.TABS_LOGGEDIN,
            people=g.PEOPLE,
            trends=g.TRENDS
            )

    except Exception as ex:
        print(ex)
    finally:
        db.close()