"""Форум билдов. Здесь ты пишешь новую систему.й

Классы мира (Player, Item, Enchantment, Guild) лежат в world.py, их не трогай.
Внутреннее устройство Build — твоё решение. Снаружи у билда должны читаться
поля, перечисленные в README: на них опираются автопроверки.
"""
import copy 
import weakref
from world import BALANCE, Enchantment, Guild, Item, Player, character_stats


class Build:
    def __init__(self, name, items: list[Item], stats, author=None, guild_tag=None, parent=None, dynamic = False):
        self.name = name 
        self.items = []
        for item in items:
            cloned_item = Item(name = item.name, kind = item.kind)
            cloned_item.enchantments = [copy.copy(enchantments) for enchantments in item.enchantments]
            self.items.append(cloned_item)
        
        self.guild_tag = guild_tag
        self.parent = parent
        self._author_ref = weakref.ref(author) if author is not None else None
        self._author_name = author.name if author is not None else "Аноним"

        self._dynamic = dynamic
        self._old_stats = stats.copy()

    @property
    def stats(self):
        if self._dynamic == False:
            return self._old_stats
        else:
            return character_stats(self.items)



    @property
    def author_name(self):
        return self._author_name

    @property
    def author(self):
        return self._author_ref() if self._author_ref is not None else None 



    """Опубликованный билд."""


class Forum:
    def __init__(self):
        self.build_and_likes = {}

    def post(self, build):
        self.build_and_likes[build] = 0

        return build 
        """Выложить билд на форум."""
        raise NotImplementedError

    def like(self, build):
        self.build_and_likes[build] = self.build_and_likes.get(build, 0) + 1

        """Поставить билду лайк."""
        raise NotImplementedError

    def likes(self, build):
        return self.build_and_likes.get(build, 0)
        """Сколько у билда лайков."""
        raise NotImplementedError

    def top(self, n=10):
        result = dict(sorted(self.build_and_likes.items(), key = lambda item:item[1], reverse = True)[:n])
        return result
        """n билдов с наибольшим числом лайков, по убыванию."""
        raise NotImplementedError


def publish(player, name, dynamic = False):
    return Build(
        name = name,
        items = player.equipment,
        stats = character_stats(player.equipment),
        author = player,
        guild_tag = player.guild.tag if player.guild is not None else None, 
        parent = None,
        dynamic = dynamic 
    )
    

    """Снимок экипировки игрока на момент публикации."""
    raise NotImplementedError


def fork(build, player, name):
    return Build(
        name = name,
        items = build.items,
        stats = build.stats,
        author = player,
        guild_tag = player.guild.tag if player.guild is not None else None,
        parent = build 
    )
    


    """Новый билд игрока player «на основе билда build»."""
    raise NotImplementedError


def ancestry(build):
    chain = []
    visited_players = set()
    current_build = build
    while current_build != None:
        if current_build in visited_players:
            break
        else:
            visited_players.add(current_build)
            chain.append(current_build)
            current_build = current_build.parent
    return chain



    """Цепочка от самого билда до корня: [build, родитель, дед, ...]."""
    raise NotImplementedError

def count_objects_in_my_build(build):
    count = set()
    for item in build.items:
        count.add(id(item))
        for e in item.enchantments:
            count.add(id(e))
    return len(count) +1


    


    
