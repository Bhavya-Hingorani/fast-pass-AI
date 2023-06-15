from twilio.rest import Client

def initializeTwilioApp():
    account_sid = 'ACb5cf883dc6469af60d36638736dc7f51'
    auth_token = 'f2c9e4c8a4dd806a937247d262d02a95'
    return Client(account_sid, auth_token)

def createSMS(reci, bodyMessage):
    recipient = reci # replace with recipient's phone number
    message = client.messages.create(
        to=recipient,
        from_='+15076186770',
        body=bodyMessage
    )


client = initializeTwilioApp()
# createSMS("+918451839119")
