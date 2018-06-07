# TwitchPlays
This script grabs input from your twitch chat. It can also grab votes for words and use the majority vote for something (I don't know what yet). Remember TwitchPlaysPokemon? This is basically the democracy mode done for you.

Only dropping this on github so I can motivate myself to add to it

# twitch_input.py setup
NICK is the channel name. In this case, it is https://www.twitch.tv/pattycakelol/



PASS is the Twitch IRC OAuth Token that you can get from https://twitchapps.com/tmi/

example: oauth:g0swlyxirxij68svtxu16fcpjit6os (has already been trashed btw)

# Usage
>python twitch_input.py

Go to your channel, type stuff, and see it show up in console

If you vote (send single word messages starting with '!'), they will also show up in console along with all previous votes & the current vote majority

# Future
- [ ] Add timer for democracy mode
- [ ] Add anarchy mode
- [ ] Make something cool using this????
