from discord_slash.utils.manage_commands import create_option, create_choice
from src.utils.config import MP3_files


def fetchArguments(msg):

    if msg is None:
        return None, None

    msgsplit = msg.split("-")

    if msg.startswith("-"):
        return None, msgsplit[0]

    elif "-" in msg:
        return msgsplit[0], msgsplit[1:]

    else:
        return msg, None


class SlashChoice:
    choiceSound = [
        {"value": "imgay",  "name": "I am gay (IDUBBBZTV)"},
        {"value": "yee",    "name": "Yee"},
        {"value": "oof",    "name": "OOF"},
        {"value": "intro",  "name": "Intro"}
        ]
    
    choiceOVoice =[
        {"value": "o1",     "name": "o1 ข้าพเจ้ารู้สึกตื้นตัน (I am impressed.)"},
        {"value": "o2",     "name": "o2 ข้าพเจ้าขอส่งความประถณาดี (I wish you best wishes.)"},
        {"value": "o3",     "name": "o3 *ไอ* (*cough*)"}
        ]
    
    choiceTuVoice=[
        {"value": "tu1",    "name": "tu1 ฮ้ะ (Huh?)"},
        {"value": "tu2",    "name": "tu2 อื่อฮึ (Uh-huh)"},
        {"value": "tu3",    "name": "tu3 ทำไม (Why?)"},
        {"value": "tu4",    "name": "tu4 อะไร อะไร (Whatx2)"},
        {"value": "tu5",    "name": "tu5 จะเอาอะไรจากผมอ้ะ (What do you want from me?)"},
        {"value": "tu6",    "name": "tu6 Okay"},
        {"value": "tu7",    "name": "tu7 ชักไม่เข้าท่าแล้วนะ 1(It's getting inappropriate1)"},
        {"value": "tu8",    "name": "tu8 จบยัง (Done?)"},
        {"value": "tu9",    "name": "tu9 จะเอาอะไรจากผมอ้ะ (What do you want from me?)"},
        {"value": "tu10",   "name": "tu10 โธ่วววววว์ (Interjection1)"},
        {"value": "tu11",   "name": "tu11 อะไร เอาใหม่ดิ๊ (What? Say it again.)"},
        {"value": "tu12",   "name": "tu12 อ่า (Ah.)"},
        {"value": "tu13",   "name": "tu13 ฮ้ะ (Huh?)"},
        {"value": "tu14",   "name": "tu14 ทำไมเล่า (Just why?)"},
        {"value": "tu15",   "name": "tu15 มีอะไร (What do you want?)"},
        {"value": "tu16",   "name": "tu16 อ่าแล้วอะไรอีก (Ah, what's next?)"},
        {"value": "tu17",   "name": "tu17 ชักไม่เข้าท่าแล้วนะ2 (It's getting inappropriate2"},
        {"value": "tu18",   "name": "tu18 เดี๋ยวเหอะ (Interjection2)"},
        {"value": "tu19",   "name": "tu19 ไร้สาระ (Nonsense.)"},
        {"value": "tu20",   "name": "tu20 อะไรนะ  (What??)"},
        {"value": "tu21",   "name": "tu21 เข้าใจมั้ย (Got it?)"},
        {"value": "tu22",   "name": "tu22 หัวเราะ หัวเราะ (Laughx2)"},
        {"value": "tu23",   "name": "tu23 ไม่ได้โมโหเลย! (I'm not even angry!)"}
        ]
    
    choicePomVoice   =  [
        {"value": "pom1",  "name": "pom1 ไม่รู้ ยังไม่รู้เรื่องอะไรเลย (I don't know, I don't know anything yet.)"},
        {"value": "pom2",  "name": "pom2 ไม่รู้ ยังไม่รู้ยังไม่รู้ยังไม่รู้ (I don't know, I don't know anything yet. x3)"},
        {"value": "pom3",  "name": "pom3 ก็ยังไม่เห็นเลยไอ้ห่า (I still haven't seen it, bastard.)"}
        ]
    
    choiceVoiceLang  =  [
        {"value": "af",      "name": "Afrikaans"},
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
        {"value": "vi",      "name": "Vietnamese"},
        {"value": "zh-CN",   "name": "Chinese"}
        ]
    
    programmingLanguageChoice = [
        {"value": "html",       "name": "HTML, XML"},
        {"value": "bash",       "name": "Bash"},
        {"value": "c",          "name": "C"},
        {"value": "c++",        "name": "C++"},
        {"value": "csharp",     "name": "C#"},
        {"value": "css",        "name": "CSS"},
        {"value": "markdown",   "name": "Markdown"},
        {"value": "ruby",       "name": "Ruby"},
        {"value": "go",         "name": "Go"},
        {"value": "java",       "name": "Java"},
        {"value": "js",         "name": "Javascript"},
        {"value": "json",       "name": "JSON"},
        {"value": "kotlin",     "name": "Kotlin"},
        {"value": "lua",        "name": "Lua"},
        {"value": "objc",       "name": "Objective-C"},
        {"value": "php",        "name": "PHP"},
        {"value": "py",         "name": "Python"},
        {"value": "r",          "name": "R"},
        {"value": "rust",       "name": "Rust"},
        {"value": "shell",      "name": "Shell Session"},
        {"value": "sql",        "name": "SQL"},
        {"value": "swift",      "name": "Swift"},
        {"value": "yaml",       "name": "YAML"},
        {"value": "typescript", "name": "TypeScript"},
        {"value": "vbnet",      "name": "Visual Basic .NET"}
        ]
