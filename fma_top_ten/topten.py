import db_helper
from flask import Flask, render_template, jsonify, request

from db_helper import add_new_tourn_data

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add")
def add_result():
    return render_template("add_entry.html")

@app.route("/view_results")
def view_results():
    return render_template("view_data.html")

@app.route("/add_result")
def add_data():
    return render_template("add_entry.html")

@app.route("/api/add_data", methods=["POST"])
def add_tournament_information():
    data = request.get_json()
    print(data)
    add_new_tourn_data(data)
    #return "", 200
    return jsonify({"message": "Data received"}), 200

@app.route("/api/schools")
def populate_schools():
    schools = db_helper.get_schools()
    if len(schools) > 0:
        data = db_helper.school_data_helper(schools)
        return jsonify(data), 200

@app.route("/api/divisions")
def populate_division():
    divisions = db_helper.get_divisions()
    if len(divisions) >0:
        data = db_helper.two_column_helper(divisions)
        return jsonify(data), 200

@app.route("/api/belt_ranks")
def populate_belts():
    belt_ranks = db_helper.get_belt_ranks()
    if len(belt_ranks) >0:
        data = db_helper.two_column_helper(belt_ranks)
        return jsonify(data), 200

@app.route("/api/events")
def populate_events():
    events = db_helper.get_events()
    if len(events) >0:
        data = db_helper.two_column_helper(events)
        return jsonify(data), 200

@app.route("/api/tournaments")
def populate_tournaments():
    tourn = db_helper.get_tournaments()
    if len(tourn) >0:
        data = db_helper.tournament_helper(tourn)
        return jsonify(data), 200

@app.route("/api/topten")
def populate_top_ten():

    top_ten_raw = db_helper.populate_top_ten(request=request)
    if len(top_ten_raw) >0:
        data = db_helper.top_ten_data_helper(top_ten_raw)
        return jsonify(data), 200
    else:
        return [{}], 204

app.run(debug=True)
