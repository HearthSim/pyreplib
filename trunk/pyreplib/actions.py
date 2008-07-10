import struct
import operator

__all__ = ['ActionBase', 'Action', 'action_classes', 'Select',
           'ShiftSelect', 'ShiftDeselect', 'Build', 'Vision', 'Ally',
           'Hotkey', 'Move', 'Attack', 'Cancel', 'CancelHatch', 'Stop',
           'ReturnCargo', 'Train', 'CancelTrain', 'Cloak', 'Decloak',
           'Hatch', 'Unsiege', 'Siege', 'BuildInterceptor', 'UnloadAll',
           'Unload', 'MergeArchon', 'HoldPosition', 'Burrow', 'Unburrow',
           'CancelNuke', 'Lift', 'Research', 'CancelResearch', 'Upgrade',
           'Morph', 'Stim', 'LeaveGame', 'MergeDarkArchon', 'Byte', 'Word',
           'DWord', 'Field']

Byte = 'B'
Word = 'H'
DWord = 'I'

# Hex to string mappings {{{
attacks = {
    0x00: 'Move with right click',
    0x06: 'Move by click move icon',
    0x08: 'Attack',
    0x09: 'Gather',
    0x0E: 'Attack Move',
    0x13: 'Failed Casting (?)',
    0x1B: 'Infest CC',
    0x22: 'Repair',
    0x27: 'Clear Rally',
    0x28: 'Set Rally',
    0x4F: 'Gather',
    0x50: 'Gather',
    0x70: 'Unload',
    0x71: 'Yamato',
    0x73: 'Lockdown',
    0x77: 'Dark Swarm',
    0x78: 'Parasite',
    0x79: 'Spawn Broodling',
    0x7A: 'EMP',
    0x7E: 'Launch Nuke',
    0x84: 'Lay Mine',
    0x8B: 'ComSat Scan',
    0x8D: 'Defense Matrix',
    0x8E: 'Psionic Storm',
    0x8F: 'Recall',
    0x90: 'Plague',
    0x91: 'Consume',
    0x92: 'Ensnare',
    0x93: 'Stasis',
    0x94: 'Hallucination',
    0x98: 'Patrol',
    0xB1: 'Heal',
    0xB4: 'Restore',
    0xB5: 'Disruption Web',
    0xB6: 'Mind Control',
    0xB8: 'Feedback',
    0xB9: 'Optic Flare',
    0xBA: 'Maelstrom',
    0xC0: 'Irradiate',
}

researches = {
    0x00: 'Stim Pack',
    0x01: 'Lockdown',
    0x02: 'EMP Shockwave',
    0x03: 'Spider Mines',
    0x05: 'Siege Tank',
    0x07: 'Irradiate',
    0x08: 'Yamato Gun',
    0x09: 'Cloaking Field (wraith)',
    0x0A: 'Personal Cloaking (ghost)',
    0x0B: 'Burrow',
    0x0D: 'Spawn Broodling',
    0x0F: 'Plague',
    0x10: 'Consume',
    0x11: 'Ensnare',
    0x13: 'Psionic Storm',
    0x14: 'Hallucination',
    0x15: 'Recall',
    0x16: 'Stasis Field',
    0x18: 'Restoration',
    0x19: 'Disruption Web',
    0x1B: 'Mind Control',
    0x1E: 'Optical Flare',
    0x1F: 'Maelstrom',
    0x20: 'Lurker Aspect',
}

