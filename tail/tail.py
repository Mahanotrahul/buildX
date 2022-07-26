#!/usr/bin/env python3

import sys
import os
import time

BUF_SIZE = 512

class Tail():
    def __init__(self, filename, n=10):
        self.filename = filename
        self.n = n

    def tailer(self):
        try:
            with open(self.filename) as f:
                self._file = f
                self._file.seek(0, os.SEEK_END)
                self._file_length = self._file.tell()
                self._printlastlines()

                while True:
                    line = self._file.readline()
                    if line: sys.stdout.write(line)
                    else: time.sleep(1)
        except KeyboardInterrupt as e:
            print("Interrupted. Exiting")
            self._file.close()
        except Exception as e:
            print(e)
            self._file.close()

    def _printlastlines(self):
        bytes_per_line = BUF_SIZE    # initial assumption. we will modify it later.
        bytes_to_read = bytes_per_line * self.n     # if we have x bytes_per_line and we want to read n lines, so total bytes to read would be the multiplication of both

        # start reading
        while True:
            print("bytes to read : {}".format(bytes_to_read))
            if bytes_to_read >= self._file_length:      # if bytes to read is already greater then filesize, it means we can read from filestart
                print("bytes to read >= filelength : {}".format(bytes_to_read))
                self._file.seek(0, 0)
                last_lines = self._file.read().split('\n')[-self.n:]
                break
                
            else:
                print("bytes to read < filelength : {}".format(bytes_to_read))
                # first move the pointer to the end and then go back byte_to_read bytes backwards.
                # we cannot do this => f.seek(-bytes_to_read, SEEK_END)
                # because python3.2+ doesnot allow negative bytes to be read from seek end (unless file is opened in binary mode)
                # so we use seek_set

                self._file.seek(0, os.SEEK_END)
                self._file.seek(self._file_length-bytes_to_read, os.SEEK_SET)

                last_words = self._file.read(bytes_to_read)
                line_breaks = len(last_words.split('\n'))
                print("line breaks : {}".format(line_breaks))

                if line_breaks >= self.n:   # we reached just above the n lines, so we print the last n lines
                    print("line breaks >= n : {}".format(line_breaks))
                    last_lines = last_words.split('\n')[-self.n:]
                    break
                
                else:       # we are still not there above n lines, so we need to up our bytes_per_line => that in turn updates our bytes_to_read
                    print("line breaks < n : {}".format(line_breaks))

                    if line_breaks == 0:        # if we have not crossed even 1 line from the end, then bytes_to_read is significantly small
                        bytes_to_read = bytes_to_read * self.n
                    else:
                        bytes_per_line = bytes_to_read/line_breaks      # since linebreaks is smaller then n, we calculate approx. bytes in each line and then multiply that with n to reach just above n lines
                        bytes_to_read = round(bytes_per_line * self.n)
            time.sleep(1)       # sleep(1) just to visualize the bytes_to_read decision being taken during start


        sys.stdout.write('\n'.join(last_lines))
        sys.stdout.flush()
        # sys.stdout.write('')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("filename missing")
        sys.exit(1)
    else:
        filename = sys.argv[1]
    if len(sys.argv) >= 2:
        n = int(sys.argv[2])

    file = Tail(filename, n)
    file.tailer()


