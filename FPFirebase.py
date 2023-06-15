import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import smsService as smss

def initializeFirestoreApp():
    cred = credentials.Certificate("./Keys/Firebase-Key.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

def generateUserJSON(UserName, UserPhoneNumber, UserNumberPlates):
    return {
        "UserName": UserName,
        "UserBalance": 0,
        "UserPhoneNumber": UserPhoneNumber,
        "UserNumberPlates": UserNumberPlates
    }

def generateTicketJSON(TicketCharge, TicketLocation, TicketNumberPlate):
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%d-%m-%Y, %H:%M:%S")

    return {
        "TicketCharge": TicketCharge,
        "TicketLocation": TicketLocation,
        "TicketTimestamp": current_time_str,
        "TicketNumberPlate": TicketNumberPlate
    }      

def addNewUser(userData):
    users_ref = db.collection("Users")
    # users_ref.document("user_id").set(userData)
    users_ref.add(userData)

def addNewTicket(ticketData):
    user_ref = db.collection("Users").where("UserNumberPlates", "array_contains", ticketData["TicketNumberPlate"]).limit(1).get()
    if not user_ref:
        return False

    users_ref = db.collection("Tickets")
    # users_ref.document("user_id").set(userData)
    users_ref.add(ticketData)
    updateUserBalance(ticketData["TicketNumberPlate"], -ticketData["TicketCharge"], ticketData)

    return True

def retrieveUserByNumberPlate(numberPlate):
    users_ref = db.collection("Users")
    query = users_ref.where("UserNumberPlates", "array_contains", numberPlate)
    results = query.get()

    for doc in results:
        return doc.to_dict()
    
def retrieveTicketByNumberPlate(numberPlate):
    users_ref = db.collection("Tickets")
    query = users_ref.where("TicketNumberPlate", "==", numberPlate)
    results = query.get()
    docs = []
    for doc in results:
        docs.append(doc.to_dict())

    return docs

def updateUserBalance(numberPlate, changeInBalance, ticketData=None):
    users_ref = db.collection("Users")
    query = users_ref.where("UserNumberPlates", "array_contains", numberPlate)
    results = query.get()
    
    for doc in results:
        user = doc.to_dict()
        userId = doc.id
        break
    
    currentBalance = user["UserBalance"]
    user_ref = users_ref.document(userId)
    user_ref.update({'UserBalance': currentBalance + changeInBalance})

    if(ticketData == None):
        message = "Rs." + str(changeInBalance) + " added to your account. New balance: " + str(currentBalance + changeInBalance)
    else:
        message = "Thank you for using Fast Pass. You were charged " + str(ticketData["TicketCharge"]) + " at " + str(ticketData["TicketLocation"]) + " on " + str(ticketData["TicketTimestamp"]) + " for your car " + str(ticketData["TicketNumberPlate"])

    smss.createSMS(user["UserPhoneNumber"], message)

db = initializeFirestoreApp()
# updateUserBalance("MH15TC554", 1000)
# ticket = generateTicketJSON(100, "Mulund", "MH15TC554")
# added = addNewTicket(ticket)
# print(added)