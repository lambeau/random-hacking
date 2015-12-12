#!/usr/bin/env python3

import concurrent.futures
import threading
import queue
import time
import json


def main():
    incoming = queue.Queue()
    outgoing = queue.Queue()

    receiver = threading.Thread(target=receive, args=(incoming,), daemon=True)
    processor = threading.Thread(target=process, args=(incoming, outgoing), daemon=True)
    distributor = threading.Thread(target=distribute, args=(outgoing,))

    receiver.start()
    processor.start()
    distributor.start()

    distributor.join()


def receive(incoming):
    with open('input.json', 'r') as file:
        for line in file:
            event = json.loads(line)
            print('> {}'.format(event['id']))
            incoming.put(event)


def process(incoming, outgoing):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        while True:
            event = incoming.get()
            future = executor.submit(process_change, event)
            outgoing.put(future)


def process_change(event):
    start = time.time()
    while time.time() - start < event['wait']:
        time.sleep(0.0001)
    print('processed {}'.format(event['id']))
    return event


def distribute(outgoing):
    start = time.time()
    while True:
        event = outgoing.get().result()
        print('< {}'.format(event['id']))
        if event['id'] == 1234:
            print('done! elapsed time: {}'.format(time.time() - start))
            break


if __name__ == '__main__':
    main()
