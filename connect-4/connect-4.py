#Importerer colored funksjonene fra termcolor
#Dette gir meg tilgan til farget tekst
from termcolor import colored
#Jeg importerer hele librariet fordi jeg bruker os.exit(), og exit er et keyword
import os

#Definerer hvordan forskjellige kvadrater skal se ut
#Jeg bestemte meg for å bruke så rare ascii characters for
#å gjøre spillet mer oversiktlig
label = {
        "empty": colored("▒▒", "white"),
        "red": colored("▒▒", "red"),
        "blue": colored("▒▒", "blue"),
        }

#Lager brettet som en 2 dimensjonell liste
def make_board():
    board = []
    for i in range(board_size):
        #.append() legger inputet til listen
        board.append([])
        for j in range(board_size):
            #Alt er tomt når det begynner
            board[i].append("empty")
    #Returnerer brettet funksjonen har lagd
    return board

def print_board():
    #Jeg tror at du må endre clear til cls i windows
    #Tømmer terminalen
    os.system('clear')
    #Det samme som make_board(), men printer ut hver item
    for i in range(board_size):
        for j in range(board_size):
            #end="", brukes for å bli kvitt newline
            print(label[board[i][j]], end=" ")
        #Lager 2 newlines
        print("\n")
    #Printer tallene
    for i in range(board_size):
        print(i+1, end="  ")
    print()

def drop():
    #Dette er for å forsikre seg at du skriver inn et gyldig felt
    while True:
        try:
            index = int(input(f"{player} drop: ")) - 1
            #Skjekker om det er en valid input
            if index >= 0 and index < board_size and board[0][index] == "empty":
                #Fortsetter programmet om det er sant
                break
            else:
                #for en eller annen grunn kan jeg ikke bruke quit()
                #jeg tror at det har noe med at quit() endrer "staten" til programmet,
                #mens os.exit() ikke har noen "side effects", og blir derfor treatert
                #som en vanlig error
                os.exit()
        except:
            print("Input error, make sure you input a valid number") 
    
    #Går ned helt til den finner et okkupert felt og putter det du dropper over den
    for i in range(board_size):
        if board[i][index] != "empty":
            board[i-1][index] = player
            break
        #Hvis du er på bunnen skal du droppe den hvor du er, og ikke over
        elif i + 1 == board_size:
            board[i][index] = player
            break
    
def straight_check():
    #Øker sum helt til den finner feil type felt, hvor den resetter seg
    #Originalt var h_sum og v_sum i sine egne funksjoner,
    #men jeg kom opp med at jeg kan bare invertere i og j
    #så jeg kunne bare bruke samme loop
    #hvis den finner 4 på rad returnerer den tidlig med True
    for i in range(board_size):
        h_sum = 0
        v_sum = 0
        for j in range(board_size):
            if board[i][j] == player:
                h_sum += 1
            else:
                h_sum = 0
            if h_sum == 4:
                return True

            if board[j][i] == player:
                v_sum += 1
            else:
                v_sum = 0
            if v_sum == 4:
                return True
    return False

#Denne funksjonen var litt vanskelig å komme opp med, den beste måten
#å beskrive den på er måten jeg løste problemet på, med å tegne problemet
#Tenk for deg et brett med størrelse 5:
#
#i=0|0,1,2,3,4
#i=1|1,2,3,4,5
#i=2|2,3,4,5,6
#i=3|3,4,5,6,7
#i=4|4,5,6,7,8
#    ---------
#j=  0,1,2,3,4

#Hvis hvert tall er sin egen liste index, kan vi finne ut hvilken index en rute
#hører til basert på summen av i og j, ellers er programmet det samme som straight_check()
#På den andre diagonalen vil du finne at jeg må bare gå baklengs på en av aksene, så jeg inverterte loopen
def diagonal_check():
    sum1 = []
    sum2 = []
    for i in range(2 * board_size - 1):
        sum1.append(0)
        sum2.append(0)
    
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == player:
                sum1[i + j] += 1
            else:
                sum1[i + j] = 0
            if sum1[i + j] == 4:
                   return True

            if board[board_size - (i + 1)][j] == player:
                sum2[i + j] += 1
            else:
                sum2[i + j] = 0
            if sum2[i + j] == 4:
                   return True
    return False
    
#Main program
board_size = int(input("Board size: "))
if board_size < 4:
        print("Board too small!")
        quit(1)
#Brettet blir hva funksjonen returnerer
board = make_board()
player = "red"
#Går for evig, hver tur er en loop
while True:
    print_board()
    #Skjekker om check funksjonene returnerer True
    if straight_check() or diagonal_check():
        print(f"The winner is {player}!!!")
        #Error code 0 betyr at alt gikk bra (tror jeg, det er sånn i c)
        quit(0)
    #Alternerer player
    if player == "red":
        player = "blue"
    else:
        player = "red"
    drop()
