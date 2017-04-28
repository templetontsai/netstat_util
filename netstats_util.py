from flask import Flask, render_template, Response, make_response, request
import json
import subprocess

app = Flask(__name__)


def digCMD(param):
    try:
        output = subprocess.check_output(
            ['dig', '+noall', '+answer', '+short', param]).decode('utf-8')

        output = output.split('\n')[:-1]

        return json.dumps(output)
    except subprocess.CalledProcessError:
        raise


def digBatchCMD(jsonObj):
    try:
        domainList = jsonObj['domainName']

        outputIPList = []
        for i in domainList:

            output = subprocess.check_output(
                ['dig', '+noall', '+answer', '+short', i]).decode('utf-8')
            output = output.split('\n')[:-1]

            outputIPList.append({'domain': i, 'ip': output})

        '''
        with open('batch_dig.txt', 'w') as f:
            for i in domainList:
                f.write(i + '\n')
        output = subprocess.check_output(
            ['dig', '+noall', '+answer', '+short', '-f', 'batch_dig.txt']).decode('utf-8')
        output = output.split('\n')
        '''

        return json.dumps(outputIPList)
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


@app.route('/digbatch', methods=['GET', 'POST'])
def digbatch():
    return digBatchCMD(request.get_json(force=True, cache=True))


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
        app.run(threaded=True, host='0.0.0.0', port=8000, debug=True)
        log.write("done adding wsgi app\n")
    except Exception as e:
        log.write(repr(e))
