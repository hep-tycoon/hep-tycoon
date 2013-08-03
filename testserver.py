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

@app.route('/')
def index():
    return redirect('/frontend/index.html')

@app.route('/time')
def time():
    return jsonify(**{
        'time': gamemanager.start_time
    })

@app.route('/hr/scientists/')
def list_scientists():
    return jsonify(**{
        'max_scientists': hr.max_scientists,
        'scientists': map(str, hr.scientists)
    })

@app.route('/hr/hire/<float:salary>/<int:n>')
def hire_scientists(salary, n):
    hired = hr.hire(salary, n)
    return jsonify(**{
        'salary': salary,
        'n': n,
        'hired': hired
    })

@app.route('/hr/fire/<int:n>')
def fire_scientists(n):
    fired, penalty = hr.fire(n)
    return jsonify(**{
        'n': n,
        'fired': fired,
        'penalty': penalty
    })

@app.route("/hr/salary/<float:newsalary>")
def set_salary(newsalary):
    assert newsalary >= 0
    for scientist in hr.scientists:
        scientist.salary = newsalary
    return jsonify()

@app.route("/accelerator")
def get_accelerator():
    return jsonify(**gamemanager.accelerator.json())


@app.route("/accelerator/shutdown")
def shutdown_accelerator():
    gamemanager.accelerator_stop()
    return jsonify()

@app.route("/accelerator/poweron")
def poweron_accelerator():
    gamemanager.accelerator_start()
    return jsonify()

@app.route("/accelerator/upgrade")
def upgrade_accelerator():
    gamemanager.accelerator_upgrade()
    return jsonify()

@app.route("/datacenter")
def get_datacenter():
    return jsonify(**gamemanager.data_centre.json())

@app.route("/detectors")
def get_detectors():
    detectors = gamemanager.accelerator.detectors

    all_detectors = set(technology.query_tech_tree(["detectors"]).keys())
    installed = set([d.slug for d in detectors])
    avaliable = all_detectors.difference(installed)

    return jsonify(
        detectors=[d.json() for d in detectors],
        max_detectors=gamemanager.accelerator.slots,
        free_slots=gamemanager.accelerator.free_slots,
        available=[technology.from_tech_tree("detectors", d, 0).json() for d in avaliable],
    )

@app.route("/detector/<detector>/upgrade")
def upgrade_detector(detector):
    gamemanager.detector_upgrade(detector)
    return jsonify()

@app.route("/detector/<detector>/remove")
def remove_detector(detector):
    gamemanager.detector_remove(detector)
    return jsonify()

@app.route("/detector/<detector>/add")
def buy_detector(detector):
    gamemanager.detector_buy(detector)
    return jsonify()

@app.route("/datacenter/upgrade")
def upgrade_datacenter():
    gamemanager.datacentre_upgrade()
    return jsonify()

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
