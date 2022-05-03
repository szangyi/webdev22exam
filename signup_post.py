from bottle import post, request, response, redirect
import uuid
import re
import g
import time
from time import gmtime, strftime
import pymysql

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@post("/signup")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

################ DEFINE THE VARIABLES ################
    user_id = str(uuid.uuid4())
    follow_id = str(uuid.uuid4())
    user_first_name = request.forms.get("user_first_name")
    user_last_name = request.forms.get("user_last_name")
    user_nick_name = request.forms.get("user_nick_name")
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")
    user_total_tweets = "0"
    user_created_at_epoch = str(int(time.time()))
    user_created_at = strftime("%a, %d %b %Y %H:%M", gmtime())


################ VALIDATE ################
    user_id, error_id = g._is_uuid4(user_id)
    if error_id : return g._send(400, error_id)
    follow_id, error_f_id = g._is_uuid4(follow_id)
    if error_f_id : return g._send(400, error_f_id)
    user_first_name, error_fn = g._is_item_textshort(user_first_name)
    if error_fn : return g._send(400, error_fn)
    user_last_name, error_ln = g._is_item_textshort(user_last_name)
    if error_ln : return g._send(400, error_ln)
    user_nick_name, error_nn = g._is_item_textmedium(user_nick_name)
    if error_nn : return g._send(400, error_nn)
    user_email, error_e = g._is_item_email(user_email)
    if error_e : return g._send(400, error_e)
    user_password, error_pw = g._is_item_textlong(user_password)
    if error_pw : return g._send(400, error_pw)

    try:
        print("production mode")
        import production
        db_config = g.DB_PROD

    except Exception as ex:
        print("development mode")
        print(ex)
        db_config = g.DB_DEV

        ### EMAIL - only in development mode ###
        sender_email = "szangyiwebdev@gmail.com"
        receiver_email = user_email
        # password = g.EMAIL_PW
        password = g.APP_PW

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your new Tweeter account"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = """\
        Hey,

        Thank you for creating an account on Twetter.
        Enjoy!
        Tweeter
        """

        html = """\
        <html>
            <body>
            <p>
                Hey,<br>
                Thank you for creating an account on Twetter.
                <h2>Enjoy!</h2>
                <em>Twetter</em>
            </p>
            </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as ex:
                print("-----error")
                print(ex) 

    try:
################ CONNECT TO DB AND EXECUTE ################
        db = pymysql.connect(**db_config)
        cur = db.cursor()

        sql = """INSERT INTO users (user_id, user_first_name, user_last_name, user_nick_name, user_email, user_password, user_total_tweets, user_created_at_epoch, user_created_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        var = (user_id, user_first_name, user_last_name, user_nick_name, user_email, user_password, user_total_tweets, user_created_at_epoch, user_created_at)
        cur.execute(sql, var)
        print("user created successfully") 

        sql_follow = """
        INSERT INTO follows (follow_id, user_email_initiator, user_email_receiver, status) 
        VALUES (%s, %s, %s, 1)
        """
        var = (follow_id, user_email, user_email)
        cur.execute(sql_follow, var)


        db.commit()
    except Exception as ex:
        print("error:")
        print(ex)
        response.status = 500
    finally:
        db.close()
    return redirect("/login?success=signup_success")
    

  