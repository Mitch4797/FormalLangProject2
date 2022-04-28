#Mitchell humphries
#This is my python Script to inturprit numebrs
##################################################
#Imports
import time #Used for trouble Shooting.

##################################################
#Enum State Class
from multiprocessing.connection import wait

class STATE:
    DONE = -1

    ERROR = 0
    START = 1

    INTEGERFIRST = 2
    INTEGER = 3
    INTERGERUNDER = 4 #Integer part underscore

    DECIMALNOINT = 13
    DECIMALFIRST = 5
    DECIMAL = 6
    DECIMALUNDER = 7 #Decimal part underscore
    
    EXPONENTSIGN = 11
    EXPONENTFIRST =  8
    EXPONENT = 9
    EXPONENTUNDER = 10 #exponent part underscore

    FORCEDEND = 12

###################################################
def getPrecedence(charInput):
    match charInput:
        case '+':
            return 1
        case '-':
            return 1
        case '*':
            return 2
        case '/':
            return 2
        case '^':
            return 3
    #print("Operation Checked When Not Present")
    return 0

def isOperation(c):
    if c=='+'or c=='-' or c=='/'or c =='*' or c=='^':
        return True
    else:
        return False

def preformOperation(a,b,operation):
    match operation:

        case '+':
            #print("Operation Preformed: + ")
            return (a + b)
        case '-':
            #print("Operation Preformed: - ")
            return (a - b)
        case '*':
            #print("Operation Preformed: * ")
            return (a*b)
        case '/':
            #print("Operation Preformed: / ")
            if a == 0:
                return "Divide by zero Error"
            else:
                return (a/b)
        case '^':
            #print("Operation Preformed: ^")
            return (a**b)
    return("No Match In preform operation")

###################################################
    
#List of non acceptable states 
NOTACCEPT = [STATE.ERROR, STATE.INTEGER, STATE.INTERGERUNDER, STATE.DECIMALNOINT, STATE.DECIMALUNDER, STATE.EXPONENTUNDER, STATE.FORCEDEND]
ENDCHAR = ['*', '/', '+', '-', '^', ')', '(', ' ']