upgrades = {
    0x00: 'Terran Infantry Armor',
    0x01: 'Terran Vehicle Plating',
    0x02: 'Terran Ship Plating',
    0x03: 'Zerg Carapace',
    0x04: 'Zerg Flyer Carapace',
    0x05: 'Protoss Ground Armor',
    0x06: 'Protoss Air Armor',
    0x07: 'Terran Infantry Weapons',
    0x08: 'Terran Vehicle Weapons',
    0x09: 'Terran Ship Weapons',
    0x0A: 'Zerg Melee Attacks',
    0x0B: 'Zerg Missile Attacks',
    0x0C: 'Zerg Flyer Attacks',
    0x0D: 'Protoss Ground Weapons',
    0x0E: 'Protoss Air Weapons',
    0x0F: 'Protoss Plasma Shields',
    0x10: 'U-238 Shells (Marine Range)',
    0x11: 'Ion Thrusters (Vulture Speed)',
    0x13: 'Titan Reactor (Science Vessel Energy)',
    0x14: 'Ocular Implants (Ghost Sight)',
    0x15: 'Moebius Reactor (Ghost Energy)',
    0x16: 'Apollo Reactor (Wraith Energy)',
    0x17: 'Colossus Reactor (Battle Cruiser Energy)',
    0x18: 'Ventral Sacs (Overlord Transport)',
    0x19: 'Antennae (Overlord Sight)',
    0x1A: 'Pneumatized Carapace (Overlord Speed)',
    0x1B: 'Metabolic Boost (Zergling Speed)',
    0x1C: 'Adrenal Glands (Zergling Attack)',
    0x1D: 'Muscular Augments (Hydralisk Speed)',
    0x1E: 'Grooved Spines (Hydralisk Range)',
    0x1F: 'Gamete Meiosis (Queen Energy)',
    0x20: 'Defiler Energy',
    0x21: 'Singularity Charge (Dragoon Range)',
    0x22: 'Leg Enhancement (Zealot Speed)',
    0x23: 'Scarab Damage',
    0x24: 'Reaver Capacity',
    0x25: 'Gravitic Drive (Shuttle Speed)',
    0x26: 'Sensor Array (Observer Sight)',
    0x27: 'Gravitic Booster (Observer Speed)',
    0x28: 'Khaydarin Amulet (Templar Energy)',
    0x29: 'Apial Sensors (Scout Sight)',
    0x2A: 'Gravitic Thrusters (Scout Speed)',
    0x2B: 'Carrier Capacity',
    0x2C: 'Khaydarin Core (Arbiter Energy)',
    0x2F: 'Argus Jewel (Corsair Energy)',
    0x31: 'Argus Talisman (Dark Archon Energy)',
    0x33: 'Caduceus Reactor (Medic Energy)',
    0x34: 'Chitinous Plating (Ultralisk Armor)',
    0x35: 'Anabolic Synthesis (Ultralisk Speed)',
    0x36: 'Charon Boosters (Goliath Range)',
}

unit_types = {
    0x00: 'Marine',
    0x01: 'Ghost',
    0x02: 'Vulture',
    0x03: 'Goliath',
    0x05: 'Siege Tank',
    0x07: 'SCV',
    0x08: 'Wraith',
    0x09: 'Science Vessel',
    0x0B: 'Dropship',
    0x0C: 'Battlecruiser',
    0x0E: 'Nuke',
    0x20: 'Firebat',
    0x22: 'Medic',
    0x25: 'Zergling',
    0x26: 'Hydralisk',
    0x27: 'Ultralisk',
    0x29: 'Drone',
    0x2A: 'Overlord',
    0x2B: 'Mutalisk',
    0x2C: 'Guardian',
    0x2D: 'Queen',
    0x2E: 'Defiler',
    0x2F: 'Scourge',
    0x32: 'Infested Terran',
    0x3A: 'Valkyrie',
    0x3C: 'Corsair',
    0x3D: 'Dark Templar',
    0x3E: 'Devourer',
    0x40: 'Probe',
    0x41: 'Zealot',
    0x42: 'Dragoon',
    0x43: 'High Templar',
    0x45: 'Shuttle',
    0x46: 'Scout',
    0x47: 'Arbiter',
    0x48: 'Carrier',
    0x53: 'Reaver',
    0x54: 'Observer',
    0x67: 'Lurker',
    0x6A: 'Command Center',
    0x6B: 'ComSat',
    0x6C: 'Nuclear Silo',
    0x6D: 'Supply Depot',
    0x6E: 'Refinery',
    0x6F: 'Barracks',
    0x70: 'Academy',
    0x71: 'Factory',
    0x72: 'Starport',
    0x73: 'Control Tower',
    0x74: 'Science Facility',
    0x75: 'Covert Ops',
    0x76: 'Physics Lab',
    0x78: 'Machine Shop',
    0x7A: 'Engineering Bay',
    0x7B: 'Armory',
    0x7C: 'Missile Turret',
    0x7D: 'Bunker',
    0x82: 'Infested CC',
    0x83: 'Hatchery',
    0x84: 'Lair',
    0x85: 'Hive',
    0x86: 'Nydus Canal',
    0x87: 'Hydralisk Den',
    0x88: 'Defiler Mound',
    0x89: 'Greater Spire',
    0x8A: 'Queens Nest',
    0x8B: 'Evolution Chamber',
    0x8C: 'Ultralisk Cavern',
    0x8D: 'Spire',
    0x8E: 'Spawning Pool',
    0x8F: 'Creep Colony',
    0x90: 'Spore Colony',
    0x92: 'Sunken Colony',
    0x95: 'Extractor',
    0x9A: 'Nexus',
    0x9B: 'Robotics Facility',
    0x9C: 'Pylon',
    0x9D: 'Assimilator',
    0x9F: 'Observatory',
    0xA0: 'Gateway',
    0xA2: 'Photon Cannon',
    0xA3: 'Citadel of Adun',
    0xA4: 'Cybernetics Core',
    0xA5: 'Templar Archives',
    0xA6: 'Forge',
    0xA7: 'Stargate',
    0xA9: 'Fleet Beacon',
    0xAA: 'Arbiter Tribunal',
    0xAB: 'Robotics Support Bay',
    0xAC: 'Shield Battery',
    0xC0: 'Larva',
    0xC1: 'Rine/Bat',
    0xC2: 'Dark Archon',
    0xC3: 'Archon',
    0xC4: 'Scarab',
    0xC5: 'Interceptor',
    0xC6: 'Interceptor/Scarab',
}
# }}}

