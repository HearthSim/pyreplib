from distutils.core import setup, Extension

pyunpack = Extension('pyreplib/_unpack',
                     sources=['src/pyunpack.c',
                              'src/unpack.c'])

if __name__ == '__main__':
    setup(name='pyreplib',
          author='Vincent Foley',
          author_email='vfoleybourgon@yahoo.ca',
          version='0.0.1',
          description="Python library to read Starcraft's replay files",
          packages=['pyreplib'],
          ext_modules=[pyunpack])
