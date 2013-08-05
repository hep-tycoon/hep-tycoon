"""
    A minimal server for testing stuff.
"""

from flask import Flask, jsonify, redirect
from backend import technology
from backend.game_manager import GameManager
from backend.ht_exceptions import BankruptcyException
from functools import wraps

app = Flask('HEP Tycoon Testserver', static_folder="frontend")
app.debug = True
gamemanager = None
hr = None

def jsonres(**obj):
    return jsonify(
        response=obj,
        gameStatus={
            "accelerator_running": gamemanager.accelerator_running,
            "funds": gamemanager.funds,
            "grant_bar": int(gamemanager.grant_bar),
            "grant_bar_max": gamemanager.level.publication_target,
            "grant_bar_price": gamemanager.level.grant,
            "storage_used": gamemanager.data_centre.storage_used,
            "storage_capacity": gamemanager.data_centre.storage_capacity,
            "events": gamemanager.events(),
        }
    )

def view(route):
    def decorator(viewfn):
        @wraps(viewfn)
        def __inner__(*args, **kwargs):
            try:
                return viewfn(*args, **kwargs)
            except BankruptcyException:
                gamemanager.event("bankruptcy");
                return jsonres()
        return app.route(route)(__inner__)

    return decorator


@view('/')
def index():
    return redirect('/frontend/config.html')

@view('/init_game/<type>/<partitles>/<name>')
def init(name, type, partitles):
    global gamemanager, hr
    gamemanager = GameManager(name, type, partitles)
    hr = gamemanager.hr_manager
    return redirect('/frontend/game.html')

@view("/trigger")
def trigger():
    gamemanager.process_events()
    return jsonres()

@view('/time')
def time():
    return jsonres(**{
        'time': gamemanager.start_time
    })

@view('/funds')
def funds():
    return jsonres(**{
        'funds': gamemanager.funds
    })

@view('/hr/scientists/')
def list_scientists():
    return jsonres(**{
        'max_scientists': hr.max_scientists,
        'scientists': map(str, hr.scientists)
    })

@view('/hr/hire/<int:n>')
def hire_scientists(n):
    hired = gamemanager.hr_hire(n)
    return jsonres(**{
        'n': n,
        'hired': hired
    })

@view('/hr/fire/<int:n>')
def fire_scientists(n):
    fired, penalty = hr.fire(n)
    return jsonres(**{
        'n': n,
        'fired': fired,
        'penalty': penalty
    })

@view("/hr/salary/<float:newsalary>")
def set_salary(newsalary):
    assert newsalary >= 0
    for scientist in hr.scientists:
        scientist.salary = newsalary
    return jsonres()

@view("/accelerator")
def get_accelerator():
    return jsonres(**gamemanager.accelerator.json())


@view("/accelerator/shutdown")
def shutdown_accelerator():
    gamemanager.accelerator_stop()
    return jsonres()

@view("/accelerator/poweron")
def poweron_accelerator():
    gamemanager.accelerator_start()
    return jsonres()

@view("/accelerator/upgrade")
def upgrade_accelerator():
    gamemanager.accelerator_upgrade()
    return jsonres()

@view("/datacenter")
def get_datacenter():
    return jsonres(**gamemanager.data_centre.json())

@view("/detectors")
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

@view("/detector/<detector>/upgrade")
def upgrade_detector(detector):
    gamemanager.detector_upgrade(detector)
    return jsonres()

@view("/detector/<detector>/remove")
def remove_detector(detector):
    gamemanager.detector_remove(detector)
    return jsonres()

@view("/detector/<detector>/add")
def buy_detector(detector):
    gamemanager.detector_buy(detector)
    return jsonres()

@view("/datacenter/upgrade")
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
    print(json.dumps(methods))

#methods_json()
if __name__ == '__main__':
    app.run(host="0.0.0.0")
