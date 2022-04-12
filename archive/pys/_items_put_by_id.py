from bottle import put, request
import x
import time
from datetime import datetime

##############################
@put("/items/<item_id>")
@put("/<language>/items/<item_id>")
def _(language="en", item_id=""):

  allowed_keys = ["item_name", "item_price"]
  errors = {
    "en":f"Only posible to update: {allowed_keys}", 
    "dk":f"Der kan kun opdateres: {allowed_keys}",
    "sp":f"Solo se puede actualizar: {allowed_keys}",
  }
  new_item = {}
  query_set_parts = []

  # VALIDATE
  try:
    
    # Maybe the user enters a language that is not supported, then default to english
    # Use any key to see if the language is in the errors dictionary
    if f"{language}_server_error" not in x._errors : language = "en"

    # The user has not passed any keys, inform about the keys allowed
    if not request.forms.keys(): return x._send(400, errors[f"{language}"])

    # Validate the item_id
    item_id, error = x._is_uuid4(item_id, language)
    if error : return x._send(400, error)      
    new_item["item_id"] = item_id

    # Check that only allowed keys are passed from the client
    for key in request.forms.keys():
      if not key in allowed_keys:
        print(key)
        return x._send(400, errors[f"{language}"])

    # Validate each allowed key (if given by the client)
    if request.forms.get("item_name"):
      item_name, error = x._is_item_name(request.forms.get("item_name"), language)
      if error: return x._send(400, error)
      query_set_parts.append("item_name = :item_name")
      new_item["item_name"] = item_name

    if request.forms.get("item_price"):
      item_price, error = x._is_item_price(request.forms.get("item_price"), language)
      if error: return x._send(400, error)
      query_set_parts.append("item_price = :item_price")
      new_item["item_price"] = item_price

  except Exception as ex:
    print(ex)
    return x._send(500, x._errors[f"{language}_server_error"])

  try:
    # Get the item to overwrite it with new data
    db = x._db_connect("database.sqlite")
    
    # Update the field
    item_updated_at = str(int(time.time()))
    query_set_parts.append("item_updated_at = :item_updated_at")
    new_item["item_updated_at"] = item_updated_at

    now = datetime.now()
    item_updated_at_date = now.strftime("%Y-%B-%d-%A %H:%M:%S")
    query_set_parts.append("item_updated_at_date = :item_updated_at_date")
    new_item["item_updated_at_date"] = item_updated_at_date

    # Convert the parts of the query to a string to be used in the whole query
    set_query = query_set_parts = ",".join(query_set_parts)
    print(set_query)
    # Save the item with its updated values
    counter = db.execute(f"""UPDATE items 
                  SET {set_query}
                  WHERE item_id = :item_id""", new_item).rowcount
    db.commit()
    if not counter : return x._send(204, "")
    return new_item
  except Exception as ex:
    print(ex)
    return x._send(500, x._errors[f"{language}_server_error"])
  finally:
    db.close()

  






