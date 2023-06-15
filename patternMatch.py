def matchPattern(text):
    text = text.replace(" ", "")
    
    stateCodes = ['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'DN', 'DD', 'DL', 
        'GA', 'GJ', 'HR', 'HP', 'JK', 'KA', 'KL', 'LD', 'MP', 'MH', 'MN', 
        'ML', 'MZ', 'NL','OR', 'PY', 'PN', 'RJ', 'SK', 'TN', 'TR', 'UP', 'WB']

    if not(len(text) == 10):
        # print("Length")
        return False
    elif text[0:2] not in stateCodes:
        # print(text[0:2])
        # print("State code")
        return False
    elif not (text[2:4]).isnumeric():
        # print("Area code")
        return False
    elif (text[4:6]).isnumeric():
        # print("Plate code")
        return False
    elif not (text[6:10]).isnumeric():
        # print("Plate Number")
        return False
    else:
        return True

def fixStateCode(text):
    return text