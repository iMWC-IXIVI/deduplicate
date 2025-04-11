import uuid
import hashlib
import json
import redis

from datetime import datetime

from celery_app import app

from db.orm import get_connection


redis_client = redis.StrictRedis(host='redis', port=6379)
connect = get_connection()


@app.task
def deduplicate(data: dict):
    data_string = json.dumps(data).encode()
    data_hash = hashlib.blake2s(data_string).hexdigest()

    if redis_client.exists(data_hash):
        return 'Duplicate'

    query_data = connect.select(['hash'], 'original', {'hash': data_hash})

    if query_data:
        return 'Deduplicate'

    redis_client.set(data_hash, 'hash')
    redis_client.expire(data_hash, 60)

    uuid_data = uuid.uuid4()
    dt_data = datetime.now()

    connect.insert('original', ['hash', 'id', 'raw_data', 'created'], [(data_hash, uuid_data, data_string, dt_data), ])

    return 'Success'
