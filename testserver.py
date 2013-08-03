"""
    A minimal server for testing stuff.
"""

from flask import Flask, jsonify

app = Flask('HEP Tycoon Testserver', static_folder="frontend")

# testing the hr
from backend.hr import HR
hr = HR(100)

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

if __name__ == '__main__':
    app.run()
