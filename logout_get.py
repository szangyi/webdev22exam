from bottle import get, request, redirect, response
import g
import pymysql

##############################

@get("/logout")
def _(): 
    ### DEFINE THE VARIABLES ###
    user_session_id = request.get_cookie("uuid4")

    try:
        print("production mode")
        import production
        db_config = {
        "host":"szangyi.mysql.eu.pythonanywhere-services.com", 
        "user":"szangyi", 
        "password":"sedHuq-piwdyh-xergy9", 
        "database":"szangyi$twitter", 
        "cursorclass":pymysql.cursors.DictCursor
        }

    except Exception as ex:
        print("development mode")
        print(ex)
        db_config = {
        "host":"localhost", 
        "port":8889,
        "user":"root", 
        "password":"root", 
        "database":"twitter", 
        "cursorclass":pymysql.cursors.DictCursor
        }

    try:
        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        # db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        # cur = db.cursor() 

        sql=""" DELETE FROM sessions WHERE session_id =%s"""
        cur.execute(sql, (user_session_id,))
        db.commit()
        print("session is deleted", user_session_id)
    
        # Delete the cookies from the browser
        response.set_cookie("uuid4", "", expires=0)
        response.set_cookie("user_email", "", expires=0)
        response.set_cookie("encoded_jwt", "", expires=0)
    except Exception as ex:
        print("---error:")
        # print(type(ex))
        print(ex)
    finally:
        db.close()
    ### RETURN ###
    return redirect("/login")