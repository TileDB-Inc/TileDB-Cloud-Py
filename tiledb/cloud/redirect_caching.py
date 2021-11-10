class PoolManagerCachingWrapper:
    def __init__(self, pool_manager):
        self._pool = pool_manager
        self._redirect_cache = {}

    def request(self, method, url, **kwargs):
        resp = self._pool.request(method, self._redirect_cache.get(url, url), **kwargs)

        for retry in reversed(resp.retries.history):
            if retry.redirect_location:
                self._redirect_cache[url] = retry.redirect_location
                break

        return resp
