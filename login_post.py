from bottle import post, request, redirect, response
import re
import uuid
import g
import jwt
import pymysql
import time



##############################
@post("/login")
def _():
    try:
        response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
        ### DEFINE THE VARIABLES ###
        user_email = request.forms.get("user_email")
        user_password = request.forms.get("user_password")    
        user_session_id = str(uuid.uuid4())
        user_created_at = str(int(time.time()))

        print("-------useremail:-------")
        print(user_email)
        print("-------password:-------")
        print(user_password)
       
        ### VALIDATE ###
        # VALIDATE if the form exist, at all inputs!!!!
        # if not re.match(g.REGEX_EMAIL, request.forms.get("user_email")):
        #     return redirect("/login?error=user_email")

        # if len(request.forms.get("user_password")) < 6:
        #   return redirect(f"/login?error=user_password&user_email={user_email}")
        # if len(request.forms.get("user_password")) > 50:
        #   return redirect(f"/login?error=user_password&user_email={user_email}")


        ### COOKIE ###
        encoded_jwt = jwt.encode({"uuid4": user_session_id, "user_email":user_email}, "secret key", algorithm="HS256")
        response.set_cookie("user_email", user_email, secret=g.COOKIE_SECRET)
        response.set_cookie("encoded_jwt", encoded_jwt)
        response.set_cookie("uuid4", user_session_id)
        # g.SESSIONS.append(user_session_id)


        ### CONNECT TO DB AND EXECUTE ###
        db = pymysql.connect(host="localhost", port=8889,user="root",password="root", database="twitter", cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor() #cursorClass in PyMyPy by default generates Dictionary as output

        # current user
        sql = """SELECT * 
        FROM users 
        WHERE user_email =%s 
        AND user_password=%s """
        var = (user_email, user_password)
        cur.execute(sql, var)
        user = cur.fetchone()
        print("################user logeddin")

        # current user + current user's image
        sql_user=""" SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user_image = cur.fetchone()
        print("---------userimage")
        print(user_image)

        # sessions
        sql_session= """ INSERT INTO sessions (session_id, session_user_email, session_created_at) VALUES (%s,%s,%s)  """
        val_session = (user_session_id, user_email,user_created_at )
        cur.execute(sql_session, val_session)
        print("Session is added")



        db.commit()


    except Exception as ex:
        print("---error:")
        # print(type(ex))
        print(ex)
    finally:
        db.close()


   
    ### RETURN ###
    if not user:
        print("#"*12)
        print("no match")
        return redirect("/signup")
        # return redirect(f"/login?error=wrong_usercredentials")
    else:
        if not user_image:
            return redirect("/upload_profile_image")
        else:
            return redirect("index_loggedin")
  
    # return redirect("/signup")
  
