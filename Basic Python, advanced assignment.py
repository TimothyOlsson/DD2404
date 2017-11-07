import logging
import time
import pdb

pdb.set_trace()

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='example.log',
                    level=logging.DEBUG)
                    
logging.info('\n\n########\nStart of run')

k=5
logging.info(str(k))

y=0
logging.warning('This is a warning. y = %s',str(y))

q=None
logging.error('This is an error, x = %s', str(q))
time.sleep(5)
try:
  x = 1/y
except Exception as e:
  logging.critical('Error message: %s', str(e))