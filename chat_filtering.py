# s = ':kegoatedx!kegoatedx@kegoatedx.tmi.twitch.tv PRIVMSG #symfuhny :!accountage'

def message_filter(s):

    message = s.split(":")[-1]
    name = s.split("!")[0]
    name1 = name.replace(":", "")
    return name1 + ": " + message
