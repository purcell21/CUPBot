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

def ticketOpen(req):
    result = req.get("result")
    print(result)

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
    body = "Aperto ticket n." + str(numtck[cliente]) + " sul prodotto/servizio " + prodotto + " con la seguente descrizione '" + descrizione + "'.Posso fare altro?"
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

def invioCodiceAccesso(req):
    result = req.get("result")
    print(result)

    parameters = result.get("parameters")

    email = parameters.get("indirizzoMail")
    nominativoRup = parameters.get("nominativo-rup")
    nomeUtente= parameters.get("nomeUtente")

    #inizio invio e-mail 
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    numCodice = {'Palma Romano':127892, 'Mario Rossi':871865}
    indirizziMail= {'Palma Romano':"antonio.porcelli@hotmail.it", 'Mario Rossi':"antonio.porcelli21@gmail.com"}
    
    fromaddr = "sdesk371@gmail.com"
    toaddr = str(indirizziMail[nominativoRup])

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "no-replay: So.Re.Sa SpA - Richiesta di Autorizzazione Gara - invio codice di accesso "
    body = "Gentile " + nomeUtente + " questo e' il codice di accesso per l'autorizzazione al servizio: " + str(numCodice[nominativoRup])
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ServiceDesk21")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    #fine invio e-mail 
    
    speech ="Bene. Hai chiesto di avere informazioni circa la pratica di autorizzazione di espletamento gara in autonomia per il RUP (o funzionario di riferimento) " + nominativoRup + ".Ho appena inviato una e-mail all'indirizzo associato al riferimento " + nominativoRup + ".Inserisci il codice cosi' posso autorizzarti ad accedere alla documentazione richiesta."
        
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "soresapersonalassistant"
    }

def invioRiepilogoRichiesta(req):
    result = req.get("result")
    print(result)

    parameters = result.get("parameters")
    email = parameters.get("indirizzoMail")
    nomeUtente = parameters.get("nomeUtente")
    
    #inizio invio e-mail 
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    
    fromaddr = "sdesk371@gmail.com"
    toaddr = email
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "no-replay: ASL di Lecce - Servizio di Prenotazione CUP - Riepilogo Richiesta Prenotazione"
    body = "Gentile " + nomeUtente + " con la presente comunichiamo l'avvenuta prenotazione della visita specialistica. Di seguito un riepilogo della richiesta:"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ServiceDesk21")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    #fine invio e-mail 
    
    speech ="Perfetto. Ti ho inviato una e-mail all'indirizzo " + toaddr + " contenente il riepilogo della richista di prenotazione."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "aslleccecupbot"
    }

def invioViaEmailRAGA(req):
    result = req.get("result")
    print(result)

    parameters = result.get("parameters")
    email = parameters.get("indirizzoMail")
    numeroPratica = parameters.get("numeroPratica")
    nominativoRup = parameters.get("nominativoRup")
    nomeUtente = parameters.get("nomeUtente")
    
    #inizio invio e-mail 
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    
    fromaddr = "sdesk371@gmail.com"
    toaddr = email
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "no-replay: So.Re.Sa SpA - Richiesta di Autorizzazione Gara - numero protocollo " + numeroPratica
    body = "Gentile " + nomeUtente + " come richiesto ti comunichiamo che la pratica in oggetto e' in lavorazione"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ServiceDesk21")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    #fine invio e-mail 
    
    speech ="Perfetto. La pratica di cui hai richiesto informazioni, risulta essere presa in carico dai funzionari della SoReSa. Ti ho inviato una e-mail all'indirizzo " + toaddr + " con tutte informazioni legate alla pratica  numero " + numeroPratica + "."
    #speech ="Le ho appena inviato la nuova password all'indirizzo email:" + email + ". La cambi al primo accesso."
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "soresapersonalassistant"
    }
def makeWebhookResult(req): 
    if req.get("result").get("action") == "ticket.open":return ticketOpen(req)
    elif req.get("result").get("action") == "RAGA.invioInfo":return invioViaEmailRAGA(req) 
    elif req.get("result").get("action") == "RAGA.invioCodiceAccesso":return invioCodiceAccesso(req) 
    elif req.get("result").get("action") == "CUP.invioRiepilogoRichiesta":return invioRiepilogoRichiesta(req) 
    else:return  {}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
