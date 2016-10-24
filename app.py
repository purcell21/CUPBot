#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "ticket.open":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    cliente = parameters.get("cliente")
    prodottto = parameters.get("prodotto")
    descrizione = parameters.get("descrizione")

    tckNumbers = {'AO Colli':178934, 'ASL Salerno':789876}
    
    speech = "In questo momento non riesco ad aiutarla. Ho comunque aperto il ticket n. " + str(tckNumbers[cliente]) + " sul Cliente " + cliente + "per il prodotto " + prodotto + " e per il seguente problema  " + descrizione + ".Entro poche ore sarà contattato. Posso fare altro?"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-engServiceDesk"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
