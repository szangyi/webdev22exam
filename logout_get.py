from bottle import get, request, redirect, response
import g
import pymysql

##############################

@get("/logout")
def _(): 
################ DEFINE THE VARIABLES ################
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

        sql=""" 
        DELETE FROM sessions 
        WHERE session_id =%s"""
        cur.execute(sql, (user_session_id,))
        db.commit()
        print("session is deleted", user_session_id)
    
        ## delete the cookies from the browser
        response.set_cookie("uuid4", "", expires=0)
        response.set_cookie("user_email", "", expires=0)
        response.set_cookie("encoded_jwt", "", expires=0)
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()

################ RETURN ################
    return redirect("/login")