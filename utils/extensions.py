from discord.ext import commands

from ext_list import extensions


def parse_ext_name(ext_path: str):
    split_path = ext_path.split('/')
    filename = split_path[-1]

    name = '.'.join(filename.split('.')[:-1]) if '.' in filename else filename

    split_path = split_path[:-1]
    split_path.append(name)

    ext_name = '.'.join(split_path)
    return ext_name


def load_ext(bot: commands.Bot, path: str = None, name: str = None):
    ext_name = parse_ext_name(path) if path else name
    try:
        bot.load_extension(ext_name)
    except commands.ExtensionAlreadyLoaded:
        bot.reload_extension(ext_name)


def load_all_ext(bot: commands.Bot):
    for i in extensions.values():
        load_ext(bot, i)


def reload_ext(bot: commands.Bot, path: str = None, name: str = None):
    ext_name = parse_ext_name(path) if path else name
    bot.reload_extension(ext_name)


def reload_all_ext(bot: commands.Bot):
    for i in extensions.values():
        reload_ext(bot, i)


def unload_ext(bot: commands.Bot, path: str = None, name: str = None):
    ext_name = parse_ext_name(path) if path else name
    bot.unload_extension(ext_name)


def unload_all_ext(bot: commands.Bot):
    for i in extensions.values():
        unload_ext(bot, i)
