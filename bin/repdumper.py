from optparse import OptionParser
import sys

from pyreplib import replay


VERSION = (0, 1, 0)
AVAILABLE_FORMATS = ['json', 'yaml', 'xml']

def action_to_dict(action):
    '''
    Return an action as a dictionary.  The key `action` designates the action
    type and all base fields are added.  If there are methods starting with
    'get_', call those and assign their result to the key formed by removing
    the 'get_' prefix from the method name.
    '''
    d = {'action': action.name, 'tick': action.tick}
    d.update(dict((key, getattr(action, key))
                  for key in action.base_fields.iterkeys()))

    # get_* method calls
    if action.name == 'Build':
        d['building_type'] = action.get_building_type()
    elif action.name == 'Attack':
        d['type'] = action.get_type()
    elif action.name == 'Train':
        d['unit_type'] = action.get_unit_type()
    elif action.name == 'Hatch':
        d['unit_type'] = action.get_unit_type()
    elif action.name == 'Research':
        d['research'] = action.get_research()
    elif action.name == 'Upgrade':
        d['upgrade'] = action.get_upgrade()
    elif action.name == 'Morph':
        d['building_type'] = action.get_building_type()
    elif action.name == 'Leave Game':
        d['reason'] = action.get_reason()

    return d

def player_to_dict(player):
    return {
        'name': player.name,
        'race': player.race_name,
        'type': player.type,
        'slot': player.slot,
        'number': player.number,
        'human': player.human,
        'actions': [action_to_dict(action) for action in player.actions],
    }

def replay_to_dict(replay):
    return {
        'date': replay.timestamp,
        'engine': replay.engine_name,
        'frames': replay.game_frames,
        'game_name': replay.game_name,
        'creator': replay.creator,
        'map_name': replay.map_name,
        'map_size': (replay.map_width, replay.map_height),
        'player_slots': [player_to_dict(player)
                         for player in replay.player_slots],
    }

def dump_json(replay):
    try:
        from cjson import encode
    except ImportError:
        from simplejson import dumps as encode
    print encode(replay_to_dict(replay))


def dump_yaml(replay):
    import yaml
    print yaml.safe_dump(replay_to_dict(replay))


def dump_xml(replay):
    from xml.sax.saxutils import XMLGenerator
    d = replay_to_dict(replay)
    players = d.pop('player_slots')
    gen = XMLGenerator(encoding="utf-8")
    gen.startDocument()
    gen.startElement('replay', {})

    for key, value in d.iteritems():
        gen.startElement(key, {})
        gen.characters(str(value))
        gen.endElement(key)

    gen.startElement('players', {})
    for player in players:
        actions = player.pop('actions')
        gen.startElement('player', {})
        for key, value in player.iteritems():
            gen.startElement(key, {})
            gen.characters(str(value))
            gen.endElement(key)

        gen.startElement('actions', {})
        for action in actions:
            gen.startElement('action', {})
            for key, value in action.iteritems():
                gen.startElement(key, {})
                gen.characters(str(value))
                gen.endElement(key)
            gen.endElement('action')
        gen.endElement('actions')
        gen.endElement('player')
    gen.endElement('players')

    gen.endElement('replay')
    gen.endDocument()


def version_to_string(seq):
    return '.'.join(map(str, seq))

def make_parser():
    parser = OptionParser(usage='%prog [options] <replay file>',
                          version=version_to_string(VERSION))
    parser.set_defaults(format='json')
    parser.add_option('-f', '--format', dest='format',
                      choices=AVAILABLE_FORMATS, metavar='FORMAT',
                      help='Output FORMAT %s' % AVAILABLE_FORMATS)
    return parser


def main():
    if not AVAILABLE_FORMATS:
        print 'error: no output format module is available.'
        sys.exit(1)

    parser = make_parser()
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error('no replay file specified.')
    elif len(args) > 1:
        parser.error('only one replay file may be dumped at a time.')

    rep = replay.Replay(args[0])
    if options.format == 'json':
        dump_json(rep)
    elif options.format == 'yaml':
        dump_yaml(rep)
    elif options.format == 'xml':
        dump_xml(rep)

if __name__ == '__main__':
    main()
