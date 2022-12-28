import os
import time
import schedule

# Устанавливаем в задачник запуск скрипта по парсингу данных. В нашем случае используем паука scrapy без проекта

schedule.every().day.at("00:18").do(lambda: os.system('scrapy runspider Parsing.py'))

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
    main()
