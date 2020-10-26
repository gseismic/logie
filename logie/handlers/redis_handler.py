from redis import ResponseError


class RedisHandler(BaseHandler):

    def __init__(self, host='127.0.0.1', port=6379, key='redis',
                 extra_fields=None, flush_threshold=128, flush_time=1,
                 level=NOTSET, filter=None, password=False, bubble=True,
                 context=None, push_method='rpush'):

        try:
            self.redis.ping()
        except ResponseError:
            raise ResponseError(
                'The password provided is apparently incorrect')

        self._stop_event = threading.Event()
        self._flushing_t = threading.Thread(target=self._flush_task,
                                            args=(flush_time,
                                                  self._stop_event))
        self._flushing_t.daemon = True
        self._flushing_t.start()

    def _flush_task(self, flush_time, stop_event):
        while not self._stop_event.isSet():
            with self.lock:
                self._flush_buffer()

    def _flush_buffer(self):
        """Flushes the messaging queue into Redis.

        All values are pushed at once for the same key.
        The method rpush/lpush is defined by push_method argument
        """
        if self.queue:
            getattr(self.redis, self.push_method)(self.key, *self.queue)
        self.queue = []

    def emit(self, record):
        with self.lock:
            r = {"message": record.msg,
                 "host": platform.node(),
                 "level": record.level_name,
                 "time": record.time.isoformat()}
            r.update(self.extra_fields)
            r.update(record.kwargs)
            self.queue.append(json.dumps(r))
            if len(self.queue) == self.flush_threshold:
                self._flush_buffer()

    def close(self):
        self._flush_buffer()
