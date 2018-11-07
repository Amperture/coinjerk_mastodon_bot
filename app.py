import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mastodon_interface import send_toot, send_reply, check_notifications, \
        get_qr_link, process_commands
from commands_parser import sort_mentions
from config_handler import config

db = create_engine(config['db']['uri'])
Session = sessionmaker(bind = db)
session = Session()

while True:
    time.sleep(config['mastodon']['rate_limit']) 
    notes = check_notifications()

    commands = []
    if notes:
        commands = sort_mentions(notes)
        process_commands(commands)
