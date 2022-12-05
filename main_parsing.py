import os
import time
import schedule

# Устанавливаем в задачник запуск двух скриптов по парсингу данных. В нашем случае используем паука scrapy без проекта

schedule.every().day.at("00:01").do(lambda: os.system('scrapy runspider Parsing_developers.py'))
schedule.every().day.at("01:05").do(lambda: os.system('scrapy runspider Parsing_dilers.py'))


while True:
    schedule.run_pending()
    time.sleep(1)



if __name__ == '__main__':
    main()
