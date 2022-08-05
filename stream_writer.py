import requests
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from datetime import datetime


class StreamWriter(object):
    server_url = ''
    file_size = 0.0
    bitrate = 64.0
    stream_length = 0.0
    metadata = {}

    def __init__(self, server_url, seconds, destination='./', filename='output.mp3'):
        self.server_url = server_url
        self.seconds = seconds
        self.destination = destination
        self.filename = filename

    def record(self):
        """ 
        This method records the file stream until the stream_length has been reached
        """
        while True:
            with open(self.destination+self.filename, 'w+b') as handle:
                request = requests.get(self.server_url, stream=True)
                self.metadata = request.headers

                self.bitrate = float(self.metadata['icy-br'].split(',')[0])

                for block in request.iter_content(1024):
                    self.file_size += 1024.0

                    if ((self.file_size/1024.0) * 8.0) / self.bitrate > self.seconds:
                        break_it_boy = True
                        break

                    if not block:
                        break

                    handle.write(block)

                if break_it_boy:
                    break

            if break_it_boy:
                break

        self.calc_length()

        return True

    def calc_length(self):
        self.stream_length = ( ( self.file_size/1024.0 ) * 8.0 )/self.bitrate
