from collections import Counter
from hashlib import sha256
import ujson


def hash_response(r, post_processor=None):
    r = post_processor(r) if post_processor else r
    r_text = ujson.dumps(r, sort_keys=True)  # sorted keys is important for consensus!
    return sha256(r_text.encode('utf-8')).digest()


def sort_dicts_recursive(input):
    if isinstance(input, dict):
        result = {}
        for k, v in sorted(input.items()):
            if isinstance(v, dict):
                result[k] = sort_dicts_recursive(v)
            else:
                result[k] = v
        return result
    elif isinstance(input, (tuple, list)):
        return [sort_dicts_recursive(item) for item in input]
    else:
        return input


def consensus_response(responses, consensus_n, total_n, post_processor=None):
    if not responses:
        return None, 0.0

    hash_dict = {i: hash_response(r, post_processor) for i, r in enumerate(responses) if r is not None}
    counter = Counter(hash_dict.values())
    if not counter:
        return None, 0.0

    most_hash, most_freq = counter.most_common(1)[0]
    if most_freq >= consensus_n:
        best_index = next(i for i, this_hash in hash_dict.items() if this_hash == most_hash)
        return responses[best_index], (most_freq / total_n if total_n else 0.0)
    else:
        return None, 0.0


def first_not_null(responses):
    for r in responses:
        if r:
            return r
