#!/usr/bin/env python

# Unicode dependent languages are not yet supported
languages = {
    #'cs' : 'Czech',
    #'sr' : 'Serbian',
    'cy' : 'Welsh', 'da' : 'Danish',
    'de' : 'German', 'es' : 'Spanish', 'et' : 'Estonian',
    #'el' : 'Greek',
    'fr' : 'French', 'it' : 'Italian', 'sw' : 'Swahili', 'nl' : 'Dutch',
    'no' : 'Norway', 'pl' : 'Polish', 'pt' : 'Portuguese',
    #'ru' : 'Russian',
    'sv' : 'Swedish', 'fi' : 'Finnish',
    #'zh-CN' : 'Chinese (Simplified)', 'hi' : 'Hindi', 'ko' : 'Korean', 'ja' : 'Japanese',
    'en' : 'English'}

def set_nick(session, command):
    if not len(command) > 1:
        session.server.send_private_message(session, "Insufficient Arguments for /nickname command.")
    else:
        oldnick = session.nick
        for s in session.server.sessions:
            if s == session: pass
            elif s.nick == command[1]:
                session.server.send_private_message(session, "That name is already being used. Please use '/nickname' to select a different nickname.")
                return
        session.nick = command[1]
        session.server.broadcast(0, oldnick + " is now known as " + session.nick)
        
def set_lang(session, command):
    if not len(command) > 1:
        session.server.send_private_message(session, "Insufficient Arguments for /setlang command.")
    elif not languages.has_key(command[1]):
        session.server.send_private_message(session, "Invalid language code for /setlang. Use '/help languages' to see a list of available languages.")
    else:
        session.language = command[1]
        session.server.send_motd(session)
        
def help(session, command):
    if len(command) == 1:
        # Display commands
        stringy = "Available commands:\n"
        for cmd in COMMANDS.keys():
            stringy += cmd+"\n"
            stringy += "For more detailed help type '/help <command name>'\n"
        #pass
    elif len(command) > 1 and command[1] == 'languages':
        # Display list of available languages
        langs = "Available Languages\n\n"
        for lang in sorted(languages):
            langs += lang + " : " + languages[lang] + "\n"
        session.server.send_private_message(session, langs)
        
    else:
        session.server.send_private_message(session, "Invalid argument(s) for /help command.")


COMMANDS = {
    'nickname' : set_nick,
    'setlang' : set_lang,
    'help' : help,
    }
