# Twitter settings
CONSUMER_KEY="your consumer key"
CONSUMER_SECRET="your consumer secret"
ACCESS_KEY = "your acces key"
ACCESS_SECRET = "your access secret"
TRACK=["what", "you want", "to", "track"]
SCREEN_NAME="yourtwitterid"

# Log file
LOG="twitterbox.log"
DEBUG=False

# Where did you plug in the light?
LIGHT_PIN = 4
LIGHT_DELAY = 10

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

# Priority queue priorities
PRIORITY_LOW = 10
PRIORITY_HIGH = 1

# Now get the local settings
from local_settings import *
