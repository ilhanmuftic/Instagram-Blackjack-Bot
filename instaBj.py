from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from time import sleep
from datetime import datetime
import random
import requests

# Initialize webdriver for Chrome using ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Initialize global variables
PLAYERS = []
CARDS = [2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10]
DEALER = 0
TURN = 0
STATUS = True

# Function to send a message in the Instagram chat
def sendMsg(msg):
    driver.find_elements(By.TAG_NAME, "textarea")[0].send_keys("!! "+ msg, Keys.ENTER)

# Function to get the most recent command in the Instagram chat
def getMsg():
    return driver.find_elements(By.XPATH, "//*[starts-with(text(), '!')]")[-1] 

# Function to get the command from the most recent message in the Instagram chat
def getCmd():

    txto = getMsg()
    txt = txto.text + ' '
    if(txt[0] == "!"):
        cmd = {"command": txt.split(' ')[0], "params": txt.split(' ')[1].replace('*', ' '), "true": True}
        return cmd
    else:
        return {"command": '', "params": '', "true": False}

def addPlayer(player):
    global PLAYERS
    PLAYERS.append({"name": player, "cards": 0, "wins": 0, "pcards": []})
    msg = "Added player " + player + " All players -"
    for i in PLAYERS:
        msg += " "
        msg += i["name"]

    sendMsg(msg)

def getCard():
    global CARDS
    cardi = random.randint(0, len(CARDS)-1)
    card = CARDS[cardi]
    del CARDS[cardi]
    return card



def reset():
    global CARDS
    global PLAYERS
    global DEALER
    global TURN

    CARDS = [2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 10, 10]
    for i in PLAYERS:
        i["cards"] = 0

    DEALER = 0
    TURN = 0

def start():
    reset()
    global PLAYERS
    global DEALER
    global TURN

    for i in PLAYERS:
        i["pcards"] = []

    # Deal each player 2 cards
    for _ in range(2):
        for i in PLAYERS:
            card = getCard()
            i["cards"] += card
            i["pcards"].append(card)
            if(i["cards"] == 22):
                i["cards"] = 12

    DEALER += getCard()

    msg = ""

    for i in PLAYERS:
       msg += i["name"] + ' - ' + str(i["cards"]) + ' ( ' + ' '.join(map(str, i["pcards"])) + ' )' + '\t'

    msg += "\nDealer: " + str(DEALER)

    sendMsg(msg)

    for i in PLAYERS:
        if(i["cards"]==21):
            TURN += 1
        else:
            break

def finish():
    global PLAYERS
    global DEALER

    while( DEALER < 17):
        DEALER += getCard()

    msg = ""

    for i in PLAYERS:
        msg += i["name"] + ' - ' + str(i["cards"]) + '\t'

    msg += "\nDealer: " + str(DEALER)

    sendMsg(msg)

    sleep(1)

    for i in PLAYERS:
        if(i["cards"]>21):
            sendMsg(i["name"] + " lost!")
        elif(DEALER > 21):
            i["wins"] += 1
            sendMsg(i["name"] + " won!\t\t\t(wins-" + str(i["wins"])+")")

        elif(i["cards"]<DEALER):
            sendMsg(i["name"] + " lost!")
        elif(i["cards"]>DEALER):
            i["wins"] += 1
            sendMsg(i["name"] + " won!\t\t\t(wins-" + str(i["wins"])+")")

        else:
            sendMsg(i["name"] + " tied!")


def play(hs):
    global PLAYERS
    global TURN

    if(hs=="hit"):
        card = getCard()
        if(card == 11 and PLAYERS[TURN]["cards"]+card > 21):
            card=1

        PLAYERS[TURN]["cards"] += card
        PLAYERS[TURN]["pcards"].append(card)

        if(PLAYERS[TURN]["cards"] >= 21):
            if PLAYERS[TURN]["cards"] > 21:
                for i in range(0, len(PLAYERS[TURN]["pcards"])-1):
                    if PLAYERS[TURN]["pcards"][i] == 11:
                        PLAYERS[TURN]["cards"] -= 10
                        PLAYERS[TURN]["pcards"][i] = 1
                        break

        if PLAYERS[TURN]["cards"] >= 21:
            sendMsg(PLAYERS[TURN]["name"] + " - " + str(PLAYERS[TURN]["cards"]) + " (" + ' '.join(map(str, PLAYERS[TURN]["pcards"])) + ')')
            stand()
        else:
            sendMsg(PLAYERS[TURN]["name"] + " - " + str(PLAYERS[TURN]["cards"]) + " (" + ' '.join(map(str, PLAYERS[TURN]["pcards"]))  + ")" + " \t hit/stand")

    elif(hs=="stand"):
        stand()

