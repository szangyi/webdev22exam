from bottle import get, request, view


##############################
@get("/signup")
@view("signup")
def _():
  error = request.params.get("error")
  user_email = request.params.get("user_email")
  user_name = request.params.get("user_email")
  user_lastname = request.params.get("user_email")
  user_password = request.params.get("user_password")
  return dict(error=error, user_email=user_email, user_password=user_password, user_name=user_name, user_lastname=user_lastname)
  
