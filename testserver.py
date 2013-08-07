"""
    A minimal server for testing stuff.
"""

from flask import Flask, jsonify, redirect, request
from backend import technology
from backend.game_manager import GameManager
from backend.ht_exceptions import BankruptcyException
from functools import wraps

app = Flask('HEP Tycoon Testserver', static_folder="frontend")
app.debug = True

def jsonres(**obj):
    return jsonify(
        response=obj,
        gameStatus={
            "funds": gs().funds,
            "grant_bar": int(gs().grant_bar),
            "grant_bar_max": gs().level.publication_target,
            "grant_bar_price": gs().level.grant,
            "storage_used": gs().data_centre.storage_used,
            "storage_capacity": gs().data_centre.storage_capacity,
            "events": gs().events(),
        }
    )

gamemanager_i = 0
gamemanagers = {}
def gs():
    gm = request.cookies.get("gm")
    return gamemanagers[int(gm)]


def view(route):
    def decorator(viewfn):
        @wraps(viewfn)
        def __inner__(*args, **kwargs):
            try:
                if request.cookies.get("gm") is None:
                    return redirect("/")
                return viewfn(*args, **kwargs)
            except BankruptcyException:
                gs().event("bankruptcy");
                return jsonres()
        return app.route(route)(__inner__)
    return decorator


@app.route('/')
def index():
    return redirect('/frontend/config.html')

@app.route('/init_game/<type>/<partitles>/<name>')
def init(name, type, partitles):
    global gamemanager_i, gamemanagers
    gamemanager_i += 1
    gamemanager = GameManager(name, type, partitles)
    gamemanagers[gamemanager_i] = gamemanager
    resp = redirect('/frontend/game.html')
    resp.set_cookie("gm", gamemanager_i)
    return resp

@view("/trigger")
def trigger():
    gs().process_events()
    return jsonres()

@view('/time')
def time():
    return jsonres(**{
        'time': gs().start_time
    })

@view('/funds')
def funds():
    return jsonres(**{
        'funds': gs().funds
    })

@view('/hr/scientists/')
def list_scientists():
    return jsonres(**{
        'max_scientists': gs().hr_manager.max_scientists,
        'scientists': map(str, gs().hr_manager.scientists)
    })

@view('/hr/hire/<int:n>')
def hire_scientists(n):
    hired = gs().hr_hire(n)
    return jsonres(**{
        'n': n,
        'hired': hired
    })

@view('/hr/fire/<int:n>')
def fire_scientists(n):
    fired, penalty = gs().hr_manager.fire(n)
    return jsonres(**{
        'n': n,
        'fired': fired,
        'penalty': penalty
    })

@view("/hr/salary/<float:newsalary>")
def set_salary(newsalary):
    assert newsalary >= 0
    for scientist in gs().hr_manager.scientists:
        scientist.salary = newsalary
    return jsonres()

@view("/accelerator")
def get_accelerator():
    return jsonres(**gs().accelerator.json())


@view("/accelerator/shutdown")
def shutdown_accelerator():
    gs().accelerator_stop()
    return jsonres()

@view("/accelerator/poweron")
def poweron_accelerator():
    gs().accelerator_start()
    return jsonres()

@view("/accelerator/upgrade")
def upgrade_accelerator():
    gs().accelerator_upgrade()
    return jsonres()

@view("/datacenter")
def get_datacenter():
    return jsonres(**gs().data_centre.json())

@view("/detectors")
def get_detectors():
    detectors = gs().accelerator.detectors

    all_detectors = set(technology.query_tech_tree(["detectors"]).keys())
    installed = set([d.slug for d in detectors])
    avaliable = all_detectors.difference(installed)

    return jsonres(
        detectors=[d.json() for d in detectors],
        max_detectors=gs().accelerator.slots,
        free_slots=gs().accelerator.free_slots,
        available=[technology.from_tech_tree("detectors", d, 0).json() for d in avaliable],
    )

@view("/detector/<detector>/upgrade")
def upgrade_detector(detector):
    gs().detector_upgrade(detector)
    return jsonres()

@view("/detector/<detector>/remove")
def remove_detector(detector):
    gs().detector_remove(detector)
    return jsonres()

@view("/detector/<detector>/add")
def buy_detector(detector):
    gs().detector_buy(detector)
    return jsonres()

@view("/datacenter/upgrade")
def upgrade_datacenter():
    gs().datacentre_upgrade()
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
