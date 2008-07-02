import unittest
import datetime
import struct

import pyreplib

# Need to put in the useless bytes, so we replace 'x' (pad byte) with 'B'.
PLAYER_PACK_FORMAT = pyreplib.PLAYER_STRUCT_FORMAT.replace('x', 'B')
HEADER_PACK_FORMAT = pyreplib.HEADER_STRUCT_FORMAT.replace('x', 'B')

class TestHelperFunctions(unittest.TestCase): # {{{1
    def test_from_nullstr(self):
        self.assertEquals(pyreplib.from_nullstr(''), '')
        self.assertEquals(pyreplib.from_nullstr('\0'), '')
        self.assertEquals(pyreplib.from_nullstr('\0\0\0\0'), '')
        self.assertEquals(pyreplib.from_nullstr('\0a'), '')
        self.assertEquals(pyreplib.from_nullstr('foo\0'), 'foo')
        self.assertEquals(pyreplib.from_nullstr('foo\0a'), 'foo')
        self.assertEquals(pyreplib.from_nullstr('foo'), 'foo')


class TestMockReplay(unittest.TestCase): # {{{1
    def setUp(self):
        self.rep = pyreplib.Replay()
        self.players = ''.join(struct.pack(PLAYER_PACK_FORMAT, *t) for t in (
            # Num   Slot    Type    Race    Byte    Name
            ( 0,    -1,     0,      0,      0,      ""),
            ( 1,    -1,     1,      0,      0,      "Zerg CPU"),
            ( 2,     0,     2,      1,      0,      "Terran Player"),
            ( 3,     1,     2,      2,      0,      "Protoss Player"),
            ( 4,    -1,     0,      0,      0,      ""),
            ( 5,    -1,     0,      0,      0,      ""),
            ( 6,    -1,     0,      0,      0,      ""),
            ( 7,    -1,     0,      0,      0,      ""),
            ( 8,    -1,     0,      0,      0,      ""),
            ( 9,    -1,     0,      0,      0,      ""),
            (10,    -1,     0,      0,      0,      ""),
            (11,    -1,     0,      0,      0,      ""),
        ))

    def test_replay_id(self):
        # Invalid ids
        ids = (None, -1, 0, -1, 3.2)
        for id in ids:
            self.rep.replay_id = id
            self.assert_(not self.rep.is_valid())

        # Valid id
        self.rep.replay_id = 0x53526572
        self.assert_(self.rep.is_valid())

    def test_decode_player(self):
        p1 = struct.pack(PLAYER_PACK_FORMAT, 0, -1, 0, 0, 0, '')
        p2 = struct.pack(PLAYER_PACK_FORMAT, 1, -1, 1, 0, 0, 'Zerg')
        p3 = struct.pack(PLAYER_PACK_FORMAT, 2,  0, 2, 1, 0, 'Terran')
        p4 = struct.pack(PLAYER_PACK_FORMAT, 3,  1, 2, 2, 0, 'Protoss')

        player = self.rep._decode_player(p1)
        self.assertEquals(player.name, '')
        self.assertEquals(player.race, 0)
        self.assertEquals(player.race_name, 'Zerg')
        self.assertEquals(player.type, 0)
        self.assertEquals(player.slot, -1)
        self.assertEquals(player.number, 0)
        self.assertEquals(player.human, False)

        player = self.rep._decode_player(p2)
        self.assertEquals(player.name, 'Zerg')
        self.assertEquals(player.race, 0)
        self.assertEquals(player.race_name, 'Zerg')
        self.assertEquals(player.type, 1)
        self.assertEquals(player.slot, -1)
        self.assertEquals(player.number, 1)
        self.assertEquals(player.human, False)

        player = self.rep._decode_player(p3)
        self.assertEquals(player.name, 'Terran')
        self.assertEquals(player.race, 1)
        self.assertEquals(player.race_name, 'Terran')
        self.assertEquals(player.type, 2)
        self.assertEquals(player.slot, 0)
        self.assertEquals(player.number, 2)
        self.assertEquals(player.human, True)

        player = self.rep._decode_player(p4)
        self.assertEquals(player.name, 'Protoss')
        self.assertEquals(player.race, 2)
        self.assertEquals(player.race_name, 'Protoss')
        self.assertEquals(player.type, 2)
        self.assertEquals(player.slot, 1)
        self.assertEquals(player.number, 3)
        self.assertEquals(player.human, True)

    def test_decode_players(self):
        L = list(self.rep._decode_players(self.players))
        self.assertEquals(len(L), 12)

        player = L[0]
        self.assertEquals(player.name, '')
        self.assertEquals(player.race, 0)
        self.assertEquals(player.race_name, 'Zerg')
        self.assertEquals(player.type, 0)
        self.assertEquals(player.slot, -1)
        self.assertEquals(player.number, 0)
        self.assertEquals(player.human, False)

        player = L[1]
        self.assertEquals(player.name, 'Zerg CPU')
        self.assertEquals(player.race, 0)
        self.assertEquals(player.race_name, 'Zerg')
        self.assertEquals(player.type, 1)
        self.assertEquals(player.slot, -1)
        self.assertEquals(player.number, 1)
        self.assertEquals(player.human, False)

        player = L[2]
        self.assertEquals(player.name, 'Terran Player')
        self.assertEquals(player.race, 1)
        self.assertEquals(player.race_name, 'Terran')
        self.assertEquals(player.type, 2)
        self.assertEquals(player.slot, 0)
        self.assertEquals(player.number, 2)
        self.assertEquals(player.human, True)

        player = L[3]
        self.assertEquals(player.name, 'Protoss Player')
        self.assertEquals(player.race, 2)
        self.assertEquals(player.race_name, 'Protoss')
        self.assertEquals(player.type, 2)
        self.assertEquals(player.slot, 1)
        self.assertEquals(player.number, 3)
        self.assertEquals(player.human, True)

    def test_decode_header(self):
        data = [
            1,
            28000,
            0x00, 0x00, 0x48, # Unknown bytes
            1000000000,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Unknown bytes
            'friendly game',
            128,
            128,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Unknown bytes
            'gnuvince',
            0, # Unknown byte
            'Lost Temple',
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Unknown
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Unknown
            self.players,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Unknown
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # Unknown
        ]

        header = struct.pack(HEADER_PACK_FORMAT, *data)
        self.rep._decode_headers(header)
        self.assertEquals(self.rep.game_engine, 1)
        self.assertEquals(self.rep.engine_name, 'Broodwar')
        self.assertEquals(self.rep.game_frames, 28000),
        self.assertEquals(self.rep.timestamp, 1000000000),
        self.assertEquals(self.rep.date,
                          datetime.datetime(2001, 9, 8, 21, 46, 40))
        self.assertEquals(self.rep.game_name, 'friendly game')
        self.assertEquals(self.rep.map_width, 128)
        self.assertEquals(self.rep.map_height, 128)
        self.assertEquals(self.rep.creator, 'gnuvince')
        self.assertEquals(self.rep.map_name, 'Lost Temple')

        # Starcraft instead of Broodwar
        data[0] = 0
        header = struct.pack(HEADER_PACK_FORMAT, *data)
        self.rep._decode_headers(header)
        self.assertEquals(self.rep.game_engine, 0)
        self.assertEquals(self.rep.engine_name, 'Starcraft')




if __name__ == '__main__':
    unittest.main()
