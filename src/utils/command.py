def fetchArguments(msg):

    if msg == None:
        return None, None


    msgsplit = msg.split('-')

    if msg.startswith('-'):
        return None, msgsplit[0]

    elif '-' in msg:
        return msgsplit[0], msgsplit[1:]
        
    else:
        return msg, None