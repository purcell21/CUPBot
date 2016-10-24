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

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # me == my email address
    # you == recipient's email address
    me = "antonio.porcelli21@email.com"
    you = "antonio.porcelli@hotmail.it"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = """\
        <html>
            <head></head>
                <body>
                    <p>Hi!<br>How are you?<br> Here is the <a href="https://www.python.org">link</a> you wanted.</p>
                </body>
            </html>
        """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
   
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