class ReadError(Exception):
    pass

class Field(object):
    '''
    An object that represents one field in an action block.  Initialized
    with a datatype (Byte, Word or DWord) and a size.  `size` can be an
    integer or another Field instance, in which case the value that was
    read by that field is used as the length of this field.

    `creation_counter` is used so that we can keep track of which fields
    were created first in the different Actions.  I find this pretty ugly,
    it seems like it could possibly thread-unsafe, but if it's good enough
    for a large project like Django, I imagine it's good enough for my 
    small project (until I can figure out a better design, that is ;-))
    '''

    creation_counter = 0

    def __init__(self, datatype, size):
        self.datatype = datatype
        self.size = size
        self.data = None
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __repr__(self):
        return '<Field: %s%s>' % (self.size, self.datatype)

    def __cmp__(self, other):
        return self.creation_counter - other.creation_counter

    def read(self, buf):
        # If the Field has the `format` and `size` class attributes,
        # use them.  Otherwise, compute them.
        try:
            format, length = self.format, self.length
            fixed_size = True
        except AttributeError:
            format = '<%d%s' % (self.size.data, self.datatype)
            length = struct.calcsize(format)
            fixed_size = False
        s = buf.read(length)
        try:
            t = struct.unpack(format, s)
        except struct.error:
            raise  ReadError('Could not read %d bytes, only %d available'
                            % (length, len(s)))

        if fixed_size:
            try:
                (self.data,) = t
            except ValueError:
                self.data = t
        else:
            self.data = t
        return length


class ActionBase(type):
    '''
    Meta-class for all Action objects.  This will set a `base_fields`
    attribute containing an AssocList of the binary fields to read, ordered by
    their creation_counter (as specified in datatypes.DataType.)
    '''
    def __new__(cls, name, base, attrs):
        attrs['name'] = attrs.get('name') or name
        attrs['base_fields'] = dict(ActionBase.get_declared_fields(attrs))
        # Optimization: set the instance attribute `format` and `length`
        # for all Fields that have a constant (i.e.: integer) size.
        for field in attrs['base_fields'].itervalues():
            if isinstance(field.size, int):
                field.format = '<%d%s' % (field.size, field.datatype)
                field.length = struct.calcsize(field.format)
        return super(ActionBase, cls).__new__(cls, name, base, attrs)

    def get_declared_fields(attrs):
        for attr in attrs.iteritems():
            if isinstance(attr[1], Field):
                yield attr
    get_declared_fields = staticmethod(get_declared_fields)


class Action(object):
    '''
    Base class for all Action objects.  All subclasses should define
    an `id` attribute and the different data fields of that particular
    action.  The `name` attribute can optionally be set if the name
    of the action differs from the name of the class (useful if you
    wish to use spaces.)
    '''
    __metaclass__ = ActionBase

    def __init__(self, tick):
        self.tick = tick

    def __str__(self):
        return '<Action (%s)>' % self.name

    def __repr__(self):
        return str(self)

    def read(self, buf):
        length = 0
        for (field_name, field) in sorted(self.base_fields.iteritems(),
                                          key=operator.itemgetter(1)):
            length += field.read(buf)
            setattr(self, field_name, field.data)
        return length


class Select(Action):
    id = 0x09
    count = Field(Byte, 1)
    unit_ids = Field(Word, count)


class ShiftSelect(Action):
    id = 0x0A
    name = 'Shift Select'
    count = Field(Byte, 1)
    unit_ids = Field(Word, count)


