from bottle import get, view, request, response, redirect
import g
import pymysql

## lot to fix here, but first lets work on the tweet post
##############################




@get("/index")
# @view("index_loggedin")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_session_id = request.get_cookie("uuid4")
    if not user_session_id:
        print("---NOOOT loggedin")
        return redirect("/index_loggedout")
    else:
        print("---loggedin")
        return redirect("/index_loggedin")

