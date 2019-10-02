![github banner](https://repository-images.githubusercontent.com/212122491/8d69d600-e49e-11e9-95e2-dd25d0ad9eff)

## About
This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message.

## Usage

#### How to copy your stats from Ingress Prime
Open your Agent Profile in Ingress Prime. Now press the copy button that is in the top right. 
It should be under your current Level.

#### Private chat
Open [@primestatsbot](t.me/primestatsbot) and start the bot. If you paste and send the stats you just copied it will
send back a nicely formatted message with your stats.

#### Group chat
Add  [@primestatsbot](t.me/primestatsbot) to group you want to use it in. Give the bot administrative rights so it can 
at least read messages. Whenever it detects messages that are stats copied from Ingress Prime it will back a message 
with the stats nicely formatted.

## Build your own bot
You might not trust me with hosting this bot. You might think I will save your stats or save messages send in groups 
I've been added to. In that case you can read through and check the sourcecode here and set up the bot yourself!

### Requirements
You will need Python 3.6 or higher and setup tools. That's it!

### Setup
First set up a bot using [@botfather](t.me/botfather). Here you can also get the bot token you're gonna need.

Fill in the variables in 'example.env' and save the file as '.env'.

## Installation
Open a terminal in the root of the project directory. 
Install the required Python Packages listed in 'requirements.txt' using the following command:

```
pip install -r requirements.txt
```

## Running
Now all you need to do is start the bot by typing the following command:

```
python primestatsbot.py
```

That's it! You can now use this bot as described in the section 'Usage'.