class ShiftDeselect(Action):
    id = 0x0B
    name = 'Shift Deselect'
    count = Field(Byte, 1)
    unit_ids = Field(Word, count)


class Build(Action):
    id = 0x0C
    building_type_id = Field(Byte, 1)
    pos_x = Field(Word, 1)
    pos_y = Field(Word, 1)
    building_id = Field(Word, 1) # Make a mapping for further reference?

    def get_building_type(self):
        return unit_types[self.building_type_id]


class Vision(Action):
    id = 0x0D
    unknown = Field(Byte, 2)


class Ally(Action):
    id = 0X0E
    unknown = Field(Byte, 4)


class Hotkey(Action):
    id = 0x13
    set_or_get = Field(Byte, 1) # 0 for set, 1 for get
    group = Field(Byte, 1)


class Move(Action):
    id = 0x14
    pos_x = Field(Word, 1)
    pos_y = Field(Word, 1)
    unit_id = Field(Word, 1) # 0xFFFF for moving to X/Y, unit id if following
    unknown1 = Field(Word, 1)
    unknown2 = Field(Byte, 1)


class Attack(Action):
    id = 0x15
    pos_x = Field(Word, 1)
    pos_y = Field(Word, 1)
    unit_id = Field(Word, 1) # 0xFFFF for moving to X/Y, unit id if following
    unknown = Field(Word, 1)
    type_id = Field(Byte, 1) # Taken from `attacks`
    shifted = Field(Byte, 1) # 0x00 for normal, 0x01 for shifted attack

    def get_type(self):
        return attack[self.type_id]


class Cancel(Action):
    id = 0x18


class CancelHatch(Action):
    id = 0x19
    name = 'Cancel hatch'


class Stop(Action):
    id = 0x1A
    unknown = Field(Byte, 1)


class ReturnCargo(Action):
    id = 0x1E
    name = 'Return cargo'
    unknown = Field(Byte, 1)


class Train(Action):
    id = 0x1F
    unit_type_id = Field(Word, 1)

    def get_unit_type(self):
        return unit_types[self.unit_type_id]


class CancelTrain(Action):
    id = 0x20
    name = 'Cancel train'
    unknown = Field(Byte, 2)


class Cloak(Action):
    id = 0x21
    unknown = Field(Byte, 1)


class Decloak(Action):
    id = 0x22
    unknown = Field(Byte, 1)


class Hatch(Action):
    id = 0x23
    unit_type_id = Field(Word, 1)

    def get_unit_type(self):
        return unit_types[self.unit_type_id]


class Unsiege(Action):
    id = 0x25
    unknown = Field(Byte, 1)


class Siege(Action):
    id = 0x26
    unknown = Field(Byte, 1)


class BuildInterceptor(Action):
    id = 0x27
    name = 'Build Interceptor/Scarab'


class UnloadAll(Action):
    id = 0x28
    name = 'Unload all'
    unknown = Field(Byte, 1)


class Unload(Action):
    id = 0x29
    unknown = Field(Byte, 2)


class MergeArchon(Action):
    id = 0x2A
    name = 'Merge Archon'


class HoldPosition(Action):
    id = 0x2B
    name = 'Hold position'
    unknown = Field(Byte, 1)


class Burrow(Action):
    id = 0x2C
    unknown = Field(Byte, 1)


class Unburrow(Action):
    id = 0x2D
    unknown = Field(Byte, 1)


class CancelNuke(Action):
    id = 0x2E
    name = 'Cancel nuke'


class Lift(Action):
    id = 0x2F
    unknown = Field(Byte, 4)


class Research(Action):
    id = 0x30
    research_id = Field(Byte, 1) # Taken from `researches` 


class CancelResearch(Action):
    id = 0x31
    name = 'Cancel research'


class Upgrade(Action):
    id = 0x32
    upgrade_id = Field(Byte, 1) # Taken from `upgrades`


class Morph(Action):
    id = 0x35
    building_type_id = Field(Word, 1)

    def get_building_type(self):
        return unit_types[self.building_type_id]


class Stim(Action):
    id = 0x36


class LeaveGame(Action):
    id = 0x57
    reason = Field(Byte, 1) # 0x01 for quit, 0x06 for drop


class MergeDarkArchon(Action):
    id = 0x5A
    name = 'Merge Dark Archon'


# Accumulate all the Action subclasses in a dictionary and use their
# `id` attribute to index them.
action_classes = dict((cls.id, cls) for cls in Action.__subclasses__())
