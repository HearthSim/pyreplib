import datetime
import struct

import _unpack

REPLAY_ID     = 0x53526572
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


class InvalidReplayException(Exception): pass


class Replay(object):
    def __init__(self, filename):
        data = _unpack.unpack(filename)
        self.replay_id = data[0]
        if not self.is_valid():
            raise InvalidReplayException
        self._decode_headers(data[1])

    def __str__(self):
        return '<Replay: %s>' % self.game_name

    def __repr__(self):
        return str(self)

    def _decode_headers(self, data):
        t = struct.unpack(HEADER_STRUCT_FORMAT, data)
        self.game_engine = t[0]
        self.game_frames = t[1]
        self.timestamp   = t[2]
        self.game_name   = from_nullstr(t[3])
        self.map_width   = t[4]
        self.map_height  = t[5]
        self.creator     = from_nullstr(t[6])
        self.map_name    = from_nullstr(t[7])
        self.players     = list(self._decode_players(t[8]))

    def get_engine_name(self):
        if self.game_engine == 0:
            return 'Starcraft'
        else:
            return 'Broodwar'
    engine_name = property(get_engine_name)

    def get_date(self):
        return datetime.datetime.fromtimestamp(self.timestamp)
    date = property(get_date)

    def _decode_player(self, player_data):
        t = struct.unpack(PLAYER_STRUCT_FORMAT, player_data)
        return Player(name=t[4],
                      race=t[3],
                      type=t[2],
                      slot=t[1],
                      number=t[0])

    def _decode_players(self, players_data):
        for i in xrange(PLAYER_NUMBER):
            yield self._decode_player(players_data[i*36 : (i+1)*36])

    def is_valid(self):
        return self.replay_id == REPLAY_ID


class Player(object):
    def __init__(self, name, race, type, slot, number):
        self.name = from_nullstr(name)
        self.race = race
        self.type = type
        self.slot = slot
        self.number = number
        self.human = self.slot != -1

    def __str__(self):
        return '<Player: %s (%s)>' % (self.name, self.race_name())

    def __repr__(self):
        return str(self)

    def get_race_name(self):
        d = {
            0: 'Zerg',
            1: 'Terran',
            2: 'Protoss',
            6: 'Race 6',
        }
        return d[self.race]
    race_name = property(get_race_name)
