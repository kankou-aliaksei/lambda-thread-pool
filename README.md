# AWS Lambda thread pool (lambda-thread-pool)

You cannot use "multiprocessing.Queue" or "multiprocessing.Pool" within a Python Lambda environment because the Python Lambda execution environment does not support shared memory for processes.

You will see an issue if you attempt to use Pool:

```
{
  "errorMessage": "[Errno 38] Function not implemented",
  "errorType": "OSError",
  "requestId": <request_id>,
  "stackTrace": [
    "  File \"/var/task/lambda_function.py\", line 10, in lambda_handler\n    pool = Pool(10)\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/pool.py\", line 927, in __init__\n    Pool.__init__(self, processes, initializer, initargs)\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/pool.py\", line 196, in __init__\n    self._change_notifier = self._ctx.SimpleQueue()\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/context.py\", line 113, in SimpleQueue\n    return SimpleQueue(ctx=self.get_context())\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/queues.py\", line 341, in __init__\n    self._rlock = ctx.Lock()\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/context.py\", line 68, in Lock\n    return Lock(ctx=self.get_context())\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/synchronize.py\", line 162, in __init__\n    SemLock.__init__(self, SEMAPHORE, 1, 1, ctx=ctx)\n",
    "  File \"/var/lang/lib/python3.9/multiprocessing/synchronize.py\", line 57, in __init__\n    sl = self._semlock = _multiprocessing.SemLock(\n"
  ]
}
```

AWS Lambda thread pool (lambda-thread-pool) uses "multiprocessing.Pipe" instead of "multiprocessing.Queue". It provides the ability to perform parallel execution within the AWS lambda Python execution environment.

# Prerequisites
* python3
* pip
* AWS Credentials

# Install
pip install lambda-thread-pool

# Usage

```
from lambda_thread_pool import LambdaThreadPool


def test_func(index, message):
    print(index, message, end='\n')
    return message


def lambda_handler(event, context):
    pool = LambdaThreadPool()

    results = []

    for i in range(10):
        res = pool.apply_async(test_func, (i, f'Message: {i}'))
        results.append(res)

    pool.join()

    for result in results:
        print('Result:', result.get())

```
