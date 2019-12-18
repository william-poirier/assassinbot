import random
import json
from flask import Flask, request, render_template

# Will Poirier
# Software Engineering
# Assassin-Bot

# This program is designed to help run a game me and my friends play called Assassins
# The game is set up with every player in a "circle"
# Each player only knows their target (a player on one side of them in the "circle")
# If you can "kill" your target (poke them with a pencil or something), you replace them in the circle
# And get points based on some factors, including the number of witnesses
# This program is designed to automate the circle aspect of this game
# Thus removing the need for a person to not play the game and manually manage the circle

app = Flask(__name__)


@app.route("/")
def main():
    # Display the homepage
    return render_template("/")


# That template will have a button to see someone's target
# That will take you to "/target", where you input the username
@app.route("/target_find")
def find_target(user):
    circle = load_circle()
    target = circle[user]
    return render_template("/target_found")  # Need to get target sent to HTML


def load_circle():
    with open("circle.json", "r") as f:
        circle = json.load(f)  # loads all key-value pairs from file into dictionary
    return circle


def save_circle(circle):
    with open("circle.json", "w") as f:
        json.dump(circle, f, indent=2)


def load_points():
    with open("point_totals.json", "r") as f:
        point_totals = json.load(f)  # loads all key-value pairs from file into dictionary
    return point_totals


def save_points(point_totals):
    with open("point_totals.json", "w") as f:
        json.dump(point_totals, f, indent=2)


# Here's the big one - the "I killed someone" button
# "/kill" redirects here after the info is gathered
@app.route("/kill_")
def kill_player(killer, killed, witnesses):
    circle = load_circle()
    points = 50
    points -= witnesses
    if circle[killed] == killer:
        points += 25
    if circle["kills"] == 0:
        points += 25
    point_totals = load_points()
    point_totals[killer] += points
    save_points(point_totals)
    circle[killer] = circle[killed]
    circle.delete(killed)
    save_circle(circle)
    main()


# The Create New Game button will exist, which will be an overwrite for the whole system.
# That's where the point_totals and circle starting conditions come from
@app.route("/create")
def create_new_game():
    circle = {}
    point_totals = {}
    save_circle(circle)
    save_points(point_totals)
    main()


# an Add Player Button will lead here
@app.route("/add_player_")
def add_player(username):
    circle = load_circle()
    point_totals = load_points()
    circle[username] = "none"
    point_totals[username] = 0
    save_circle(circle)
    save_points(point_totals)
    main()


# The Start Game button makes the Add Player button disapear somehow
# As well as randomly swapping giving players targets
# This'll be a doosy
@app.route("/start_game")
def start_game():
    circle = load_circle()
    for i in circle:
        circle[i] = i
    loops = 0
    while loops < 100:
        indexA = circle.randomindex()
        indexB = circle.randomindex()
        if indexA != indexB:
            circle = dict_swap(indexA, indexB, circle)
        loops += 1
    save_circle(circle)
    return render_template("/game_started")


# Here is the method to swap people in the dictionary
def dict_swap(indexA, indexB, dictionary):
    circle = dictionary
    temp_storeA = circle[indexA]
    temp_storeB = circle[indexB]
    circle[indexA] = temp_storeB
    circle[indexB] = temp_storeA
    return circle
