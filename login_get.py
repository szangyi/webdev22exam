from bottle import get, redirect, request, response, view
import g

##############################
@get("/login")
@view("login")
def _():
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

    success = request.params.get("success")
    error = request.params.get("error")
    user_email = request.params.get("user_email")
    user_password = request.params.get("user_password")
    user_session_id = request.get_cookie("uuid4")

    if user_session_id:
        return redirect("/index_loggedin")

    return dict(
        success=success,
        error=error, 
        user_email=user_email, 
        user_password=user_password
        )