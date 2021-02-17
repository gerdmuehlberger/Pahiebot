from setup.DiscordBotConnector import DiscordBotConnector
from setup.DatabaseConnector import DatabaseConnector
from setup.ApiConnector import ApiConnector
from setup.Commands import Commands
from setup.CommandProcessor import CommandProcessor
from setup.Errorhandler import Errorhandler
from setup.SSD_Mobilenet_v3 import SSD_Mobilenet_v3
from pathlib import Path
import json
import os


currentWorkingDirectory = Path(__file__).parents[0]
currentWorkingDirectory = str(currentWorkingDirectory)
isProductionEnvironment = os.environ.get('IS_HEROKU', None)

if isProductionEnvironment:
    discordtoken = os.environ.get('token')
    dbuser = os.environ.get('dbuser')
    dbpass = os.environ.get('dbpass')
    dbhost = os.environ.get('dbhost')
    dbname = os.environ.get('db')
    reddit_use_script = os.environ.get('use_script')
    reddit_client_secret = os.environ.get('client_secret')
    reddit_user_agent = os.environ.get('user_agent')
    reddit_username = os.environ.get('username')
    reddit_password = os.environ.get('password')

else:
    developmentConfigFile = json.load(open(currentWorkingDirectory+'/config/secrets.json'))
    discordtoken = developmentConfigFile['devtoken']
    dbuser = developmentConfigFile['dbuser']
    dbpass = developmentConfigFile['dbpass']
    dbhost = developmentConfigFile['dbhost']
    dbname = developmentConfigFile['db']
    reddit_use_script = developmentConfigFile['use_script']
    reddit_client_secret = developmentConfigFile['client_secret']
    reddit_user_agent = developmentConfigFile['user_agent']
    reddit_username = developmentConfigFile['username']
    reddit_password = developmentConfigFile['password']


# Establishing Discord Connection
discordBotConnectionObject = DiscordBotConnector(discordtoken)

# Establishing Database Connection
databaseConnectionObject = DatabaseConnector(dbuser, dbpass, dbhost, dbname)

# Establishing Reddit Connection
redditConnectionObject = ApiConnector.redditConnector(ApiConnector(), reddit_use_script, reddit_client_secret, reddit_user_agent, reddit_username, reddit_password)

# Creating BotObject for handling commands
botObject = DiscordBotConnector.botObject

# Initialise Errorhandler for Unexpected Exceptions
Errorhandler(botObject)

# Initialise all Commands for the Botobject
Commands(botObject, databaseConnectionObject, redditConnectionObject)

#Enable functionality to process Commands
CommandProcessor(botObject)

# Initialise Mobilenet Model Class
#SSD_Mobilenet_v3()

# Running the Bot
discordBotConnectionObject.runBot()