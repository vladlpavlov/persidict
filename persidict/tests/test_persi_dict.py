import inspect
import random

import pytest
from moto import mock_s3

from persidict import FileDirDict, S3Dict, SafeStrTuple
import pandas as pd


mutable_tests = [

(FileDirDict, dict(file_type="pkl", digest_len=11))
,(FileDirDict, dict(file_type="json", digest_len=11))
,(S3Dict, dict(file_type="pkl", bucket_name="my_bucket", digest_len=11))
,(S3Dict, dict(file_type="json", bucket_name="his_bucket", digest_len=11))

,(FileDirDict, dict(file_type="pkl", digest_len=5))
,(FileDirDict, dict(file_type="json", digest_len=5))
,(S3Dict, dict(file_type="pkl", bucket_name="my_bucket", digest_len=5))
,(S3Dict, dict(file_type="json", bucket_name="his_bucket", digest_len=5))

,(FileDirDict, dict(file_type="pkl", digest_len=0))
,(FileDirDict, dict(file_type="json", digest_len=0))
,(S3Dict, dict(file_type="pkl", bucket_name="my_bucket", digest_len=0))
,(S3Dict, dict(file_type="json", bucket_name="his_bucket", digest_len=0))

,(FileDirDict, dict(file_type="pkl"))
,(FileDirDict, dict(file_type="json"))
,(S3Dict, dict(file_type="pkl", bucket_name="her_bucket"))
,(S3Dict, dict(file_type="json", bucket_name="their_bucket"))

,(S3Dict, dict(file_type="pkl", bucket_name="a_bucket", root_prefix = "_"))
,(S3Dict, dict(file_type="json", bucket_name="the_bucket", root_prefix = "OYO"))

]

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_case_sensitivity(tmpdir, DictToTest, kwargs):

    if "digest_len" in kwargs and kwargs["digest_len"] <=3:
        return

    dict_to_test = DictToTest(dir_name = tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()

    for s in ["aaAA", "AAaa", "AAAA", "aaaa", "aAaA", "aAaa"]:
        dict_to_test[s] = s + s
        model_dict[s] = s + s
        assert len(dict_to_test) == len(model_dict)
        assert dict_to_test[s] == model_dict[s]

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_basics(tmpdir, DictToTest, kwargs):
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()
    assert len(dict_to_test) == len(model_dict) == 0

    all_keys = [("test",f"key_{i}","Q") for i in range(10)]

    for i,k in enumerate(all_keys):
        dict_to_test[k] = i
        dict_to_test[k] = i
        model_dict[k] = i
        assert len(dict_to_test) == len(model_dict)
        dict_to_test[k] = i+1
        model_dict[k] = i+1
        assert dict_to_test[k] == model_dict[k]

    for i,k in enumerate(all_keys):
        fake_k = f"fake_key_{i}"
        assert k in dict_to_test
        assert fake_k not in dict_to_test
        del dict_to_test[k]
        del model_dict[k]
        assert len(dict_to_test) == len(model_dict)
        assert k not in dict_to_test

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_iterators(tmpdir, DictToTest, kwargs):
    """Test if iterators work correctly."""
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()
    assert len(dict_to_test) == len(model_dict) == 0

    for i in range(25):
        k = f"key_{i*i}"
        dict_to_test[k] = 2*i
        model_dict[k] = 2*i

    assert (len(model_dict)
            == len(list(dict_to_test.keys()))
            == len(list(dict_to_test.values()))
            == len(list(dict_to_test.items())))

    assert sorted([str(k[0]) for k in dict_to_test.keys()]) == sorted(
        [str(k) for k in model_dict.keys()]) ##?!?!?!?!?!?!?
    assert sorted([str(v) for v in dict_to_test.values()]) == sorted(
        [str(v) for v in model_dict.values()])

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_complex_keys(tmpdir, DictToTest, kwargs):
    """Test if compound keys work correctly."""
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()

    for k in [("a", "a_1"), ("a", "a_2"), ("b", "b_1", "b_2", "b_3")]:
        dict_to_test[k] = 2*str(k)
        model_dict[k] = 2*str(k)
        assert len(dict_to_test) == len(model_dict)
        assert dict_to_test[k] == model_dict[k]

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_subdicts(tmpdir, DictToTest, kwargs):
    """Test if get_subdict() works correctly."""
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()

    fdd = dict_to_test
    fdd[("a", "a_1")] = 10
    fdd[("a", "a_2")] = 100
    fdd[("b", "b_1")] = 1000
    assert len(fdd.get_subdict("a")) == 2
    assert len(fdd.get_subdict("b")) == 1
    assert len(fdd.get_subdict("f")) == 0
    assert len(fdd.get_subdict(("i","j","k"))) == 0
    sbscts = fdd.subdicts()
    assert len(sbscts) == 2

    fdd[("b", "b_2")] = 10000
    fdd[("b", "b_3")] = 100000
    fdd[("c", "c_1")] = None
    assert len(fdd.get_subdict("a")) == 2
    assert len(fdd.get_subdict("b")) == 3
    assert len(fdd.get_subdict("c")) == 1
    sbscts = fdd.subdicts()
    assert len(sbscts) == 3

    print(f"{fdd.__dict__}")

    fdd.clear()
    assert len(fdd.get_subdict("a")) == 0
    assert len(fdd.get_subdict("b")) == 0


@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_work_with_basic_datatypes(tmpdir, DictToTest, kwargs):
    sample_data = [ [1,2,3,4,5]
                    ,["a","b","c","d","e"]
                    ,[i*i/3.14 for i in range(55)]
                    ,[str(i)*i for i in range(33)]
                    ,(1,2,3,4,5)
                    ,{"a":1,"b":2,"c":3,"d":4,"e":5}
                    ,{1,2,3,4,5}
                    ,True
                    ,(1,2,3,4,5,(6,7,8,9,10,(11,12,13,14,15)))
                    ]
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()
    for i,d in enumerate(sample_data):
        dict_to_test[str(i)] = d
        model_dict[str(i)] = d
        assert len(dict_to_test) == len(model_dict)
        assert dict_to_test[str(i)] == model_dict[str(i)]

    assert dict_to_test == model_dict

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_work_with_pandas(tmpdir, DictToTest, kwargs):
    """Validate how dict_to_test works with various pandas data types."""
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()

    dict_to_test["z"] = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    model_dict["z"] = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    assert (dict_to_test["z"] == model_dict["z"]).sum().sum() == 5

    dict_to_test["zz"] = pd.Series([1, 2, 3, 4, 5, 6])
    model_dict["zz"] = pd.Series([1, 2, 3, 4, 5, 6])
    assert (dict_to_test["zz"] == model_dict["zz"]).sum() == 6

    dict_to_test["zzz"] = pd.Index([1, 2, 3, 4])
    model_dict["zzz"] = pd.Index([1, 2, 3, 4])
    assert (dict_to_test["zzz"] == model_dict["zzz"]).sum() == 4

    dict_to_test["zzzz"] = pd.RangeIndex(0, 15)
    model_dict["zzzz"] = pd.RangeIndex(0, 15)
    assert (dict_to_test["zzzz"] == model_dict["zzzz"]).sum() == 15

    #TODO: add MultiIndex tests

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_more_dict_methods(tmpdir, DictToTest, kwargs):
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()
    model_dict = dict()

    for i in range(10):
        k = ("_"+str(10*i),)
        k = SafeStrTuple(k)
        dict_to_test[k] = i + 1
        model_dict[k] = i + 1

        k = (i + 1) * (str(i) + "zz",)
        k = SafeStrTuple(k)
        fake_k = (i + 1) * (str(i) + "aa",)
        fake_k = SafeStrTuple(fake_k)
        dict_to_test[k] = "hihi"
        model_dict[k] = "hihi"

        assert k in dict_to_test
        assert fake_k not in dict_to_test
        assert SafeStrTuple(k+"UUUU") not in dict_to_test

        new_key = ("new_key", str(i))
        new_key = SafeStrTuple(new_key)

        assert (dict_to_test.setdefault(new_key, 1) ==
                model_dict.setdefault(new_key, 1))

        assert (dict_to_test.setdefault(new_key, 2) ==
                model_dict.setdefault(new_key, 2))

        assert (dict_to_test.pop(new_key, 2) ==
                model_dict.pop(new_key, 2))

    assert dict_to_test == dict_to_test
    assert dict_to_test == model_dict

    for v in model_dict:
        assert v in dict_to_test

    dict_to_test.clear()

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_delete_if_exists(tmpdir, DictToTest, kwargs, rundom=None):
    dict_to_test = DictToTest(dir_name=tmpdir, **kwargs)
    dict_to_test.clear()

    good_keys = []
    bad_keys = []

    for i in range(1,12):
        good_k = ("good",)*i
        bad_k = ("bad",)*i
        good_keys.append(good_k)
        bad_keys.append(bad_k)
        dict_to_test[good_k] = i


    num_successful_deletions = 0
    all_keys = good_keys + bad_keys
    random.shuffle(all_keys)
    for k in all_keys:
        num_successful_deletions += dict_to_test.delete_if_exists(k)

    assert num_successful_deletions == len(good_keys)
    dict_to_test.clear()


@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_random_keys(tmpdir, DictToTest, kwargs):
    dict_to_test = DictToTest(dir_name = tmpdir, **kwargs)
    for n in range(10):
        dict_to_test[str(n)] = n**2
        dict_len = len(dict_to_test)
        for i in range(dict_len+1):
            assert len(dict_to_test.random_keys(max_n=i)) == i
        for i in range(dict_len+1, 10):
            assert len(dict_to_test.random_keys(max_n=i)) == dict_len

    for q in range(1,6):
        all_keys = set()
        for n in range(50):
            single_random_key = dict_to_test.random_keys(max_n=q)[0]
            all_keys |= {single_random_key}
        assert len(all_keys) >= 7


def demo_function(a:int=0, b:str="", c:float=0.0, d:bool=False):
    for element in [a,b,c,d]:
        print(element)
    return str(a)+str(b)+str(c)+str(d)

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_s3
def test_work_with_python_src(tmpdir, DictToTest, kwargs):
    """Validate how dict_to_test works with Python source code."""
    new_kwargs = dict(**kwargs)
    new_kwargs |= dict(dir_name=tmpdir, file_type = "py"
                       , base_class_for_values = str)

    dict_to_test = DictToTest(**new_kwargs)
    dict_to_test.clear()
    model_dict = dict()

    src = inspect.getsource(demo_function)
    print(f"{type(src)=}")
    dict_to_test["my_function"] = src
    assert dict_to_test["my_function"] == src

    dict_to_test.clear()

