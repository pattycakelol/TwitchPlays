import socket

HOST = "irc.twitch.tv"
PORT = 6667
NICK = 'pattycakelol' # twitch channel name
PASS = '' # Twitch Chat OAuth Password

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))

voting = True
votes = {}                              # dictionary -> key = string(voted word) : value = tuple(int(frequency), list(usernames))

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
        print(username + ": " + message)

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

            # game logic using majority vote

            add_vote(message, username)
            print("current votes: " + str(votes))
            print("vote majority: " + get_majorty())