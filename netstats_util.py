from flask import Flask, render_template, Response, make_response
import json
import subprocess

app = Flask(__name__)


def digCMD(param):
    try:
        output = subprocess.check_output(['dig', '+noall', '+answer', param])
        return json.dumps(output.decode('utf-8'))
    except subprocess.CalledProcessError:
        raise


def tracerouteCMD(param):
    try:
        output = subprocess.check_output(['traceroute', param])
        return json.dumps(output.decode('utf-8'))
    except subprocess.CalledProcessError:
        raise


def whoisCMD(param):
    try:
        output = subprocess.check_output(['whois', param])
        return json.dumps(output.decode('utf-8'))
    except subprocess.CalledProcessError:
        raise


def pingCMD(n, param, s):
    try:
        output = subprocess.check_output(['ping', '-c', n, '-s', s, param])
        return json.dumps(output.decode('utf-8'))
    except subprocess.CalledProcessError:
        raise


@app.route('/dig')
@app.route('/dig/<label>')
def dig(label='-h'):
    return digCMD(label)


@app.route('/traceroute/<label>')
def traceroute(label=''):
    return tracerouteCMD(label)


@app.route('/whois/<label>')
def whois(label=''):
    return whoisCMD(label)


@app.route('/ping/<label>/<n>/<s>')
def ping(n=1, label='', s=56):
    return pingCMD(n, label, s)

with open('./log', 'a+') as log:
    try:
        app.run(threaded=True, host='0.0.0.0', port=8000,
                ssl_context='adhoc', debug=True)
        log.write("done adding wsgi app\n")
    except Exception as e:
        log.write(repr(e))
