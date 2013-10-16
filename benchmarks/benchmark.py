# -*- coding: utf-8 -*-

import gevent
import gevent.monkey
gevent.monkey.patch_all()
import gevent.pool

import gsocketpool.pool
import time
import uuid

from bkyototycoon import KyotoTycoonConnection, KyotoTycoonPoolConnection
from kyototycoon import KyotoTycoon

NUM_REQUESTS = 5000
NUM_BULK = 5


def _create_request():
    return [{uuid.uuid1().hex:'1' for n in xrange(NUM_BULK)} for n in xrange(NUM_REQUESTS)]


def benchmark_get_bulk():
    client = KyotoTycoonConnection()
    requests = _create_request()

    [client.set_bulk(req) for req in requests]

    start = time.time()
    [client.get_bulk(req.keys()) for req in requests]
    print 'get_bulk qps:', int(NUM_REQUESTS * NUM_BULK / (time.time() - start))


def benchmark_set_bulk():
    client = KyotoTycoonConnection()
    requests = _create_request()

    start = time.time()
    [client.set_bulk(req) for req in requests]
    print 'set_bulk qps:', int(NUM_REQUESTS * NUM_BULK / (time.time() - start))


def benchmark_get_bulk_with_pool():
    client = KyotoTycoonConnection()
    requests = _create_request()

    [client.set_bulk(req) for req in requests]

    conn_pool = gsocketpool.pool.Pool(KyotoTycoonPoolConnection, initial_connections=50)
    glet_pool = gevent.pool.Pool(50)

    def _run(req):
        with conn_pool.connection() as client:
            client.get_bulk(req.keys())

    start = time.time()
    [_ for _ in glet_pool.imap_unordered(_run, requests)]
    print 'get_bulk_with_pool qps:', int(NUM_REQUESTS * NUM_BULK / (time.time() - start))


def benchmark_set_bulk_with_pool():
    conn_pool = gsocketpool.pool.Pool(KyotoTycoonPoolConnection, initial_connections=50)
    glet_pool = gevent.pool.Pool(50)

    requests = _create_request()

    def _run(req):
        with conn_pool.connection() as client:
            client.set_bulk(req)

    start = time.time()
    [_ for _ in glet_pool.imap_unordered(_run, requests)]
    print 'set_bulk_with_pool qps:', int(NUM_REQUESTS * NUM_BULK / (time.time() - start))


def benchmark_kyototycoon_get_bulk():
    client = KyotoTycoon()
    client.open()

    requests = _create_request()

    [client.set_bulk(req) for req in requests]

    start = time.time()
    [client.get_bulk(req.keys()) for req in requests]
    print 'python-kyototycoon get_bulk qps:', int(NUM_REQUESTS * NUM_BULK / (time.time() - start))


def benchmark_kyototycoon_set_bulk():
    client = KyotoTycoon()
    client.open()

    requests = _create_request()

    start = time.time()
    [client.set_bulk(req) for req in requests]
    print 'python-kyototycoon set_bulk qps:', int(NUM_REQUESTS * NUM_BULK / (time.time() - start))


benchmark_get_bulk()
benchmark_set_bulk()
benchmark_get_bulk_with_pool()
benchmark_set_bulk_with_pool()
benchmark_kyototycoon_get_bulk()
benchmark_kyototycoon_set_bulk()
