from discord_slash.utils.manage_commands import create_option, create_choice
from src.utils.config import MP3_files


def fetchArguments(msg):

    if msg == None:
        return None, None

    msgsplit = msg.split("-")

    if msg.startswith("-"):
        return None, msgsplit[0]

    elif "-" in msg:
        return msgsplit[0], msgsplit[1:]

    else:
        return msg, None


class SlashChoice:
    voiceSoundChoice = [{"value": "imgay",  "name": "I am gay (IDUBBBZTV)"},
                        {"value": "yee",    "name": "Yee"},
                        {"value": "oof",    "name": "OOF"},
                        {"value": "intro",  "name": "Intro"}]
    
    voiceTuSoundChoice=[{"value": "tu1:",   "name": "ฮ้ะ (Huh?)"},
                        {"value": "tu2",    "name": "อื่อฮึ (Uh-huh)"},
                        {"value": "tu3",    "name": "ทำไม (Why?)"},
                        {"value": "tu4",    "name": "อะไร อะไร (Whatx2)"},
                        {"value": "tu5",    "name": "จะเอาอะไรจากผมอ้ะ (What do you want from me?)"},
                        {"value": "tu6",    "name": "Okay"},
                        {"value": "tu7",    "name": "ชักไม่เข้าท่าแล้วนะ 1(It's getting inappropriate1)"},
                        {"value": "tu8",    "name": "จบยัง (Done?)"},
                        {"value": "tu9",    "name": "จะเอาอะไรจากผมอ้ะ (What do you want from me?)"},
                        {"value": "tu10",   "name": "โธ่วววววว์ (Interjection1)"},
                        {"value": "tu11",   "name": "อะไร เอาใหม่ดิ๊ (What? Say it again.)"},
                        {"value": "tu12",   "name": "อ่า (Ah.)"},
                        {"value": "tu13",   "name": "ฮ้ะ (Hah.)"},
                        {"value": "tu14",   "name": "ทำไมเล่า (Just why?)"},
                        {"value": "tu15",   "name": "มีอะไร (What do you want?)"},
                        {"value": "tu16",   "name": "อ่าแล้วอะไรอีก (Ah, what's next?)"},
                        {"value": "tu17",   "name": "ชักไม่เข้าท่าแล้วนะ2 (It's getting inappropriate2"},
                        {"value": "tu18",   "name": "เดี๋ยวเหอะ (Interjection2)"},
                        {"value": "tu19",   "name": "ไร้สาระ (Nonsense.)"},
                        {"value": "tu20",   "name": "อะไรน (What??)"},
                        {"value": "tu21",   "name": "เข้าใจมั้ย (Got it?)"},
                        {"value": "tu22",   "name": "หัวเราะ หัวเราะ (Laughx2)"}]
                
                        
    voiceLangChoice = [{"value": "af",      "name": "Afrikaans"},
                       {"value": "ar",      "name": "Arabic"},
                       {"value": "de",      "name": "German"},
                       {"value": "el",      "name": "Greek"},
                       {"value": "en",      "name": "English"},
                       {"value": "es",      "name": "Spanish"},
                       {"value": "fi",      "name": "Finnish"},
                       {"value": "fr",      "name": "French"},
                       {"value": "hi",      "name": "Hindi"},
                       {"value": "id",      "name": "Indonesian"},
                       {"value": "it",      "name": "Italian"},
                       {"value": "ja",      "name": "Japanese"},
                       {"value": "ko",      "name": "Korean"},
                       {"value": "la",      "name": "Latin"},
                       {"value": "mk",      "name": "Macedonian"},
                       {"value": "my",      "name": "Myanmar (Burmese)"},
                       {"value": "nl",      "name": "Dutch"},
                       {"value": "pl",      "name": "Polish"},
                       {"value": "pt",      "name": "Portuguese"},
                       {"value": "ru",      "name": "Russian"},
                       {"value": "th",      "name": "Thai"},
                       {"value": "tl",      "name": "Filipino"},
                       {"value": "tr",      "name": "Turkish"},
                       {"value": "vi",      "name": "Vie tnamese"},
                       {"value": "zh-CN",   "name": "Chinese"}]
