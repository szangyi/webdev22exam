# from urllib import response
from bottle import get, view, request, redirect, response
import g
import pymysql


##############################
@get("/settings")
@view("settings")
def _():
    # url = format(request.url)
    # print("url:")
    # print(url)

################ DEFINE THE VARIABLES ################
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_email = request.get_cookie("user_email", secret=g.COOKIE_SECRET)
    error = request.params.get("error")

################ COOKIE ################
    prev_url = request.url
    response.set_cookie("prev_url", prev_url)

    user_session_id = request.get_cookie("uuid4")
    if user_session_id is None:
        redirect("/login")

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

        ## current user + current user's image
        sql_user=""" SELECT * 
        FROM users
        JOIN users_images
        WHERE user_email =%s
        AND users.user_id = users_images.fk_user_id
        """
        cur.execute(sql_user, (user_email,))
        user = cur.fetchone()

        ## people to follow
        sql_people = """
        SELECT * FROM users
        WHERE user_email NOT IN
	        (SELECT user_email_receiver 
            FROM follows
            WHERE status = 1
            AND user_email_initiator=%s)
        AND user_email != "admin@admin.com"
        ORDER BY RAND()
        LIMIT 3
        """
        cur.execute(sql_people, (user_email,))
        cur.execute(sql_people)
        people = cur.fetchall()


        db.commit()

################ RETURN ################
        return dict(
            error=error,
            user_email=user_email,
            user=user,
            tabs=g.TABS_LOGGEDIN,
            people=people,
            trends=g.TRENDS
            )
    except Exception as ex:
        print(ex)
        response.status = 500
    finally:
        db.close()