def stand():
    global TURN
    global PLAYERS
    TURN += 1

    if (TURN == len(PLAYERS)):
        finish()
    else:
        while (PLAYERS[TURN]["cards"] == 21):
            TURN += 1
            if (TURN == len(PLAYERS)):
                finish()
                return


        sendMsg(PLAYERS[TURN]["name"] + " - " + str(PLAYERS[TURN]["cards"]) + " (" + ' '.join(map(str, PLAYERS[TURN]["pcards"]))  + ")" + " \t hit/stand")

def rrplay():
    global PLAYERS

    msg = ""

    for i in PLAYERS:
        msg += i["name"] + "\t"

    sendMsg("Russian Roulette:\t" + msg)

    rrp = PLAYERS

    for i in range(0, len(rrp)-1):
        sleep(3)
        x = random.randint(0, len(rrp) - 1)
        sendMsg(rrp[x]["name"])
        del rrp[x]


    sendMsg(rrp[0]["name"] + " won!")




if __name__ == "__main__":
    driver.get('https://instagram.com')
    input("Log into your instagram account, enter the chat you want the bot to be activated in and press enter!")
    sendMsg("hello")

    while True:
        sleep(1)
        try:
            cmd = getCmd()
            if(cmd["true"] and cmd["command"]!="!!"):
                if(cmd["command"]=="!addp"):
                    addPlayer(cmd["params"])
                elif(cmd["command"]=="!hit"):
                    play("hit")
                elif (cmd["command"] == "!stand"):
                    play("stand")
                elif (cmd["command"] == "!start"):
                    start()
                elif (cmd["command"] == "!reset"):
                    PLAYERS = []
                elif (cmd["command"] == "!remove"):

                    name = PLAYERS[int(cmd["params"])]["name"]

                    del PLAYERS[int(cmd["params"])]
                    sendMsg("Removed " + name)

                elif (cmd["command"] == "!pause"):
                    sleep(int(cmd["params"]))
                elif (cmd["command"] == "!players"):
                    msg = ""
                    for i in PLAYERS:
                        msg += i["name"] + " - " + str(i["wins"]) + " "

                    sendMsg(msg)
                elif cmd["command"] == "!help":
                    sendMsg("Svakom igracu kao i dealeru se dijele po dvije karte na pocetku, (dealeru je otkrivena samo jedna do kraja igre).\
                                     Cilj igre je imati vecu vrijednost karata od dealera, bez da taj broj prelazi 21.\
                                     Ukoliko igrac ima vise od 21 kartu, automatski gubi.\
                                     Nakon podjele karti, igrac (koji je na redu) ima opciju \"Hit\" - igrac dobija kartu iz spila\
                                     i \"Stand\" igrac zavrsava svoj potez i na red dolazi onaj poslije njega.\
                                     Igrac moze 'hitati' koliko god zeli dok je njegov potez, sve dok njegove karte ne prelaze 21.\
                                     Na kraju, kada svi igraci zavrse potez, dealeru se dijele karte sve dok ne bude imao vrijednost 17 ili vise\n \
                                     Komande: !addp <ime> dodaje igraca, !start pocinje igru, !reset brise sve igrace i resetuje igru, a za igru komande !hit i !stand\
                                     !russian ruski rulet, bot ispisuje ispale na kraju ostaje samo jedan pobjednik\
                                     !flip glava-pismo, !players ispisuje sve igrace i njihove pobjede, !rename <id>,<name> \
                                     !remove <id> brise igraca \
                                     !ask <pitanje da/ne> daje odgovor da ili ne,  !joke, !idegas gasi gasera\
                                     id se gleda po redu pocevsi od 0 (komanda !players)\
                                     u porukama razmak je zamijenjen sa *\
                                     Bot ignorise sve poruke koje ne pocinju sa '!'")
                elif (cmd["command"] == "!shutdown"):
                    sendMsg("baj")
                    break
                elif (cmd["command"] == "!idegas"):
                    now = datetime.now()

                    current_time = now.strftime("%H:%M:%S")
                    sendMsg("Shutting Down " + current_time)
                    os.system("shutdown /p")
                elif (cmd["command"] == "!russian"):
                    rrplay()
                elif (cmd["command"] == "!status"):
                    sendMsg(STATUS)
                elif (cmd["command"] == "!flip"):
                    sendMsg(random.choice(["Glava", "Pismo"]))
                elif cmd["command"] == "!rename":
                    PLAYERS[int(cmd["params"].split(',')[0])]["name"] = cmd["params"].split(',')[1]
                elif cmd["command"] == "!spam":
                    if int(cmd["params"].split(',')[0]) > 20:
                        sendMsg("Odbij sotono odbij!")
                    else:
                        for _ in range(0, int(cmd["params"].split(',')[0])):
                            sendMsg(cmd["params"].split(',')[1])
                elif cmd["command"] == "!ask":
                    sendMsg(random.choice(["Da", "Ne"]))
                elif cmd["command"] == "!joke":
                    joke = requests.get('https://v2.jokeapi.dev/joke/Dark?format=txt')
                    sendMsg(joke.text)

        except:
            print("Error")
            raise
            
    driver.close()        
   
