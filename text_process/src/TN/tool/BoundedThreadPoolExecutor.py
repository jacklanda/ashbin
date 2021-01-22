# -*- coding: UTF-8 -*-
from concurrent.futures import ThreadPoolExecutor
import queue
class BoundedThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers=None, thread_name_prefix=''):
        super().__init__(max_workers, thread_name_prefix)
        # self._work_queue = queue.Queue(self._max_workers * 2)  # 队列大小为最大线程数的两倍
        self._work_queue = queue.Queue(self._max_workers)  # 队列大小为最大线程数的两倍