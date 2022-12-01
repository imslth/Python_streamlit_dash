import os
import time
import schedule

schedule.every().day.at("00:01").do(lambda: os.system('scrapy runspider Parsing_developers.py'))
schedule.every().day.at("00:30").do(lambda: os.system('scrapy runspider Parsing_dilers.py'))


while True:
    schedule.run_pending()
    time.sleep(1)



if __name__ == '__main__':
    main()
