import requests
import sched, time
import logging
import os
import datetime

current_time = datetime.datetime.now().strftime ('%H_%M_%S')

logger = logging.getLogger(__name__)
log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)


def get_bitcoin_price():
  """
  Fetches latest bitcoin price
  :return: Bitcoin price in USD
  :rtype: Float
  """
  
  try:
    logger.info('Sending request ...')   
    response = requests.get(TICKER_API_URL)
  except Exception as err:
    logger.error(err)
  response_json = response.json()
   
  return (response_json['bpi']['USD']['rate_float'])


#writing to file

def write_to_file(filepath):
  """
  Writes content to the file as Time Series
  :param filepath: Path to the file
  :type filepath: string
  """
  try:
    logger.info('Writing to file {0}'.format(filepath))   
    with open(filepath, "a+") as f:
      f.write('\n'+str(get_bitcoin_price())+ ',' + str(time.time()))
      f.close()
  except IOError:
    logger.error("File not accessible")


##Scheduler

s = sched.scheduler(time.time, time.sleep)
def write_on_schedule(filepath):
  """
  Function to write data to file in intervals
  :param filepath: Path to the file
  :type filepath: string
  """
  write_to_file(filepath)
  s.enter(5, 1, write_on_schedule,argument=(filepath,))
  s.run()

if __name__ == "__main__":

  TICKER_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
  FILEPATH = "bitcoin.data"

  if os.path.isfile(FILEPATH):
    logger.info('Backing up the old file')
    os.rename(FILEPATH,(FILEPATH + '_' + str(current_time)))

  write_on_schedule(FILEPATH)


