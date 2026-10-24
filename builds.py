import weakref

from world import BALANCE, Enchantment, Guild, Item, Player, character_stats


def _copy_item(item):
    enchants = [Enchantment(e.name, e.stat, e.bonus) for e in item.enchantments]
    return Item(item.name, item.kind, enchants)


class Build:
    def __init__(self, name, items, stats, author, author_name, guild_tag,
                 parent=None):
        self.name = name
        self.items = items
        self.stats = stats
        self.author_name = author_name
        self.guild_tag = guild_tag
        self.parent = parent
        self._author = weakref.ref(author) if author is not None else None

    @property
    def author(self):
        if self._author is None:
            return None
        return self._author()

    def __repr__(self):
        return f"<Build {self.name} by {self.author_name}>"


class Forum:
    def __init__(self):
        self._posts = []
        self._likes = {}

    def post(self, build):
        self._posts.append(build)
        self._likes.setdefault(build, 0)

    def like(self, build):
        self._likes[build] = self._likes.get(build, 0) + 1

    def likes(self, build):
        return self._likes.get(build, 0)

    def top(self, n=10):
        ordered = sorted(self._posts, key=lambda b: self._likes.get(b, 0),
                         reverse=True)
        return ordered[:n]


def publish(player, name):
    items = [_copy_item(it) for it in player.equipment]
    stats = character_stats(items)
    guild_tag = player.guild.tag if player.guild is not None else None
    return Build(name, items, stats, player, player.name, guild_tag)


def fork(build, player, name):
    items = [_copy_item(it) for it in build.items]
    stats = dict(build.stats)
    guild_tag = player.guild.tag if player.guild is not None else None
    return Build(name, items, stats, player, player.name, guild_tag,
                 parent=build)


def ancestry(build):
    chain = []
    seen = set()
    cur = build
    while cur is not None:
        if cur in seen:
            break
        seen.add(cur)
        chain.append(cur)
        cur = cur.parent
    return chain


def live_stats(build):
    return character_stats(build.items)
