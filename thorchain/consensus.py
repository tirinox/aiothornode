from collections import Counter
from hashlib import sha256


def text_response_hash(r):
    return sha256(r.encode('utf-8')).hexdigest()


def consensus_response(text_responses, consensus_n, total_n):
    hash_dict = {i: text_response_hash(r) for i, r in enumerate(text_responses) if r}
    counter = Counter(hash_dict.values())
    most_hash, most_freq = counter.most_common(1)[0]
    if most_freq >= consensus_n:
        best_index = next(i for i, this_hash in hash_dict.items() if this_hash == most_hash)
        return text_responses[best_index], (most_freq / total_n if total_n else 0.0)
    else:
        return None, 0.0
