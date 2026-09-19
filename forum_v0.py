"""Форум билдов, прошлый патч. Сделано на коленке, работает, скандалит.

Файл нужен только затем, чтобы воспроизвести обе жалобы из тикета.
Чинить его не надо: новую версию ты пишешь в builds.py.
"""

from world import character_stats


class Build:
    def __init__(self, name, author, items):
        self.name = name
        self.author = author
        self.items = items
        self.guild = author.guild
        self.parent = None

    @property
    def stats(self):
        return character_stats(self.items)

    def __repr__(self):
        return f"<Build {self.name} by {self.author.name}>"


FORUM = []


def publish(player, name):
    build = Build(name, player, player.equipment)
    FORUM.append(build)
    return build
