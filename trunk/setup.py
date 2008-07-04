from distutils.core import setup, Extension

module1 = Extension('_unpack',
                    sources=['src/pyunpack.c',
                             'src/unpack.c'])

if __name__ == '__main__':
    setup(name='Broodwar Replay File Unpacker',
          version='0.1',
          description='Helper C module.',
          ext_modules=[module1])
