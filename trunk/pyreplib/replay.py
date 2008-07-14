import datetime
import struct
from cStringIO import StringIO

from pyreplib import _unpack
from pyreplib.actions import action_classes

TICKS_PER_SECOND = 24
REPLAY_ID = 0x53526572
PLAYER_NUMBER = 12
HEADER_STRUCT_FORMAT = (
    '<'    # Little-endian
    'B'    # Game engine, 0 = Vanilla, 1 = Broodwar
    'L'    # Game frames (each frame == 42ms)
    '3x'   # Unknown, always 0x00, 0x00, 0x48
    'L'    # Save time, UNIX timestamp
    '12x'  # Unknown
    '28s'  # Game name (padded with 0x00)
    'H'    # Map width
    'H'    # Map height
    '16x'  # Unknown
    '24s'  # Creator name (padded with 0x00)
    '1x'   # Unknown
    '26s'  # Map name (padded with 0x00)
    '38x'  # Unknown
    '432s' # Players data
    '40x'  # Unknown
) # Parens are there to prevent an indentation error.
PLAYER_STRUCT_FORMAT = (
    '<'   # Little endian
    'I'   # Player number (0-11)
    'i'   # Slot number (-1 if CPU or None, 0-7 otherwise)
    'B'   # Player type (0: None, 1: CPU, 2: Player)
    'B'   # Race (0: Zerg, 1: Terran, 2: Protoss)
    'x'   # Unknown byte
    '25s' # Player name
) # Parens are there to prevent an indentation error.


def from_nullstr(s):
    i = s.find('\0')
    if i == -1:
        return s
    else:
        return s[:i]


def avg(L):
    return sum(L) / len(L)

class InvalidReplayException(Exception): pass


class Replay(object):
    def __init__(self, filename):
        self.data = _unpack.unpack(filename)
        self.replay_id = self.data[0]
        self._decode_headers(self.data[1])
        self._decode_actions(self.data[2])

    def __str__(self):
        return '<Replay: %s>' % self.game_name

    def __repr__(self):
        return str(self)

    def _get_replay_id(self):
        return self._replay_id

    def _set_replay_id(self, value):
        if value != 0x53526572:
            raise InvalidReplayException('Replay id is not 0x53526572')
        else:
            self._replay_id = value
    replay_id = property(_get_replay_id, _set_replay_id)

    def get_engine_name(self):
        '''English name of the replay's Starcraft engine'''
        if self.game_engine == 0:
            return 'Starcraft'
        else:
            return 'Broodwar'
    engine_name = property(get_engine_name)

    def get_date(self):
        '''Take the timestamp and return a datetime.'''
        return datetime.datetime.fromtimestamp(self.timestamp)
    date = property(get_date)

    def is_valid(self):
        '''A replay is considered valid when its id is 0x53526572.'''
        return self.replay_id == REPLAY_ID

    def _decode_headers(self, data):
        '''Takes a header binary string and assigns the different
        attributes.  No return value.'''
        t = struct.unpack(HEADER_STRUCT_FORMAT, data)
        self.game_engine = t[0]
        self.game_frames = t[1]
        self.timestamp   = t[2]
        self.game_name   = from_nullstr(t[3])
        self.map_width   = t[4]
        self.map_height  = t[5]
        self.creator     = from_nullstr(t[6])
        self.map_name    = from_nullstr(t[7])
        self.player_slots = list(self._decode_players(t[8]))
        self.players     = [p for p in self.player_slots if p.human]

    def _decode_player(self, player_data):
        '''Takes a 36 byte string and returns a Player object.'''
        t = struct.unpack(PLAYER_STRUCT_FORMAT, player_data)
        return Player(name=t[4],
                      race=t[3],
                      type=t[2],
                      slot=t[1],
                      number=t[0])

    def _decode_players(self, players_data):
        '''Takes a 432 byte string and yields 12 Player objects.'''
        for i in xrange(PLAYER_NUMBER):
            player = self._decode_player(players_data[i*36 : (i+1)*36])
            yield player


    def _decode_actions(self, action_data):
        # Cache players and they slot number to improve performance
        players = dict((p.slot, p) for p in self.players)
        data_length = len(action_data)
        buf = StringIO(action_data)
        while buf.tell() != data_length:
            tick, block_length = struct.unpack('< I B', buf.read(5))
            while block_length:
                player_id, action_id = struct.unpack('< B B', buf.read(2))
                block_length -= 2
                action_cls = action_classes.get(action_id)
                # Skip over unknown actions
                if action_cls is None:
                    continue
                action = action_cls(tick)
                player = players[player_id]
                player.actions.append(action)
                n = action.read(buf)
                block_length -= n


class Player(object):
    def __init__(self, name, race, type, slot, number):
        self.name = from_nullstr(name)
        self.race = race
        self.type = type
        self.slot = slot
        self.number = number
        self.human = self.slot != -1 and self.type != 0
        self.actions = []
        self.__actions_per_minute = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Player: %s (%s)>' % (self.name, self.race_name)

    def get_race_name(self):
        '''Return english description of player's race.  jca's lib indicates
        that there's a race 6, but I (nor he) have any idea what it does.'''
        if self.race == 0:
            return 'Zerg'
        elif self.race == 1:
            return 'Terran'
        elif self.race == 2:
            return 'Protoss'
        elif self.race == 6:
            return 'Race 6'
        else:
            return ''
    race_name = property(get_race_name)
