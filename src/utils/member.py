def getNick(member):
    return member.nick if member.nick is not None else member.name
