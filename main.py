#! /usr/bin/env python
import schedule
import time 
from datetime import datetime
from stream_writer import StreamWriter

def job():
    print('Gravando bolicho')

    s = StreamWriter('https://ice.fabricahost.com.br/radiotweb',
        100,
        filename=datetime.strftime(
            datetime.now(), '%Y-%m-%d_%H_%M_%S.mp3'),
        destination='./recorded/'
    )
    s.record()
    print('Fim da gravação')


schedule.every().day.at("17:59:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)