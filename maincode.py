"""
Bot soll erstmal festgelegte Wilkommensnachricht senden für LGBTQ+ Gruppe(n)
"""

import telebot
import datetime
import json

bot_token = 'TOKEN'
bot = telebot.TeleBot(bot_token)
bot_name = "@lgbtqia_german_bot"

bot.can_join_groups = True

def json_write(datta, filename='LGBTQ+.json'):
    with open(filename, 'w') as f:
        json.dump(datta, f, indent=4)

while True:
    with open('LGBTQ+.json') as json_file:
        data = json.load(json_file)

    @bot.message_handler(commands=['start'])
    def send_start(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Hi, ich bin der Bot der Gruppe @LGBTQFlintaGerman. Sende /help für mehr!")

    @bot.message_handler(commands=['welcome'])
    def new(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.reply_to(message, data["welcome"])

    @bot.message_handler(content_types=['new_chat_members'])
    def new(message):
        for user in message.new_chat_members:
            userId = user.id
            for i in data["users"]["Banned"]:
                if i["user_id"] == userId:
                    bot.kick_chat_member(message.chat.id, userId)

                    @bot.message_handler(content_types='left_chat_member')
                    def del_left_message(message2):
                        bot.delete_message(message2.chat.id, message2.message_id)
                    bot.reply_to(message, f"Nutzer*in gebannt. Grund: {i['reason']}")
            else:
                bot.reply_to(message, data["welcome"])
                joined_users = data["users"]["Joined"]
                joined_users.append(userId)
                json_write(data)
        bot.delete_message(message.chat.id, message.id)
        json_write(data)

    @bot.message_handler(commands=['rules'])
    def rules(message):
        bot.reply_to(message, "Das sind die Regeln der LGBTQ+ German Gruppe 🌈🏳️‍🌈🏳️‍⚧:\n\n"+data["rules"])

    @bot.message_handler(commands=['kick', 'ban'])
    def kick_person(message):
        try:
            user = message.reply_to_message
            len_command = len(message.text.split()[0])+1
            try:
                reason = message.text[len_command:]
            except AttributeError:
                reason = "None"
            bot.kick_chat_member(message.chat.id, user.id)
            banned_user = {"user_id": int(user.id), "reason": reason}
            data["users"]["Banned"].append(banned_user)
            if user.id in data["users"]["Joined"]:
                data["users"]["Joined"].remove(user.id)
            json_write(data)
            bot.reply_to(message, f"{user.first_name} wurde gekickt! Grund: {reason}")
        except AttributeError:
            len_message = len(message.text.split())
            if len_message < 2:
                bot.reply_to(message, "Du musst eine Nutzer*innen ID angeben oder auf eine Nachricht antworten!")
            elif len_message == 2:
                userId = message.text.split()[1]
                bot.kick_chat_member(message.chat.id, userId)
                reason = "None"
                banned_user = {"user_id": int(userId), "reason": reason}
                data["users"]["Banned"].append(banned_user)
                if userId in data["users"]["Joined"]:
                    data["users"]["Joined"].remove(userId)
                json_write(data)
                bot.reply_to(message, f"Nutzer*in wurde gekickt! Grund: {reason}")
            else:
                userId = message.text.split()[1]
                len_until_reason = len(message.text[:len(message.text.split()[0] + message.text.split()[1])])
                reason = message.text[len_until_reason:]
                bot.kick_chat_member(message.chat.id, userId)
                banned_user = {"user_id": int(userId), "reason": reason}
                data["users"]["Banned"].append(banned_user)
                if userId in data["users"]["Joined"]:
                    data["users"]["Joined"].remove(userId)
                json_write(data)
                bot.reply_to(message, f"Nutzer*in wurde gekickt!\nGrund: {reason}")

        @bot.message_handler(content_types='left_chat_member')
        def member_got_kicked(message2):
            bot.delete_message(message2.chat.id, message2.message_id)
        json_write(data)

    @bot.message_handler(commands=['set_welcome'])
    def set_welcome(message):
        try:
            command = message.text.split()[0]
            text = message.text[len(command) + 1:]
            data["welcome"] = text
            json_write(data)
            bot.reply_to(message, "Willkommensnachricht aktualisiert!")
        except Exception as ex:
            bot.reply_to(message, "Irgendwas ist schief gelaufen.")
            print(ex)
        bot.delete_message(message.chat.id, message.chat.id)
        json_write(data)

    @bot.message_handler(commands=['set_rules'])
    def set_welcome(message):
        try:
            command = message.text.split()[0]
            text = message.text[len(command)+1:]
            data["rules"] = text
            json_write(data)
            bot.reply_to(message, f"Regeln aktualisiert!\nRegeln:\n{data['rules']}")
        except Exception as ex:
            bot.reply_to(message, "Irgendwas ist schief gelaufen.")
            print(ex)
        bot.delete_message(message.chat.id, message.chat.id)
        json_write(data)

    @bot.message_handler(content_types='left_chat_member')
    def member_left(message):
        user = message.left_chat_member
        data["users"]["Joined"].remove(user.id)
        bot.reply_to(message, f"{user.first_name} hat die Gruppe verlassen.")
        json_write(data)
        bot.delete_message(message.chat.id, message.chat.id)

    @bot.message_handler(commands=['warn'])
    def warn_user(message):
        user = message.reply_to_message.from_user
        with open('LGBTQ+.json') as f:
            data = json.load(f)
        warned = data["users"]["warned"]
        len_command = len(message.text.split()[0])+1
        reason = message.text.split[len_command:]
        if warned:
            for i in warned:
                if i["user_id"] == user.id:
                    i["warns"] = i["warns"] + 1
                else:
                    warned.append({"user_id": user.id, "warns": 1})
                    bot.reply_to(message, f"{user.first_name} hat {i['warns']}/3 warns. Pass auf! Bei 3 Verwarnungen wirst du entfernt!\nGrund: {reason}")
                if i["warns"] == 3:
                    banned_user = {"user_id": user.id, "reason": "3 Verwarnungen"}
                    data["users"]["Banned"].append(banned_user)
                    bot.kick_chat_member(message.chat.id, user.id)
                    bot.reply_to(message, f"{user.first_name} wurde entfernt! Grund: 3 Verwarnungen")

                    @bot.message_handler(content_types='left_chat_member')
                    def member_got_kicked(message2):
                        data["users"]["Joined"].remove(user.id)
                        json_write(data)
                        bot.delete_message(message2.chat.id, message2.id)
                else:
                    bot.reply_to(message, f"{user.first_name} hat {i['warns']}/3 warns. Pass auf! Bei 3 Verwarnungen wirst du entfernt!\nGrund: {reason}")
        else:
            warned.append({"user_id": user.id, "warns": 1})
            bot.reply_to(message, f"{user.first_name} hat 1/3 warns. Pass auf! Bei 3 Verwarnungen wirst du entfernt!\nGrund: {reason}")
        json_write(data)
        bot.delete_message(message.chat.id, message.id)

    @bot.message_handler(commands=['unban'])
    def unban_user(message):
        try:
            user = message.reply_to_message
            bot.unban_chat_member(message.chat.id, user.id)
            for i in data["users"]["Banned"]:
                if i["user_id"] == user.id:
                    data["users"]["Banned"].remove(i)
            bot.reply_to(message, f"{user.first_name} wurde eine weitere chance gegeben!")
        except AttributeError:
            len_message = len(message.text.split())
            if len_message < 2:
                bot.reply_to(message, "Du musst eine Nutzer*innen ID angeben oder auf eine Nachricht antworten!")
            elif len_message == 2:
                userId = message.text.split()[1]
                bot.unban_chat_member(message.chat.id, userId)
                for i in data["users"]["Banned"]:
                    if i["user_id"] == userId:
                        data["users"]["Banned"].remove(i)
                bot.reply_to(message, f"{userId} wurde eine weitere chance gegeben!")
            else:
                userId = message.text.split()[1]
                len_until_reason = len(message.text[:len(message.text.split()[0]+message.text.split()[1])])
                reason = message.text[len_until_reason:]
                bot.unban_chat_member(message.chat.id, userId)
                for i in data["users"]["Banned"]:
                    if i["user_id"] == userId:
                        i.remove(userId)
                bot.reply_to(message, f"{userId} wurde eine weitere chance gegeben!\nGrund: {reason}")
        json_write(data)

    now = str(datetime.datetime.now())
    try:
        print("Start Polling   "+now)
        bot.polling()
    except Exception as e:
        print("Error, retry ... " + str(e)+'   '+now)
