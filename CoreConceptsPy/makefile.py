# This is a helper script to run the tests and examples where make does not work seamlessly *caugh* windows *caugh* ...

import fnmatch
import os
import subprocess
import sys
import unittest

examples = {
    'events': [
        'example-1.py',
        'example-2.py',
        'example-3.py',
        'example-4.py',
        'example-5.py'
    ],
    'fields': [],
    'locations': [],
    'networks': [
        'karate.py',
        'ucsb.py'
    ],
    'objects': []
}

def usage():
    print 'Usage: python %s test-events|fields|locations|networks|objects|all' % (sys.argv[0])
    print '  or:  python %s example-events|fields|locations|networks|objects|all' % (sys.argv[0])

def clean():
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.pyc'):
            os.remove(os.path.join(root, filename))

def test(selector):
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.discover('test', selector, '..'))
    unittest.TextTestRunner().run(suite)

def example(selector = None):
    for cc in examples:
        if selector == None or cc == selector:
            for f in examples[cc]:
                subprocess.call('python examples/' + cc + '/' + f, shell = True)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        clean()
        if sys.argv[1] == 'test-events':
            test('events')
        elif sys.argv[1] == 'test-fields':
            test('fields')
        elif sys.argv[1] == 'test-locations':
            test('locations')
        elif sys.argv[1] == 'test-networks':
            test('networks')
        elif sys.argv[1] == 'test-objects':
            test('objects')
        elif sys.argv[1] == 'test-all':
            test('*')
        elif sys.argv[1] == 'example-events':
            example('events')
        elif sys.argv[1] == 'example-fields':
            pass
        elif sys.argv[1] == 'example-locations':
            pass
        elif sys.argv[1] == 'example-networks':
            example('networks')
        elif sys.argv[1] == 'example-objects':
            pass
        elif sys.argv[1] == 'example-all':
            example()
        else:
            usage()
    else:
        usage()
