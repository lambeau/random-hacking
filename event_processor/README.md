# Event Processor

### Usage

The program assumes there is a file present named `input.json` in the current
working directory that has a single json object per line with at least the following
fields:

```
{"id": <value>, "wait": <positive numeric value>}
```

If the preceding is true, then the program can be run as follows:

```
./event_processor.py
```

### Output

* `> <id>`: event has been received into the system
* `processed <id>`: event has been processed
* `< <id>`: event has been distributed

**Example**:
```
> 1
> 2
> 3
processed 2
> 4
processed 3
processed 1
< 1
< 2
processed 4
< 3
< 4
```

### Dependencies

* Python >= 3.2 (for `concurrent.futures` library)

## Thoughts

#### Approach

I approached this problem by first implementing a simple, single-threaded
example. When I got that working, I broke the functionality down into three
components: receiving, processing and distributing events. At first
I tried to have each of these components run in their own process using the
`multiprocessing` library and using `Queue` for message passing between them.
For processing the events, I used `Pool.apply_async()` with a callback that
put the result in the outgoing queue. This approach led to good performance,
but lacked the output-in-order requirement.

I wanted to have the three components be able to run without any shared state
to enable maximum scalability, but decided against it for the reason that I
did not want to depend on the content of the events themselves. Otherwise,
distributor process could inspect the `id` field and reorder the events based
on that.

Instead, I went with the approach of having the receiving and distributing
tasks run in the same process, but different threads. I still used queues
for message passing, but put a `Future` object in the outgoing queue that
the distributor process could then block on when retrieving the result. The
future came from submitting a task to an `Executor`; this could be scaled
out depending on the performance needs of the service.

Overall, this program was built with the mindset that it would be a
long-running server process. The receive component could easy be replaced with
something that receives events as they come in. Likewise, the distributor
just needs the `if id == <end of sample file>` block removed to run longer.

#### Open items

* Is is possible to have this implemented so that there is no shared state
  between components?
* Would this need to be backed by a reliable message passing architecture,
  like AMQP?
