from collections import Counter
from hashlib import sha256
import ujson


def hash_response(r):
    r_text = ujson.dumps(r, sort_keys=True)  # sorted keys is important for consensus!
    return sha256(r_text.encode('utf-8')).digest()


def consensus_response(responses, consensus_n, total_n):
    if not responses:
        return None, 0.0

    hash_dict = {i: hash_response(r) for i, r in enumerate(responses) if r}
    counter = Counter(hash_dict.values())
    most_hash, most_freq = counter.most_common(1)[0]
    if most_freq >= consensus_n:
        best_index = next(i for i, this_hash in hash_dict.items() if this_hash == most_hash)
        return responses[best_index], (most_freq / total_n if total_n else 0.0)
    else:
        return None, 0.0
