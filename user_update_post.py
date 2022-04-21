# from urllib import response
from bottle import get, view, request, redirect, response, post
import g
import pymysql


##############################
@post("/settings")
@view("settings")
def _():
    try:
        ### DEFINE THE VARIABLES ###
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
       
        print(user_email)

        user_first_name_update = request.forms.get("user_first_name")
        user_last_name_update = request.forms.get("user_last_name")

        ### VALIDATE ###


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

        ##### update user
        sql_user_update=""" 
            UPDATE users 
            SET user_first_name =%s,
            user_last_name =%s
            WHERE user_email=%s
            """   

        var = (user_first_name_update, user_last_name_update, user_email)   
        cur.execute(sql_user_update, var)


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
    return redirect("/settings")