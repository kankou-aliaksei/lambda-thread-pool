from multiprocessing import Process, Pipe


class LambdaThreadPool:
    def __init__(self, *args):
        self.__connections = []
        self.__processes = []

    class __ResultWrapper:
        def __init__(self, conn):
            self.__conn = conn

        def get(self):
            return self.__conn.recv()

    def apply_async(self, handler, handler_args_tuple):
        parent_conn, child_conn = Pipe()
        self.__connections.append(parent_conn)
        args = (child_conn, handler) + handler_args_tuple
        process = Process(target=self.__handler_wrapper, args=args)
        self.__processes.append(process)
        process.start()
        return self.__ResultWrapper(parent_conn)

    def join(self):
        for process in self.__processes:
            process.join()

    def close(self):
        pass

    @staticmethod
    def __handler_wrapper(conn, handler, *args):
        conn.send(handler(*args))
        conn.close()
