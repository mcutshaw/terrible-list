from db import db
from configparser import ConfigParser
config = ConfigParser()
config.read('list.conf')
d = db(config)