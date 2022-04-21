from bottle import get, request, view


##############################
@get("/signup")
@view("signup")
def _():
  error = request.params.get("error")
  user_first_name = request.params.get("user_first_name")
  user_last_name = request.params.get("user_last_name")
  user_nick_name = request.params.get("user_nick_name")
  user_email = request.params.get("user_email")
  user_password = request.params.get("user_password")
  return dict(
    error=error, 
    user_first_name=user_first_name,
    user_last_name=user_last_name,
    user_nick_name=user_nick_name,
    user_email=user_email,
    user_password=user_password
    )
  
