from bottle import get, request, response, redirect, view
import g
import pymysql


##############################
@get("/profile_image")
@view("profile_image_upload")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    error = request.params.get("error")
    user_session_id = request.get_cookie("uuid4")

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

        sql_user=""" SELECT * FROM users WHERE user_email =%s"""
        cur.execute(sql_user, (user_email,))
        db.commit()
        user = cur.fetchone()
        print("---------user")
        print(user)

################ RETURN ################
        return dict(
            user=user,
            error=error
        )
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()