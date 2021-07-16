from src.utils.member import getNick
def formatCode(ctx, language:str, sourcecode:str):
    return f"""By {getNick(ctx.author)}```{language}\n{sourcecode}\n```"""