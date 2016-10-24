#!/usr/bin/env python

import urllib
import json
import os
import smtplib

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
    
    msg = "\r\n".join(["From: antonio.porcelli21@gmail.com","To: antonio.porcelli@hotmail.it","Subject: Just a message","","Why, oh why"])
    
    username = 'antonio.porcelli21@gmail.com'
    password = 'pURCELL210174@'
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    #server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    
    result = req.get("result")
    parameters = result.get("parameters")
    descrizione = parameters.get("descrizione")
    cliente = parameters.get("cliente")
    prodotto = parameters.get("prodotto")

    #cost = {'Europe':200, 'North America':300, 'South America':400, 'Asia':500, 'Africa':600}
    #'AO Colli':200, 'AOU Federico II':300, 'AOU Ruggi':400, 'ASL Salerno':500, 'Soresa':600, 'Santobono':700, 'Pascale':800, 'ASL Caserta':900
    
    numtck = {'AO Colli':127892, 'AOU Federico II':871865, 'AOU Ruggi':787265, 'ASL Salerno':902876, 'Soresa':276734, 'Santobono':676754, 'Pascale':878971, 'ASL Caserta':897654}
    
    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech = "In questo momento non posso aiutarla. Ho aperto il ticket n." + str(numtck[cliente]) + " per il Cliente " + cliente + " sul prodotto/servizio " + prodotto + " con la seguente descrizione '" + descrizione + "'.Posso fare altro?"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
