from bottle import get, request, view, response
import g
import pymysql


##############################
@get("/profile_image")
@view("profile_image_upload")
def _():
    ### DEFINE THE VARIABLES ###
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    error = request.params.get("error")

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