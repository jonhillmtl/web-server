from os import environ
import sys
import nose

if __name__ == '__main__':
    environ['NOSE_WITH_DOCTEST'] = '1'
    environ['NOSE_NOCAPTURE'] = '1'
    nose.main()
