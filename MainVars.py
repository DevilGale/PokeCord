import os
import sys
import asyncio
import discord
import datetime

# api #
import requests
from imgurpython import ImgurClient

from var_secrets.py import *

# DISCORD  VARS #
client = discord.Client()

BOT_PREFIX = "$"
CHANNEL_IDs  = ("449281327988998156")

# PYTHON VALS #
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Globals #

imgr_client = ImgurClient(imgr_client_id, imgr_client_secret)

# Image Vars #
white = (255,255,255,255)
black = (0, 0, 0, 255)