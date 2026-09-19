"""Игровой мир: зачарования, вещи, игроки, гильдии и таблица баланса.

Этот файл держит остальной сервер, поэтому классы и их поля не трогай.
Форум ты пишешь в builds.py.
"""

# Таблица баланса: вид вещи -> (характеристика, базовое значение).
# Патчи меняют именно её, например нерф меча: BALANCE["меч"] = ("урон", 80).
BALANCE = {
    "меч": ("урон", 120),
    "топор": ("урон", 150),
    "лук": ("урон", 90),
    "щит": ("защита", 60),
    "шлем": ("защита", 30),
    "сапоги": ("скорость", 15),
}

STATS = ("урон", "защита", "скорость")


class Enchantment:
    def __init__(self, name, stat, bonus):
        self.name = name
        self.stat = stat          # одна из STATS
        self.bonus = bonus

    def __repr__(self):
        return f"<{self.name} +{self.bonus} {self.stat}>"


class Item:
    def __init__(self, name, kind, enchantments=None):
        self.name = name
        self.kind = kind          # ключ в BALANCE
        self.enchantments = list(enchantments) if enchantments else []

    def __repr__(self):
        return f"<{self.name} ({self.kind}) x{len(self.enchantments)}>"


class Player:
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.equipment = []       # надетые вещи
        self.guild = None

    def __repr__(self):
        return f"<Player {self.name}>"


class Guild:
    def __init__(self, tag):
        self.tag = tag
        self.members = []

    def join(self, player):
        if player.guild is not None:
            player.guild.leave(player)
        self.members.append(player)
        player.guild = self

    def leave(self, player):
        self.members.remove(player)
        player.guild = None

    def __repr__(self):
        return f"<Guild {self.tag} ({len(self.members)})>"


def character_stats(items, balance=None):
    """Характеристики персонажа в этих вещах по таблице баланса."""
    balance = BALANCE if balance is None else balance
    stats = dict.fromkeys(STATS, 0)
    for item in items:
        stat, base = balance.get(item.kind, ("урон", 0))
        stats[stat] += base
        for ench in item.enchantments:
            stats[ench.stat] += ench.bonus
    return stats


def remove_from_game(player):
    """Удалить игрока из игры: выйти из гильдии, снять всё.

    Ссылки на игрока, которые держат другие системы, эта функция не трогает.
    """
    if player.guild is not None:
        player.guild.leave(player)
    player.equipment = []


_KINDS = ("меч", "щит", "шлем", "сапоги", "лук", "топор")
_ENCHANTS = (("Огонь", "урон", 12), ("Камень", "защита", 8), ("Ветер", "скорость", 5))
_NAMES = ("ada", "bo", "cy", "dee", "eli", "fox", "gus", "hal", "ivy", "jo")


def make_player(name, level=10, items=6, enchantments=3):
    player = Player(name, level)
    for i in range(items):
        kind = _KINDS[i % len(_KINDS)]
        player.equipment.append(Item(
            f"{kind} {name}",
            kind,
            [Enchantment(*_ENCHANTS[j % len(_ENCHANTS)]) for j in range(enchantments)],
        ))
    return player


def make_test_guild(tag="WOLF", players=200, items=6, enchantments=3):
    """Тестовая гильдия: 200 игроков, у каждого 6 вещей по 3 зачарования.

    Первый игрок — ada: guild.members[0].
    """
    guild = Guild(tag)
    for n in range(players):
        name = _NAMES[n] if n < len(_NAMES) else f"player{n:03d}"
        guild.join(make_player(name, items=items, enchantments=enchantments))
    return guild