##################################################
def stringInterpreter(inputString):

    floatStack = []
    operationsStack = []

    ##############################################
    #For State
    i = 0
    currentState = STATE.START

    #Enter Loop to start solving
    while i < len(inputString):
        currentCharcter = inputString[i]

        if(currentCharcter == ' '):
            i = i + 1
            continue

        elif currentCharcter.isdigit() or currentCharcter == '.':
            inNumber = True
            
            #for base
            sign = 1
            value = 0
            power = 0.1

            #fpr exp
            exponent = 0
            expSign = 1
            currentState = STATE.START

            while(inNumber):

                match currentState:
                    #Start State
                    case STATE.START:
                        if currentCharcter == '.':
                            power = 0.1
                            currentState = STATE.DECIMALNOINT
                        elif currentCharcter.isdigit():
                            value = ord(currentCharcter) - ord('0')
                            currentState = STATE.INTEGER
                        ########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        #########
                        else:
                            currentState = STATE.ERROR

                    #Integer Portion
                    case STATE.INTEGER:
                        if currentCharcter == '.':
                            power = 0.1
                            currentState = STATE.DECIMALFIRST
                        elif currentCharcter == '_':
                            currentState = STATE.INTERGERUNDER
                        elif currentCharcter.isdigit():
                            value = 10 * value + ord(currentCharcter) - ord('0')
                        elif currentCharcter == 'e' or currentCharcter == 'E':
                            currentState = STATE.EXPONENTSIGN
                        elif currentCharcter =='f' or currentCharcter == 'F':
                            currentState = STATE.DONE
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    case STATE.INTERGERUNDER:
                        if currentCharcter.isdigit():
                            value = 10 * value + ord(currentCharcter) - ord('0')
                            currentState = STATE.INTEGER
                        elif currentCharcter == '_':
                            pass
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    #Decimal Portion
                    case STATE.DECIMALNOINT:
                        if currentCharcter.isdigit():
                            value = value + power * (ord(currentCharcter) - ord('0'))
                            power = power/10 
                            currentState = STATE.DECIMAL
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR               

                    case STATE.DECIMALFIRST:
                        if currentCharcter.isdigit():
                            value = value + power * (ord(currentCharcter) - ord('0'))
                            power = power/10 
                            currentState = STATE.DECIMAL
                        elif currentCharcter == 'e' or currentCharcter == 'E':
                            currentState = STATE.EXPONENTSIGN
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    case STATE.DECIMAL:
                        if currentCharcter.isdigit():
                            value = value + power * (ord(currentCharcter) - ord('0'))
                            power = power/10
                        elif currentCharcter == '_':
                            currentState = STATE.DECIMALUNDER
                        elif currentCharcter == 'e' or currentCharcter == 'E':
                            currentState = STATE.EXPONENTSIGN
                        elif currentCharcter =='f' or currentCharcter == 'F':
                            currentState = STATE.DONE
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.DONE
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    case STATE.DECIMALUNDER:
                        if currentCharcter.isdigit():
                            value = value + power * (ord(currentCharcter) - ord('0'))
                            power = power/10
                            currentState = STATE.DECIMAL
                        elif currentCharcter == '_':
                            pass
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    #Exponent Portion
                    case STATE.EXPONENTSIGN:
                        if currentCharcter == '-':
                            expSign = -1
                            currentState = STATE.EXPONENTFIRST
                        elif currentCharcter == '+':
                            expSign = 1
                            currentState = STATE.EXPONENTFIRST
                        elif currentCharcter.isdigit():
                            exponent = ( ord(currentCharcter) - ord('0') )
                            currentState = STATE.EXPONENT
                        else:
                            currentState = STATE.ERROR

                    case STATE.EXPONENTFIRST:
                        if currentCharcter.isdigit():
                            exponent = ( ord(currentCharcter) - ord('0') )
                            currentState = STATE.EXPONENT
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.DONE
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    case STATE.EXPONENT:
                        if currentCharcter.isdigit():
                            exponent = 10 * exponent + (ord(currentCharcter) - ord('0'))
                        elif currentCharcter =='f' or currentCharcter == 'F':
                            currentState = STATE.DONE
                        elif currentCharcter == '_':
                            currentState = STATE.EXPONENTUNDER
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.DONE
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                    case STATE.EXPONENTUNDER:
                        if currentCharcter.isdigit():
                            exponent = 10 * exponent + (ord(currentCharcter) - ord('0'))
                            currentState = STATE.EXPONENT
                        elif currentCharcter =='_':
                            pass
                        #########
                        elif currentCharcter in ENDCHAR:
                            currentState = STATE.ERROR
                            i = i-1
                        ########
                        else:
                            currentState = STATE.ERROR

                #CHECK IF IN ERROR STATEMENT
                if(currentState == STATE.DONE):
                    inNumber = False

                if currentState == STATE.ERROR:
                    floatStack.append("ERROR, Invalid Form-STATE.ERROR" )
                    inNumber = False

                    #Handle Finishing/Done Statß
                elif(i + 1 >= len(inputString) or currentState == STATE.DONE):
                    #If in there states, do NOT ACCEPT
                    if(currentState in NOTACCEPT):    
                        floatStack.append("ERROR, Invalid Form-NOT IN ACCEPT")
                    else:
                        floatStack.append( sign * value * pow(10,(expSign * exponent )))

                    inNumber = False
                else:
                    i = i + 1
                    currentCharcter = inputString[i]
                    

             #Marks end of InNumber ###########################

        elif currentCharcter == '(':
            operationsStack.append(currentCharcter)

        elif currentCharcter == ')':

            while operationsStack[-1] != '(' and len(operationsStack) !=0 :
                num2 = floatStack[-1]
                floatStack.pop()
                num1 = floatStack[-1]
                floatStack.pop()
                operation = operationsStack[-1]
                operationsStack.pop()
                result = preformOperation(num1,num2,operation)
                floatStack.append(result)

            operationsStack.pop()

        #elif isOperation(currentCharcter):
        else:

            while(len(operationsStack) != 0 and getPrecedence(currentCharcter) <= getPrecedence(operationsStack[-1])):
                num2 = floatStack[-1]
                floatStack.pop()
                num1 = floatStack[-1]
                floatStack.pop()
                operation = operationsStack[-1]
                operationsStack.pop()
                result = preformOperation(num1,num2,operation)
                floatStack.append(result)

            operationsStack.append(currentCharcter)

        #Increment i 
        i = i + 1
    
    while( operationsStack ):
        num2 = floatStack[-1]
        floatStack.pop()
        num1 = floatStack[-1]
        floatStack.pop()
        operation = operationsStack[-1]
        operationsStack.pop()
        result = preformOperation(num1,num2,operation)
        floatStack.append(result)

    return floatStack[-1]
        

##################################################

#To Run Program
print("Mitchell H. Calculator.")
print("Type 'exit' or 'q' to close program.")

while True:
    inputString = input("Please enter input String:")

    if inputString == "exit" or inputString == "Exit" or inputString == "q":
        break
    
    try:
        #print("Tried")
        newNum = stringInterpreter(inputString)
        print(newNum)
    except:
        print("Error, invalid Form")

