from enum import Enum

from flask import Blueprint, render_template, request as req, flash, redirect, url_for

from app.data import devs, links
from app.fetch_data import fetch_batsman_data, fetch_bowler_data, fetch_all_rounder_data, fetch_wicket_keeper_data


class PlayerTypes(Enum):
    BATSMAN = "batsman"
    BOWLER = "bowler"
    WICKETKEEPER = "wicketkeeper"
    ALL_ROUNDER = "allrounder"


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template(
        "main/index.html",
        devs=devs,
        years=links.keys()
    )


@bp.route("/player-info")
def player_info():
    year, player_type = req.args.get("year"), req.args.get("player-type")
    all_player_types = [player.value for player in PlayerTypes]
    if year not in links or player_type not in all_player_types:
        flash("Both Year and Player Type are needed and should be valid")
        return redirect(url_for("main.index"))

    return render_template(
        "main/player-info.html",
        devs=devs,
        player_type=player_type,
        year=year
    )


@bp.route("/result", methods=("GET", "POST"))
def result():
    year, player_type = req.form["year"], req.form["player-type"]
    link = links[year]
    match player_type:
        case PlayerTypes.BATSMAN.value:
            data = {
                "avg": req.form["avg"],
                "strike-rate": req.form["strike-rate"],
                "balls-faced": req.form["balls-faced"]
            }
            tabledata = fetch_batsman_data(link[player_type], data)

        case PlayerTypes.ALL_ROUNDER.value:
            data = {
                "wickets-taken": req.form["strike-rate"],
                "economy": req.form["ball-avg"],
                "avg": req.form["bat-avg"]
            }
            tabledata = fetch_all_rounder_data(link["batsman"], link["bowler"], data)

        case PlayerTypes.WICKETKEEPER.value:
            data = {
                "dismissals": req.form["dismissals"],
                "avg": req.form["avg"],
                "strike-rate": req.form["strike-rate"]
            }
            tabledata = fetch_wicket_keeper_data(link['wicketkeeper'], link['batsman'], data)

        case _:
            # bowler data
            data = {
                "wickets-taken": req.form["wickets-taken"],
                "economy": req.form["economy"],
                "avg": req.form["avg"]
            }
            tabledata = fetch_bowler_data(link[player_type], data)

    return render_template("main/results.html", devs=devs, tabledata=tabledata)
