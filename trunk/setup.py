from distutils.core import setup, Extension

module1 = Extension('_unpack',
                    sources=['pyunpack.c', 'unpack.c'])

setup(name='Broodwar Replay File Unpacker',
      version='0.1',
      description='Helper C module.',
      ext_modules=[module1])
