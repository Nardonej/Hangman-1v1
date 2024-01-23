# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 07:56:31 2023

@authors: Josh Nardone, Giang Do
"""

import socket

Host = socket.gethostname()
Port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((Host, Port))
playAgain = input("Do you want to play? (y/n): ")
encodedPlay = playAgain.encode('utf-8')
s.sendall(b'Client1: ' + encodedPlay)

if playAgain.lower() == 'n':
    print("You didn't want to play. Exiting...")
    s.close()
    
    

if playAgain.lower() == 'y':
    opponentPlay = (s.recv(50).decode('utf-8'))
    print(opponentPlay)
    if opponentPlay == "your opponent did not want to play":
        print("Closing...")
        s.close()
    else:    
        while True:
            a = input("Enter a 5 letter word (or type 'end' to exit): ")
        
            if a == 'end':
                s.sendall(b'Client has ended the chat')
                s.close()
                break
        
            if len(a) != 5:
                print("Word is not 5 letters long. Please try again.")
            else:
                encodedInput = a.encode('utf-8')
                print("please wait for your opponent to submit a word")
                s.sendall(b'Client1: ' + encodedInput)
                print(s.recv(500).decode('utf-8'))
        
                for i in range(10):
                    while True:
                        b = input("Enter any letter or 'guess' to guess your opponent's word:")
                        if b == "guess":
                            break
                        elif len(b) == 1:
                            print(9 - i, " guesses left")
                            break
                        else:
                            print("Please enter a single letter.")
                                    
                    guessInput = b.encode('utf-8')
                    s.sendall(b'Client1: ' + guessInput)
                    print(s.recv(500).decode('utf-8'))
                    if b == "guess":
                        break
                 
                c = input("Please enter your guess: ")
                finalGuessInput = c.encode('utf-8')
                s.sendall(b'Client2: ' + finalGuessInput)
                result = s.recv(1024).decode('utf-8')
                print(result)
                finalResult = (s.recv(1024).decode('utf-8'))
                print(finalResult)
                while "rock" in finalResult or "paper" in finalResult or "scissors" in finalResult:
                    while True:
                        RPS = input("Please enter either 'r', 'p', or 's': ")
                        if (RPS == 'r') or (RPS == 's') or (RPS == 'p'):
                            break
                        else:
                            print("please enter a valid guess")
                    encodedRPS = RPS.encode('utf-8')
                    s.sendall(b'Client1: ' + encodedRPS)
                    RPSresult = (s.recv(1024).decode('utf-8'))
                    print(RPSresult)
                    if "Congratulations!" in RPSresult or "You lost." in RPSresult:
                        break
                break
            s.close

