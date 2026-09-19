"""Форум билдов. Здесь ты пишешь новую систему.

Классы мира (Player, Item, Enchantment, Guild) лежат в world.py, их не трогай.
Внутреннее устройство Build — твоё решение. Снаружи у билда должны читаться
поля, перечисленные в README: на них опираются автопроверки.
"""

from world import BALANCE, Enchantment, Guild, Item, Player, character_stats


class Build:
    """Опубликованный билд."""


class Forum:
    def post(self, build):
        """Выложить билд на форум."""
        raise NotImplementedError

    def like(self, build):
        """Поставить билду лайк."""
        raise NotImplementedError

    def likes(self, build):
        """Сколько у билда лайков."""
        raise NotImplementedError

    def top(self, n=10):
        """n билдов с наибольшим числом лайков, по убыванию."""
        raise NotImplementedError


def publish(player, name):
    """Снимок экипировки игрока на момент публикации."""
    raise NotImplementedError


def fork(build, player, name):
    """Новый билд игрока player «на основе билда build»."""
    raise NotImplementedError


def ancestry(build):
    """Цепочка от самого билда до корня: [build, родитель, дед, ...]."""
    raise NotImplementedError
