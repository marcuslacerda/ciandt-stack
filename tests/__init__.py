"""Package for tests."""
import os
import sys
import logging

sys.path.insert(1, os.path.abspath(os.curdir))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'lib_tests'))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'jobs'))
# sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'server', 'app'))

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

# print sys.path
