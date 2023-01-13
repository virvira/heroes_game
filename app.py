from flask import Flask, render_template, request
from equipment import Equipment
from classes import unit_classes

from base import Arena

app = Flask(__name__, template_folder="templates")

heroes = {
    "player": ...,
    "enemy": ...
}

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
        result = arena.player_use_skill
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
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
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

        return render_template("templates/hero_choosing.html", result=result)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    pass


if __name__ == "__main__":
    app.run(port=25000)
