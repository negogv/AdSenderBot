import json
import os
from typing import List

data_path = os.path.join(os.path.dirname(__file__), 'result.json')

def get_all_chats() -> List[int]:
    """
    Returns all chats listed in exported-acc-data/result.json as a list of integers.

    Returns:
        List[int]: list of chat IDs
    """
    with open(data_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        chat_ids = [int(chat["id"]) for chat in data["chats"]["list"]]
        return chat_ids


""" 
--------------------------------------------------------------------------------
                This fucker crushes all the code
--------------------------------------------------------------------------------
            {
                "name": "Praha Best Party 1",
                "type": "public_supergroup",
                "id": 2358621536
            },
--------------------------------------------------------------------------------
            

"""