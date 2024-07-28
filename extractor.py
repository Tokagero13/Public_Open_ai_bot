# extractor.py

def extract_variables(data):
    update_id = data["update_id"]

    message = data["message"]
    message_id = message["message_id"]

    from_user = message["from"]
    from_user_id = from_user["id"]
    from_user_is_bot = from_user["is_bot"]
    from_user_first_name = from_user["first_name"]
    from_user_username = from_user["username"]
    from_user_language_code = from_user["language_code"]

    chat = message["chat"]
    chat_id = chat["id"]
    chat_first_name = chat["first_name"]
    chat_username = chat["username"]
    chat_type = chat["type"]

    message_date = message["date"]
    message_text = message["text"]

    return {
        "update_id": update_id,
        "message_id": message_id,
        "from_user_id": from_user_id,
        "from_user_is_bot": from_user_is_bot,
        "from_user_first_name": from_user_first_name,
        "from_user_username": from_user_username,
        "from_user_language_code": from_user_language_code,
        "chat_id": chat_id,
        "chat_first_name": chat_first_name,
        "chat_username": chat_username,
        "chat_type": chat_type,
        "message_date": message_date,
        "message_text": message_text,
    }
