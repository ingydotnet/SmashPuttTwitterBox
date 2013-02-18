# Twitter settings
consumer_key="your consumer key"
consumer_secret="your consumer secret"
access_key = "your acces key"
access_secret = "your access secret"
track=["what", "you want", "to", "track"]
screen_name="yourtwitterid"

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
