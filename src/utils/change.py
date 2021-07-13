
async def change_last_message(ctx):
    dic1={
        "1":"ๅ",
        "!":"+",
        "2":"/",
        "@":"๑",
        "3":"-",
        "#":"๒",
        "4":"ภ",
        "$":"๓",
        "5":"ถ",
        "%":"๔",
        "6":"ุ",
        "^":"ู",
        "7":"ึ",
        "&":"฿",
        "8":"ค",
        "*":"๕",
        "9":"ต",
        "(":"๖",
        "0":"จ",
        ")":"๗",
        "-":"ข",
        "_":"๘",
        "=":"ช",
        "+":"๙",

        "q":"ๆ",
        "Q":"๐",
        "w":"ไ",
        "W":"\"",
        "e":"ำ",
        "E":"ฎ",
        "r":"พ",
        "R":"ฑ",
        "t":"ะ",
        "T":"ธ",
        "y":"ั",
        "Y":"ํ",
        "u":"ี",
        "U":"๊",
        "i":"ร",
        "I":"ณ",
        "o":"น",
        "O":"ฯ",
        "p":"ย",
        "P":"ญ",
        "[":"บ",
        "{":"ฐ",
        "]":"ล",
        "}":",",
        "\\":"ฃ",
        "|":"ฅ",

        "a":"ฟ",
        "A":"ฤ",
        "s":"ห",
        "S":"ฆ",
        "d":"ก",
        "D":"ฏ",
        "f":"ด",
        "F":"โ",
        "g":"เ",
        "G":"ฌ",
        "h":"้",
        "H":"็",
        "j":"่",
        "J":"๋",
        "k":"า",
        "K":"ษ",
        "l":"ส",
        "L":"ศ",
        ";":"ว",
        ":":"ซ",
        "'":"ง",
        "\"":".",
        
        "z":"ผ",
        "Z":"(",
        "x":"ป",
        "X":")",
        "c":"แ",
        "C":"ฉ",
        "v":"อ",
        "V":"ฮ",
        "b":"ิ",
        "B":"ฺ",
        "n":"ื",
        "N":"์",
        "m":"ท",
        "M":"?",
        ",":"ม",
        "<":"ฒ",
        ".":"ใ",
        ">":"ฬ",
        "/":"ฝ",
        "?":"ฦ",
        " ":" "
    }

    dic2={
    }

    for i in dic1:
        dic2[dic1[i]]=i

    channel = ctx.channel
    fetchMessage = await channel.history().flatten()
    for i in range(1,len(fetchMessage)):
        if (fetchMessage[i].author == ctx.author) & (not fetchMessage[i].content.startswith('$')):
            message=fetchMessage[i].content
            answer=''
            for i in range (len(message)):

                try:
                    answer += dic1[message[i]]
                except KeyError:
                    answer += dic2[message[i]]

            await ctx.send(f'{ctx.author} อ่ะแก้ให้ละ\n> {answer}')
            break
    if fetchMessage[i].content == None:
        await ctx.send(f'{ctx.author} พิมพ์มาก่อนดิวะไม่พิมพ์มาผมจะแก้อะไรล่ะะ')