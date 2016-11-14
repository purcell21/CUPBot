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
    if req.get("result").get("action") != "RAGA.sendINFO":
        return  {}
    
        # recupero richiesta
        result = req.get("result")
        parameters = result.get("parameters")
        
        # recupero parametri del metodo RAGA.sendINFO
        mailTo = parameters.get("indirizzoMail")
        numeroRichiesta=parameters.get("numeroRichiesta")
        
        #inizio invio e-mail 
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText

        fromaddr = "sdesk371@gmail.com"
        toaddr = mailTo

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "So.Re.Sa - Richiesta di Autorizzazione Gara in Autonomia n." + numeroRichiesta
        body = "Salve, la richiesta di autorizzazione in oggetto è nello stato di lavorazione. Quanto prima i funzionari So.Re.Sa le risponderanno."
        
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
     "source": "soresapersonalassistant"
}
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
