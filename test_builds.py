import builds
import world
import pytest
import weakref
import gc 

def hero_build():
    wind_dragon = world.Enchantment("Ветер", "урон", 20)
    sword = world.Item("Макнуин", "меч", [wind_dragon])
    helmet = world.Item("Last_chanse", "шлем")
    guild = world.Guild("Evil")

    player = world.Player("Bad_boy")
    guild.join(player)
    player.equipment = [sword, helmet]
    published_build = builds.publish(player, "The_best")
    return player, helmet, sword, wind_dragon, published_build

def test_change_equipment():
    player, helmet, sword, wind_dragon, published_build = hero_build()
    player.equipment.append(world.Item("Bootsss", "сапоги"))

    assert len(published_build.items) == 2, "Ошибка добавления предметов"

def test_change_item():
    player, helmet, sword, wind_dragon, published_build = hero_build()

    helmet.name =  "Loose" 

    assert published_build.items[1].name == "Last_chanse"

def test_change_enchantment():
    player, helmet, sword, wind_dragon, published_build = hero_build()

    Dragon_breath = world.Enchantment("Огонь", "урон", 25)
    sword.enchantments = [Dragon_breath]

    assert published_build.items[0].enchantments[0].name == "Ветер", "Ошибка зачарования"

def test_change_guild():
    player, helmet, sword, wind_dragon, published_build = hero_build()

    New_guild = world.Guild("Rav")
    player.guild = New_guild

    assert published_build.guild_tag == "Evil", "Ошибка гильдии"

def test_memory1():
    guild = world.make_test_guild()
    player = guild.members[0]

    published_build = builds.publish(player, "NO_UOM")

    result = builds.count_objects_in_my_build(published_build)

    print(result)

    assert result <=30, "UOM"

def test_memory2():
    guild = world.make_test_guild()
    player = guild.members[0]

    published_build = builds.publish(player, "NO_UOM")

    result = builds.count_objects_in_my_build(published_build)

    print(result)

    assert result ==25, "UOM"


def test_deleted_ref_hero():
    player = world.Player("Dead")
    player_ref = weakref.ref(player)
    published_build = builds.publish(player, "Still_Alive")
    world.remove_from_game(player)
    del player
    gc.collect() 

    assert player_ref() is None, "Ошибка сохрання игрока в памяти"
    
def test_name_of_deleted_hero():
    player = world.Player("Dead")
    player_ref = weakref.ref(player)
    published_build = builds.publish(player, "Still_Alive")
    world.remove_from_game(player)
    del player
    gc.collect() 

    assert published_build.author_name == "Dead", "Ошибка сохранения имени"


def test_parents1():
    player1 = world.make_player("First")
    player2 = world.make_player("Second")
    player3 = world.make_player("Third")

    published_build1 = builds.publish(player1, "First_build")
    forked_build1 = builds.fork(published_build1, player2, "First_build")
    published_build2 = builds.publish(player2, "Second_build")
    forked_build2 = builds.fork(published_build2, player1, "Second_build")

    assert len(builds.ancestry(forked_build2)) == 2, "Parents mistake"

def test_parents2():
    player1 = world.make_player("First")
    player2 = world.make_player("Second")
    player3 = world.make_player("Third")

    build1 = builds.publish(player1, "First_build")
    build2 = builds.fork(build1, player2, "Second_build")
    build3 = builds.fork(build2, player3, "Third_build")

    build1.parent = build3
    

    assert len(builds.ancestry(build3)) == 3, "Parents mistake, incorrect amount of parents"


def test_parents3():
    player1 = world.make_player("First")
    player2 = world.make_player("Second")
    player3 = world.make_player("Third")

    build1 = builds.publish(player1, "First_build")
    build2 = builds.fork(build1, player2, "Second_build")
    build3 = builds.fork(build2, player3, "Third_build")

    build1.parent = build3
    

    assert builds.ancestry(build3) == [build3, build2, build1], "Parents mistake, incorrect parents"



def test_nerf_build1():
    world.BALANCE["меч"] = ("урон", 120)
    hero = world.make_player(name="Hero", items = 6, enchantments = 3)
    static_build = builds.publish(hero, "Static_build")
    dynamic_build = builds.publish(hero, "Dynamic_bild", dynamic = True)

    first_damage = static_build.stats["урон"]
    

    world.BALANCE["меч"] = ("урон", 80)

    assert static_build.stats["урон"] == first_damage, "Ошибка, измение урона в статичном режиме"

def test_nerf_build2():
    world.BALANCE["меч"] = ("урон", 120)
    hero = world.make_player(name="Hero", items = 6, enchantments = 3)
    static_build = builds.publish(hero, "Static_build")
    dynamic_build = builds.publish(hero, "Dynamic_bild", dynamic = True)

    first_damage = static_build.stats["урон"]
    

    world.BALANCE["меч"] = ("урон", 80)

    assert dynamic_build.stats["урон"] != first_damage

def test_nerf_build3():
    world.BALANCE["меч"] = ("урон", 120)
    hero = world.make_player(name="Hero", items = 6, enchantments = 3)
    static_build = builds.publish(hero, "Static_build")
    dynamic_build = builds.publish(hero, "Dynamic_bild", dynamic = True)

    first_damage = static_build.stats["урон"]
    

    world.BALANCE["меч"] = ("урон", 80)

    assert static_build.stats["урон"] - dynamic_build.stats["урон"] == 40, "Ошибка, непраивльное изменение урона"

def test_nerf_build4():
    world.BALANCE["меч"] = ("урон", 120)
    hero = world.make_player(name="Hero", items = 6, enchantments = 3)
    static_build = builds.publish(hero, "Static_build")
    dynamic_build = builds.publish(hero, "Dynamic_bild", dynamic = True)

    first_damage_static = static_build.stats["урон"]
    first_damage_dynamic = dynamic_build.stats["урон"]

    world.BALANCE["меч"] = ("урон", 80)

    assert first_damage_static == first_damage_dynamic, "Ошибка баг из будуюшего"
    

    

