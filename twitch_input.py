import socket
import threading
import time
from random import randint # for the really lame math game
import os

os.system('cls')

HOST = "irc.twitch.tv"
PORT = 6667
NICK = 'pattycakelol' # twitch channel name
PASS = 'oauth:54rur4edeumk81rcu409geo8ukqgbe' # Twitch Chat OAuth Password

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))

voting = True
democracy = True
votes = {}                              # dictionary -> key = string(voted word) : value = tuple(int(frequency), list(usernames))

# lame game variables
players = {}                            # dictionary -> key = string(username) : value = int(points)
num1 = 999
num2 = 999
operator = 999
answer = 999

def add_vote(vote, username):           # add user's vote to dictionary

    if not voting: # voting has been stopped
        return

    vote_exists = votes.get(vote, ())

    if not vote_exists:                 # if nobody has previously voted for the word
        votes[vote] = (1, [username])   # add to vote dictionary with frequency=1 and start the list of users with this user
        num_votes = votes[vote][0]
        users = votes[vote][1]
    else:                               # vote exists in dictionary
        num_votes = vote_exists[0]
        users = vote_exists[1]
        if username in users:           # current user has already voted for this, do nothing
            return

        # adding current user's vote
        users.append(username)
        votes[vote] = (num_votes + 1, users)

    # remove current user's votes from other votes (if any)
    for key in votes:
        if key == vote:                 # pass over newly inserted vote
            continue
        if username in votes[key][1]:   # user's previous vote exists, remove it
            if votes[key][0] == 1:      # current user was the only one to vote for this, remove key from votes
                votes.pop(key, None)
                return
            temp = votes[key][1]
            temp.remove(username)
            votes[key] = (votes[key][0] - 1, temp)
            return

def get_majorty():                      # returns word from dictionary of votes with highest # of votes
    return max(votes.keys(), key=lambda k: votes[k][0])

def read_chat():

    while True:
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True:
        for line in str(s.recv(1024)).split('\\r\\n'):
            parts = line.split(':')
            if len(parts) < 3:
                continue

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                message = parts[2][:len(parts[2])]

            username = parts[1].split("!")[0]

            # print all messages in chat
            # print(username + ": " + message)

            if message[0] == "!":           # command recognized
                if ' ' in message:          # no arguments allowed in commands
                    continue

                message = message[1:]

                if username == NICK:        # channel owner exclusive commands
                    if message == 'QUIT':
                        quit()
                    if message == 'CLEARVOTES':
                        votes = {}
                        continue
                    if message == 'STOPVOTING':
                        voting = False
                        print('Voting has been stopped')
                        continue
                    if message == 'STARTVOTING':
                        voting = True
                        print('Voting has been started')
                        continue

            # do something to check if command is valid
            if check_answer(message):
                players[username] = players.get(username, 0) + 1
                print('{} got the question right with their answer: {}'.format(username, message))
                print('{} now has {} point(s)\n'.format(username, players[username]))
                print_question()

                # # game logic using majority vote
                # if democracy:
                #     add_vote(message, username)
                # else:
                #     # something
                # print("current votes: " + str(votes))
                # print("vote majority: " + get_majorty())

# thread used for receiving input from twitch chat
chat_reader = threading.Thread(target=read_chat)
chat_reader.start()

# main thread will run the game

# this first iteration will be a really lame math game
# viewers will have points assigned to them for each right question

def print_question():
    global num1
    global num2
    global operator
    num1 = randint(-9, 9)
    num1f = num1
    num2 = randint(-9, 9)
    num2f = num2
    operator = randint(0, 2)
    if num1 < 0:
        num1f = '(' + str(num1) + ')'
    if num2 < 0:
        num2f = '(' + str(num2) + ')'
    if operator == 0:
        print('{} + {} = ?'.format(num1f, num2f))
    if operator == 1:
        print('{} - {} = ?'.format(num1f, num2f))
    if operator == 2:
        print('{} * {} = ?'.format(num1f, num2f))

def check_answer(answer):
    if not is_number(answer):
        return False
    if operator == 0:
        if num1 + num2 == float(answer):
            return True
    if operator == 1:
        if num1 - num2 == float(answer):
            return True
    if operator == 2:
        if num1 * num2 == float(answer):
            return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

print_question()