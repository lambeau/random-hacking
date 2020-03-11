import random
import asyncio

#https://www.raspberrypi.org/documentation/linux/usage/systemd.md

async def read_in(queue):
    while True:
        print(queue.qsize())
        await queue.put(random.randint(0, 100))
        #await asyncio.sleep(.001)


async def process(in_q, out_q):
    while True:
        item = await in_q.get()
        print('process', item)
        await out_q.put(item)


async def print_out(queue):
    while True:
        item = await queue.get()
        print(item)


def main():
    in_q = asyncio.Queue(maxsize=100)
    out_q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.create_task(read_in(in_q))
    loop.create_task(process(in_q, out_q))
    loop.create_task(print_out(out_q))
    loop.run_forever()


if __name__ == '__main__':
    main()
