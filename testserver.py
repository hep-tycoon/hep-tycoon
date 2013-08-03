"""
    A minimal server for testing stuff.
"""

from flask import Flask, jsonify

app = Flask('HEP Tycoon Testserver', static_folder="frontend")
app.debug = True

# testing the game manager
from backend.game_manager import GameManager

gamemanager = GameManager('My cool lab', 'linear', 'ee')
hr = gamemanager.hr_manager  # just for testing, later we should use only the game manager

@app.route('/')
def index():
    test = {'name': 'Peter', 'lastname': 'Petersen'}
    return jsonify(**test)

@app.route('/hr/scientists/')
def list_scientists():
    return jsonify(**{
        'num_scientists': hr.num_scientists,
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
    return jsonify()

@app.route("/accelerator/poweron")
def poweron_accelerator():
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
    return jsonify(detectors=detectors)

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
