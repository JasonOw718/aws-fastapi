
def individual_serial(Conversation) ->dict:
    return {
        "id":str(Conversation["_id"]),
        "messages":Conversation["messages"]
    }
    
def list_serial(Conversations) ->list:
    return [individual_serial(Conversation) for Conversation in Conversations]