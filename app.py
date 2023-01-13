from flask import Flask, render_template, request, Response, url_for
from werkzeug.utils import redirect
from equipment import Equipment
from classes import unit_classes

from base import Arena
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__, template_folder="templates")

heroes = {}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == 'GET':
        header = "Выберите героя"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()

        result = {
            "header": header,  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": weapons,  # для названия оружия
            "armors": armors  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']

        if unit_class not in unit_classes:
            return Response(f"Выбран некорректный класс", status=400)

        equipment = Equipment()
        if weapon_name not in equipment.get_weapons_names():
            return Response(f"Выбранного оружия не существует", status=400)
        if armor_name not in equipment.get_armors_names():
            return Response(f"Выбранной брони не существует", status=400)

        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player.equip_armor(Equipment().get_armor(armor_name))
        player.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == 'GET':
        header = "Выберите соперника"
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()

        result = {
            "header": header,  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": weapons,  # для названия оружия
            "armors": armors  # для названия брони
        }
        return render_template("hero_choosing.html", result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class = request.form['unit_class']

        if unit_class not in unit_classes:
            return Response(f"Выбран некорректный класс", status=400)

        equipment = Equipment()
        if weapon_name not in equipment.get_weapons_names():
            return Response(f"Выбранного оружия не существует", status=400)
        if armor_name not in equipment.get_armors_names():
            return Response(f"Выбранной брони не существует", status=400)

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy.equip_armor(Equipment().get_armor(armor_name))
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(port=25000)
