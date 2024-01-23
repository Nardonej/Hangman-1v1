# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 07:56:15 2023

@authors: Josh Nardone, Giang Do
-"""
import socket
import threading
import time

C1Play = True
C2Play = True
C1 = ""
C2 = ""
RPSC1 = ""
RPSC2 = ""
C1finalGuess = ""
C2FinalGuess = ""
C1Correct = False
C2Correct = False
'''
We are making the guessCount -1 so that when the clinet enters "guess" it 
is not recorded as an actual guess and does not penalize them.
'''
C1GuessCount = -1
C2GuessCount = -1
'''
With the help of the internet and chat gpt we were able to use threading to help us
here the event is used as a pausing mechanism, it waits for the other user when needed
and resumes when it should.
'''
C1Finished = threading.Event()
C2Finished = threading.Event()


    
def willPlay(cs, pPlay, oPlay):
    global C1Play, C2Play
    if pPlay == 'y' and oPlay == 'y':
        cs.send(bytes('Have Fun!', 'utf-8'))
        clearGame()
    else:
        cs.send(bytes('your opponent did not want to play', 'utf-8'))
        C1Play = False  
        C2Play = False
        print("hello?")
        time.sleep(1) # chat gpt helped me troubleshoot this as a solution
        cs.close()
        
        
def handleClient(cs, CID):
    global C1, C2, C1finalGuess, C2FinalGuess, C1GuessCount, C2GuessCount, C1Finished, C2Finished, C1PA, C2PA, C1Correct, C2Correct

    while True:
        playAgain = cs.recv(1024).decode('utf-8')
        print(playAgain)
        if "Client1" in playAgain:
            C1PA = playAgain.split()[-1]
            C1Finished.set()
            C2Finished.wait()
            willPlay(cs,C1PA, C2PA)
            print(C1PA)
            
            
        elif "Client2" in playAgain:
            C2PA = playAgain.split()[-1]
            C2Finished.set()
            C1Finished.wait()
            willPlay(cs,C2PA, C1PA)
            print(C2PA)
    
        while C1Play == True and C2Play == True:
            clientInput = cs.recv(1024).decode('utf-8')
            
            if not clientInput:
                break
            
            if CID == "Client1": # CID stands for Client ID
                C1 = clientInput
                C1Finished.set()
            elif CID == "Client2":
                C2 = clientInput
                C2Finished.set()
        
            C1Finished.wait()
            C2Finished.wait()
            cs.send(bytes('Thank you for submitting a word', 'utf-8'))
            print(clientInput)
            C1Finished.clear()
            C2Finished.clear()
        
            Client1Guess = []
            Client2Guess = []
        
            for _ in range(11):
        
                guessInput = cs.recv(1024).decode('utf-8')
                if CID == "Client1":
                    if guessInput.startswith("Client1: "):
                        guessInput = guessInput[len("Client1: "):]
                        Client1Guess.append(guessInput)
                        C1GuessCount += 1
                elif CID == "Client2":
                    if guessInput.startswith("Client2: "):
                        guessInput = guessInput[len("Client2: "):]
                        Client2Guess.append(guessInput)
                        C2GuessCount += 1
        
                print(f"{CID} guesses: {guessInput}")
        
                guessInput = guessInput.strip()
                print(C1)
                print(C2)
                print(Client1Guess)
                print(Client2Guess)
                print(guessInput)
                print("-------------")
        
                if CID == "Client1":
                    if C2 and guessInput == "guess":
                        cs.send(bytes('please enter the word you would like to guess and wait for your opponent to do the same', 'utf-8'))
                        C1finalGuess = cs.recv(1024).decode('utf-8')
                        print(C2)
                        print("*****")  
                        #We tell the user what we are waiting for
                        C1Finished.set() # this signals that Client1 is done guessing
                     
                        C2Finished.wait()  # resumes the program when Client2 has finished guessing
                        C2Finished.clear()
                        
                        if C1finalGuess == C2:
                            C1Correct = True
                            cs.send(bytes('You guessed the word Correctly', 'utf-8'))
                            determineWinner(cs, C1Correct, C2Correct, CID)
                            break
                        else:
                            cs.send(bytes('Incorrect you lost :(', 'utf-8'))
                        break  # this exits the loop and essentially ends the game
                    if C2.split()[-1] and guessInput.split()[-1] in C2.split()[-1]:
                        cs.send(bytes(f'Letter "{guessInput}" is in the word', 'utf-8'))
                    else:
                        cs.send(bytes(f'Letter  "{guessInput}" IS NOT in the word', 'utf-8'))
        
        
                # Do the same for the other Client
                elif CID == "Client2":
                    if C1 and guessInput == "guess":
                        cs.send(bytes('please enter the word you would like to guess and wait for your opponent to do the same', 'utf-8'))
                        print(C1)
                        print("*****")
                        C2FinalGuess = cs.recv(1024).decode('utf-8')
                        C2Finished.set()                  
                        C1Finished.wait() 
                        C1Finished.clear()
        
                        if C2FinalGuess == C1:
                            C2Correct = True
                            cs.send(bytes('You guessed the word Correctly', 'utf-8'))
                            determineWinner(cs, C1Correct, C2Correct, CID)
                            break
                        else:
                            cs.send(bytes('Incorrect', 'utf-8'))
                        
                        break  
                    if C1.split()[-1] and guessInput.split()[-1] in C1.split()[-1]:
                        cs.send(bytes(f'Letter "{guessInput}" is in the word', 'utf-8'))
                    else:
                        cs.send(bytes(f'Letter "{guessInput}" IS NOT in the word', 'utf-8')) 
     
    cs.close()
        
def determineWinner(cs, C1Correct, C2Correct, CID):

 if C1Correct == True and C2Correct == True:
     if CID == "Client1":
         determineResult(cs,C1GuessCount, C2GuessCount) 
     elif CID == "Client2":
         determineResult(cs, C2GuessCount, C1GuessCount)
 elif C1Correct == True and C2Correct == False:
     if CID == "Client2":
         cs.send(bytes('You got the word wrong so the game is over, You Lose!', 'utf-8'))
     if CID == "Client1": 
         cs.send(bytes('Your opponent got the word wrong so the game is over, You Win!', 'utf-8'))
 elif C1Correct == False and C2Correct == True:
     if CID == "Client2":
         cs.send(bytes('Your opponent got the word wrong so the game is over, You Win!', 'utf-8'))
     if CID == "Client1": 
         cs.send(bytes('You got the word wrong so the game is over, You Lose!', 'utf-8'))
 else:
     if CID == "Client2":
         cs.send(bytes('You and your opponent got the word wrong', 'utf-8'))
     if CID == "Client1": 
         cs.send(bytes('You and your opponent got the word wrong', 'utf-8'))

# determine who the winner and loser is
def determineResult(cs, playerGuessCount, opponentGuessCount):
    global  RPSC1, RPSC2
    if playerGuessCount < opponentGuessCount:
        cs.send(bytes(f'Great Job, you won in {playerGuessCount} guesses! You had fewer guesses than your opponent so you won!', 'utf-8'))
    elif playerGuessCount > opponentGuessCount:
        cs.send(bytes(f'You lost! Your opponent won in {opponentGuessCount} guesses, which is fewer than your {playerGuessCount} guesses.', 'utf-8'))
    else:
        cs.send(bytes('It is a tie! To determine a Winner you and your opponent will play rock, paper, sissors', 'utf-8'))
        while RPSC1 == RPSC2:
            
            C1Finished.clear() #these reset set() and wait() for each client
            C2Finished.clear()
            
            RPSC1 = ""
            RPSC2 = ""
            RPS = cs.recv(50).decode('utf-8')
            
            print(RPS)
            if "Client1" in RPS:
                RPSC1 = RPS.split()[-1]
                C1Finished.set()
                C2Finished.wait()
                determineRPSWinner(cs, RPSC1, RPSC2)
                
            elif "Client2" in RPS:
                RPSC2 = RPS.split()[-1]
                C2Finished.set()
                C1Finished.wait()
                determineRPSWinner(cs, RPSC2, RPSC1)
        
       
        

def determineRPSWinner(cs, playerChoice, opponentChoice):
    choices = {'r': 'rock', 'p': 'paper', 's': 'scissors'}
    # Determine the winner of rock-paper-scissors
    print("Choices:", choices)
    print("playerChoice:", playerChoice)
    print("opponentChoice:", opponentChoice)
    if (playerChoice == 'r' and opponentChoice == 's') or \
       (playerChoice == 'p' and opponentChoice == 'r') or \
       (playerChoice == 's' and opponentChoice == 'p'):
        cs.send(bytes(f'Congratulations! You won. {choices[playerChoice]} beats {choices[opponentChoice]}', 'utf-8'))
    elif(playerChoice == opponentChoice):
        cs.send(bytes('It was a tie, play again!', 'utf-8'))
    else:
        cs.send(bytes(f'You lost. {choices[opponentChoice]} beats {choices[playerChoice]}', 'utf-8'))

def clearGame():
    global C1finalGuess, C2FinalGuess, C1GuessCount, C2GuessCount, RPSC1, RPSC2
    C1finalGuess = ""
    C2FinalGuess = ""
    C1GuessCount = -1
    C2GuessCount = -1
    RPSC1 = ""
    RPSC2 = ""
    C1Finished.clear()
    C2Finished.clear()

    
Port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', Port))
s.listen(30)

clients = []
while True:
    cs, addr = s.accept()
    print(f"Accepted connection from {addr}") # this is to ensure connection from each client

    CID = "Client1" if not C1 else "Client2" # define who each client is 

    clients.append(cs) # add each client to the Client Socket(for threading)
    if len(clients) == 2:
        break


# opens a thread for each client
for i in range(2):
    clientThread = threading.Thread(target=handleClient, args=(clients[i], "Client1" if i == 0 else "Client2"))
    clientThread.start()
    # chat gpt helped me with threading :)

