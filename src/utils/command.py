from discord_slash.utils.manage_commands import create_option, create_choice
from src.utils.config import MP3_files


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


class SlashChoice:
    # VVV  UNECESSARY
    voiceSoundChoice = [create_choice(value=file, name=file)
                        for file in MP3_files]

    voiceLangChoice = [{"value": "af", "name": "Afrikaans"},
                       {"value": "ar", "name": "Arabic"},
                       {"value": "de", "name": "German"},
                       {"value": "el", "name": "Greek"},
                       {"value": "en", "name": "English"},
                       {"value": "es", "name": "Spanish"},
                       {"value": "fi", "name": "Finnish"},
                       {"value": "fr", "name": "French"},
                       {"value": "hi", "name": "Hindi"},
                       {"value": "id", "name": "Indonesian"},
                       {"value": "it", "name": "Italian"},
                       {"value": "ja", "name": "Japanese"},
                       {"value": "ko", "name": "Korean"},
                       {"value": "la", "name": "Latin"},
                       {"value": "mk", "name": "Macedonian"},
                       {"value": "my", "name": "Myanmar (Burmese)"},
                       {"value": "nl", "name": "Dutch"},
                       {"value": "pl", "name": "Polish"},
                       {"value": "pt", "name": "Portuguese"},
                       {"value": "ru", "name": "Russian"},
                       {"value": "th", "name": "Thai"},
                       {"value": "tl", "name": "Filipino"},
                       {"value": "tr", "name": "Turkish"},
                       {"value": "vi", "name": "Vietnamese"},
                       {"value": "zh-CN", "name": "Chinese"}]
