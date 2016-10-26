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
        return  {}
    
        # inizio apertura ticket
        result = req.get("result")
        parameters = result.get("parameters")
        descrizione = parameters.get("descrizione")
        cliente = parameters.get("cliente")
        prodotto = parameters.get("prodotto")

        numtck = {'AO Colli':127892, 'AOU Federico II':871865, 'AOU Ruggi':787265, 'ASL Salerno':902876, 'Soresa':276734, 'Santobono':676754, 'Pascale':878971, 'ASL Caserta':897654}
        speech = "In questo momento non posso aiutarla. Ho aperto il ticket n." + str(numtck[cliente]) + " per il Cliente " + cliente + " sul prodotto/servizio " + prodotto + " con la seguente descrizione '" + descrizione + "'.Posso fare altro?"

        #inizio invio e-mail 
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText

        fromaddr = "sdesk371@gmail.com"
        toaddr = "antonio.porcelli@hotmail.it"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Apertura ticket n." + str(numtck[cliente]) + " - Cliente - " + cliente
        body = "Aperto ticket n." + str(numtck[cliente]) + " sul prodotto/servizio " + prodotto + " con la seguente descrizione '" + descrizione + "'."
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "ServiceDesk21")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        #fine invio e-mail
        print("Response:")
        print(speech)
        
return {
    "speech": speech,
    "displayText": speech,
     #"data": {},
     # "contextOut": [],
     "source": "apiai"
}
     #fine apertura ticke
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
