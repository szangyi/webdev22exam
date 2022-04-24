from bottle import get, request, response, redirect, view
import g
import pymysql


@get("/")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    user_session_id = request.get_cookie("uuid4")
    
    if not user_session_id:
        return redirect("/index_loggedout")
    else:
        return redirect("/index_loggedin")

