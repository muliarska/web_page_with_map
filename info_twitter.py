import json


def json_to_dictionary(file_name):
    """
    (str) -> dict
    This function converts the json file to a dictionary
    and returns this dictionary.
    """
    f = open(file_name, encoding='utf-8')
    f_dict = json.load(f)
    return f_dict


def analyze_dictionary(name, user_key, f_dict):
    """
    (str, str, dict) -> object (str, int, list or dict, etc.)
    This function accepts the nickname of a friend for whom
    it will return information (name), the key (user_key)
    and a dictionary. The function returns information
    if present and retrieved "No information provided by user"
    if not. If no such key exists, the function returns
    "There is no such key in the file"
    """
    for friend in f_dict["users"]:
        if friend["screen_name"] == name:
            for i in friend:
                if i == user_key:
                    result = friend[user_key]
                    if result != [] and result != "" and result != None:
                        return result
                    else:
                        return "No information provided by user"

            if "url" in friend["entities"]:
                if user_key == "urls":
                    result = friend["entities"]["url"]["urls"]
                    if result != [] and result != "" and result != None:
                        return result
                    else:
                        return "No information provided by user"

                for j in friend["entities"]["url"]["urls"][0]:
                    if j == user_key:
                        result = friend["entities"]["url"]["urls"][0][user_key]
                        if result != [] and result != "" and result != None:
                            return result
                        else:
                            return "No information provided by user"

            for el in friend["status"]:
                if el == user_key:
                    result = friend["status"][el]
                    if result != [] and result != "" and result != None:
                        return result
                    else:
                        return "No information provided by user"

                if el == "entities":
                    for k in friend["status"][el]:
                        if k == user_key:
                            result = friend["status"][el][k]
                            if result != [] and result != "" and result != None:
                                return result
                            else:
                                return "No information provided by user"

    return "There is no such key in the file"
