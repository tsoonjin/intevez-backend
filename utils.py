import json
import pandas as pd
import uuid
import time

class_name = 'furniture'


def retry(max_retries, wait_time):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            if retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    retries += 1
                    time.sleep(wait_time)
            else:
              raise Exception(f"Max retries of function {func} exceeded")
        return wrapper
    return decorator

def omit(d, keys):
    return {x: d[x] for x in d if x not in keys}

def process_weaviate_object(object):
    processed = {
        "image_url": "https://source.unsplash.com/collection/1163637/480x480",
        "score": object["_additional"]["score"],
        **omit(object, ['_additional'])
    }
    print(processed)
    return processed

@retry(max_retries=3, wait_time=2)
def weaviate_search(query, client, keys, N=10):
    response = (
        client.query
        .get("furniture", keys)
        .with_hybrid(
            query=query,
        )
        .with_additional(["score"])
        .with_limit(N)
        .do()
    )
    print(response)
    result = [
        process_weaviate_object(x)
        for x in response['data']['Get'][class_name.title()]
    ]
    return result
