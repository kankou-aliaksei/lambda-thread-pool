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
