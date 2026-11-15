from flask import Flask, send_from_directory, request, jsonify
import secrets
import string

app = Flask(__name__)

rooms = {}
leaderboard = {}

def get_name(value):
    name = str(value or "Игрок").strip()[:20]
    return name or "Игрок"

@app.route("/")
def home():
    return send_from_directory("web", "index.html")

@app.route("/api/create", methods=["POST"])
def create_room():
    data = request.json or {}
    name = get_name(data.get("name"))

    code = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(6)
    )

    rooms[code] = {
        "players": [name],
        "numbers": [],
        "winner": None,
        "status": "waiting"
    }

    if name not in leaderboard:
        leaderboard[name] = {"points": 0, "wins": 0}

    return jsonify({"room": code})

@app.route("/api/join", methods=["POST"])
def join_room():
    data = request.json or {}
    code = data.get("room", "").upper()
    name = get_name(data.get("name"))

    if code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    room = rooms[code]

    if len(room["players"]) >= 2:
        return jsonify({"error": "Комната заполнена"}), 400

    room["players"].append(name)

    for player in room["players"]:
        if player not in leaderboard:
            leaderboard[player] = {"points": 0, "wins": 0}

    room["numbers"] = [
        secrets.randbelow(25),
        secrets.randbelow(25)
    ]

    room["status"] = "finished"

    if room["numbers"][0] > room["numbers"][1]:
        room["winner"] = 0
    elif room["numbers"][1] > room["numbers"][0]:
        room["winner"] = 1

    if room["winner"] is not None:
        winner_name = room["players"][room["winner"]]
        leaderboard[winner_name]["points"] += 1
        leaderboard[winner_name]["wins"] += 1

    return jsonify({"status": "joined"})

@app.route("/api/state")
def room_state():
    code = request.args.get("room", "").upper()

    if code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    room = rooms[code]

    return jsonify({
        "players": room["players"],
        "status": room["status"],
        "numbers": room["numbers"],
        "winner": room["winner"]
    })

@app.route("/api/leaderboard")
def get_leaderboard():
    ranking = sorted(
        leaderboard.items(),
        key=lambda x: (x[1]["wins"], x[1]["points"]),
        reverse=True
    )

    return jsonify([
        {
            "name": name,
            "wins": stats["wins"],
            "points": stats["points"]
        }
        for name, stats in ranking[:10]
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
