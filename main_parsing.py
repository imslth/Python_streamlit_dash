import os
import time
import schedule

schedule.every().day.at("12:57").do(lambda: os.system('scrapy runspider Parsing_developers.py'))
schedule.every().day.at("13:15").do(lambda: os.system('scrapy runspider Parsing_dilers.py'))


while True:
    schedule.run_pending()
    time.sleep(1)



if __name__ == '__main__':
    main()
