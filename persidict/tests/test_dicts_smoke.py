# from pythagoras.persistent_dicts import FileDirDict, S3_Dict
from persidict import FileDirDict
# from persidict import S3_Dict
import pandas as pd
# from moto import mock_s3

def validate_dict_object(dict_to_test):
    dict_to_test.clear()
    model_dict = dict()

    a_key = dict_to_test._add_all_suffixes_if_absent(["Blah-Blah-Blah"])
    assert a_key == dict_to_test._add_all_suffixes_if_absent(a_key)

    assert len(dict_to_test) == len(model_dict) == 0

    for s in ["aaAA", "AAaa", "AAAA", "aaaa", "aAaA", "aAaa"]:
        dict_to_test[s] = s + s
        model_dict[s] = s + s
        assert len(dict_to_test) == len(model_dict)

    dict_to_test.clear()
    model_dict.clear()
    assert len(dict_to_test) == len(model_dict) == 0

    for i in range(10):
        k = ("_"+str(10*i),)
        dict_to_test[k] = i
        dict_to_test[k] = i
        dict_to_test[k] = i + 1
        dict_to_test[k] = i + 1
        model_dict[k] = i
        model_dict[k] = i + 1

        k = (i + 1) * (str(i) + "zz",)
        fake_k = (i + 1) * (str(i) + "aa",)
        dict_to_test[k] = "hihi"
        model_dict[k] = "hihi"

        assert k in dict_to_test
        assert fake_k not in dict_to_test
        assert k+("1",) not in dict_to_test


        new_key = ("new_key", str(i))
        assert (dict_to_test.setdefault(new_key, 1) ==
                model_dict.setdefault(("new_key", str(i)), 1))

        assert (dict_to_test.setdefault(new_key, 2) ==
                model_dict.setdefault(new_key, 2))

        assert (dict_to_test.pop(new_key, 2) ==
                model_dict.pop(new_key, 2))

    assert dict_to_test == dict_to_test
    assert dict_to_test == model_dict
    for v in model_dict:
        assert v in dict_to_test

    assert (len(dict_to_test)
            == len(list(dict_to_test.keys()))
            == len(list(dict_to_test.values()))
            == len(list(dict_to_test.items())))

    assert sorted([str(k) for k in dict_to_test.keys()]) == sorted([str(k) for k in model_dict.keys()])
    assert sorted([str(v) for v in dict_to_test.values()]) == sorted([str(v) for v in model_dict.values()])


    for j in range(len(dict_to_test)):
        dict_to_test.popitem()
        model_dict.popitem()

    assert len(dict_to_test) == 0

    dict_to_test["z"] = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    model_dict["z"] = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    assert (dict_to_test["z"] == model_dict["z"]).sum().sum() == 5

    dict_to_test.clear()
    model_dict.clear()

    assert len(dict_to_test) == 0

    dict_to_test.clear()
    fdd = dict_to_test
    fdd[("a", "a_1")] = 10
    fdd[("a", "a_2")] = 100
    fdd[("b", "b_1")] = 1000
    assert len(fdd.get_subdict("a")) == 2
    assert len(fdd.get_subdict("b")) == 1
    fdd.clear()
    assert len(fdd.get_subdict("a")) == 0


def test_FileDirDict(tmpdir):
    p = FileDirDict(dir_name = tmpdir, file_type="pkl")
    validate_dict_object(p)

    p1 = FileDirDict(dir_name=tmpdir, file_type="pkl")
    validate_dict_object(p1)

    j = FileDirDict(dir_name = tmpdir, file_type="json")
    validate_dict_object(j)

#
# @mock_s3
# def test_S3_Dict(tmpdir):
#     d = S3_Dict(bucket_name ="TEST",dir_name = tmpdir)
#     validate_dict_object(d)
#
#     d_j = S3_Dict(bucket_name ="TEST", file_type="json",dir_name = tmpdir)
#     validate_dict_object(d_j)
#
#     d_p = S3_Dict(bucket_name="TEST", file_type="pkl",dir_name = tmpdir)
#     validate_dict_object(d_p)


