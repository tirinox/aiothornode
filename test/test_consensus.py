from aiothornode.consensus import sort_dicts_recursive


def test_sort_dicts_recursive_1():
    mixed_dict_1 = {
        "a": 1,
        "c": 3,
        "b": 2,
        "e": 5,
        "d": 4
    }
    sd1 = sort_dicts_recursive(mixed_dict_1)
    assert sd1 == {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
    }
    assert list(sd1.keys()) == ["a", "b", "c", "d", "e"]
    assert list(sd1.keys()) != ["a", "c", "b", "e", "d"]
    assert list(sd1.values()) == [1, 2, 3, 4, 5]
    assert list(sd1.values()) != [1, 3, 2, 5, 4]


def test_sort_dicts_recursive_2():
    mixed_dict_1 = {
        "a": 1,
        "c": 3,
        "b": {
            "zzz": 300,
            "yyy": 200,
            "xxx": 100,
        },
        "e": 5,
        "d": 4
    }
    sd1 = sort_dicts_recursive(mixed_dict_1)

    assert list(sd1.keys()) == ["a", "b", "c", "d", "e"]
    assert list(sd1.values()) == [1, {
            "zzz": 300,
            "yyy": 200,
            "xxx": 100,
        }, 3, 4, 5]

    assert list(sd1['b'].keys()) == ["xxx", "yyy", "zzz"]
    assert list(sd1['b'].keys()) != ["zzz", "yyy", "xxx"]
