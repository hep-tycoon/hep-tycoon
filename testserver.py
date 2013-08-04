"""
    A minimal server for testing stuff.
"""

from flask import Flask, jsonify, redirect
from backend import technology
from backend.game_manager import GameManager

app = Flask('HEP Tycoon Testserver', static_folder="frontend")
app.debug = True

# testing the game manager
gamemanager = GameManager('My cool lab', 'linear', 'ee')
hr = gamemanager.hr_manager  # just for testing, later we should use only the game manager

def jsonres(**obj):
    return jsonify(
        response=obj,
        gameStatus={
            "funds": gamemanager.funds,
            "grant_bar": gamemanager.grant_bar,
            "grant_bar_max": 2000,
            "storage_used": gamemanager.data_centre.storage_used,
            "storage_capacity": gamemanager.data_centre.storage_capacity
        }
    )

@app.route('/')
def index():
    return redirect('/frontend/index.html')

@app.route("/trigger")
def trigger():
    gamemanager.process_events()
    return jsonres()

@app.route('/time')
def time():
    return jsonres(**{
        'time': gamemanager.start_time
    })

@app.route('/funds')
def funds():
    return jsonres(**{
        'funds': gamemanager.funds
    })

@app.route('/hr/scientists/')
def list_scientists():
    return jsonres(**{
        'max_scientists': hr.max_scientists,
        'scientists': map(str, hr.scientists)
    })

@app.route('/hr/hire/<int:n>')
def hire_scientists(n):
    hired = gamemanager.hr_hire(n)
    return jsonres(**{
        'n': n,
        'hired': hired
    })

@app.route('/hr/fire/<int:n>')
def fire_scientists(n):
    fired, penalty = hr.fire(n)
    return jsonres(**{
        'n': n,
        'fired': fired,
        'penalty': penalty
    })

@app.route("/hr/salary/<float:newsalary>")
def set_salary(newsalary):
    assert newsalary >= 0
    for scientist in hr.scientists:
        scientist.salary = newsalary
    return jsonres()

@app.route("/accelerator")
def get_accelerator():
    return jsonres(**gamemanager.accelerator.json())


@app.route("/accelerator/shutdown")
def shutdown_accelerator():
    gamemanager.accelerator_stop()
    return jsonres()

@app.route("/accelerator/poweron")
def poweron_accelerator():
    gamemanager.accelerator_start()
    return jsonres()

@app.route("/accelerator/upgrade")
def upgrade_accelerator():
    gamemanager.accelerator_upgrade()
    return jsonres()

@app.route("/datacenter")
def get_datacenter():
    return jsonres(**gamemanager.data_centre.json())

@app.route("/detectors")
def get_detectors():
    detectors = gamemanager.accelerator.detectors

    all_detectors = set(technology.query_tech_tree(["detectors"]).keys())
    installed = set([d.slug for d in detectors])
    avaliable = all_detectors.difference(installed)

    return jsonres(
        detectors=[d.json() for d in detectors],
        max_detectors=gamemanager.accelerator.slots,
        free_slots=gamemanager.accelerator.free_slots,
        available=[technology.from_tech_tree("detectors", d, 0).json() for d in avaliable],
    )

@app.route("/detector/<detector>/upgrade")
def upgrade_detector(detector):
    gamemanager.detector_upgrade(detector)
    return jsonres()

@app.route("/detector/<detector>/remove")
def remove_detector(detector):
    gamemanager.detector_remove(detector)
    return jsonres()

@app.route("/detector/<detector>/add")
def buy_detector(detector):
    gamemanager.detector_buy(detector)
    return jsonres()

@app.route("/datacenter/upgrade")
def upgrade_datacenter():
    gamemanager.datacentre_upgrade()
    return jsonres()

def methods_json():
    methods = []
    for rule in app.url_map.iter_rules():
        methods.append({
            "url": rule.rule,
            "args": list(rule.arguments),
            "name": rule.endpoint
        })
    import json
    print json.dumps(methods)

methods_json()
if __name__ == '__main__':
    app.run(host="0.0.0.0")
