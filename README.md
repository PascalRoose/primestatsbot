![github banner](https://repository-images.githubusercontent.com/212122491/8d69d600-e49e-11e9-95e2-dd25d0ad9eff)

## About
This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message.

## Usage

#### How to copy your stats from Ingress Prime
Open your Agent Profile in Ingress Prime. Now press the copy button that is in the top right. 
It should be under your current Level.

#### Private chat
Open [@primestatsbot](http://t.me/primestatsbot) and start the bot. If you paste and send the stats you just copied it will
send back a nicely formatted message with your stats.

You can change the output format by typing ___/settings___

#### Group chat
Add  [@primestatsbot](http://t.me/primestatsbot) to group you want to use it in. Give the bot administrative rights so it can 
at least read messages. Whenever it detects messages that are stats copied from Ingress Prime it will back a message 
with the stats nicely formatted.

You can change the output format by typing ___/settings___. The command and settings menu will only work for chat admins.

#### Bot admin
The admin of the bot (in this case [@PascalRoose](https://t.me/PascalRoose)) has access to the following tools.

Broadcast a message using ___/broadcast___. This will attempt to send a message to every user that ever started the bot.

Get usage statistics using ___/stats___. This will show the uses and unique users of the last week and total.

When an exception occurs you will receive a crash report.

## Build your own bot
You might not trust me with hosting this bot. You might think I will save your stats or save messages send in groups 
I've been added to. In that case you can read through and check the sourcecode here and set up the bot yourself!

### Requirements
You will need Python 3.7 or higher and pipenv. That's it!

### Setup
First set up a bot using [@botfather](http://t.me/botfather). Here you can also get the bot token you're gonna need.

Next you're gonna want to fill in the variables in configurations/setup.py. Fill in your token, botname and telegram id. 
You can also setup webhooks in here if you want to. 

## Installation
Open a terminal in the root of the project directory. 
Setup the environment with pipenv using the following command:

```
pipenv install
```

Next you're gonna install the package by typing:
```
pipenv run python setup.py install
```

## Running
Now all you need to do is start the bot by typing the following command:

```
pipenv run python -m primestatsbot
```

That's it! You can now use this bot as described in the section 'Usage'.
