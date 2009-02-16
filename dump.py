from pyreplib import replay
import sys

for arg in sys.argv[1:]:
    try:
        replay.Replay(arg)
    except:
        print arg, ": bad replay"
