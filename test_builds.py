import gc
import weakref

from builds import Forum, ancestry, fork, live_stats, publish
from world import BALANCE, Enchantment, Guild, Item, Player, make_test_guild, remove_from_game


def make_player():
    p = Player("ada", level=10)
    p.equipment.append(Item("меч", "меч", [Enchantment("Огонь", "урон", 12)]))
    return p


def test_isolation_equipment_change():
    p = make_player()
    build = publish(p, "билд")
    assert len(build.items) == 1

    p.equipment.clear()
    assert len(build.items) == 1
    assert build.items[0].name == "меч"


def test_isolation_item_mutation():
    p = make_player()
    sword = p.equipment[0]
    build = publish(p, "билд")

    sword.name = "сломанный"
    sword.kind = "топор"
    assert build.items[0].name == "меч"
    assert build.items[0].kind == "меч"


def test_isolation_enchantment_mutation():
    p = make_player()
    sword = p.equipment[0]
    build = publish(p, "билд")

    sword.enchantments[0].bonus = 999
    sword.enchantments.append(Enchantment("Камень", "защита", 8))
    assert build.items[0].enchantments[0].bonus == 12
    assert len(build.items[0].enchantments) == 1


def test_isolation_guild_change():
    p = make_player()
    Guild("WOLF").join(p)
    build = publish(p, "билд")
    assert build.guild_tag == "WOLF"

    Guild("RAVEN").join(p)
    assert build.guild_tag == "WOLF"
    assert build.author_name == "ada"


def copied_objects(build):
    n = 1
    for it in build.items:
        n += 1
        n += len(it.enchantments)
    return n


def test_copy_boundary():
    p = make_test_guild().members[0]
    build = publish(p, "билд")
    n = copied_objects(build)
    print("скопировано объектов при публикации:", n)
    assert n <= 30
    assert n == 25


def test_fork_has_parent():
    p = make_player()
    a = publish(p, "а")
    b = fork(a, p, "б")
    assert b.parent is a
    assert ancestry(b) == [b, a]
    assert ancestry(a) == [a]


def test_fork_copies_items():
    p = make_player()
    a = publish(p, "а")
    b = fork(a, p, "б")

    a.items[0].name = "испорчен"
    a.items[0].enchantments[0].bonus = 0
    assert b.items[0].name == "меч"
    assert b.items[0].enchantments[0].bonus == 12


def test_ancestry_stops_on_cycle():
    p = make_player()
    a = publish(p, "а")
    b = fork(a, p, "б")
    c = fork(b, p, "в")
    a.parent = c
    c.parent = b
    b.parent = a

    assert ancestry(a) == [a, c, b]


def test_removed_player_is_freed():
    p = make_test_guild().members[0]
    w = weakref.ref(p)
    forum = Forum()
    build = publish(p, "танк")
    forum.post(build)

    remove_from_game(p)
    del p
    gc.collect()

    assert w() is None
    assert build.author is None
    assert build.author_name == "ada"
    assert build.guild_tag == "WOLF"
    assert build in forum.top(10)


def test_snapshot_survives_nerf():
    old = BALANCE["меч"]
    try:
        p = Player("ada", level=10)
        p.equipment.append(Item("меч", "меч"))
        build = publish(p, "билд")
        assert build.stats["урон"] == 120

        BALANCE["меч"] = ("урон", 80)

        assert build.stats["урон"] == 120
        assert live_stats(build)["урон"] == 80
    finally:
        BALANCE["меч"] = old


def test_forum_likes_and_top():
    p = make_player()
    a = publish(p, "а")
    b = fork(a, p, "б")
    forum = Forum()
    forum.post(a)
    forum.post(b)

    assert forum.likes(a) == 0
    forum.like(b)
    forum.like(b)
    forum.like(a)
    assert forum.likes(a) == 1
    assert forum.likes(b) == 2
    assert forum.top(2) == [b, a]
