import inspect
import random
from copy import deepcopy

import pytest
from moto import mock_aws

from persidict import FileDirDict, S3Dict, SafeStrTuple
import pandas as pd

from persidict.tests.data_for_mutable_tests import mutable_tests

@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_aws
def test_get_params(tmpdir, DictToTest, kwargs):
    """Test .get_params() method."""
    dict_to_test = DictToTest(base_dir=tmpdir, **kwargs)
    dict_to_test.clear()
    model_params = DictToTest.get_default_params()
    model_params.update(kwargs)
    model_params["base_dir"] = str(tmpdir)

    if "root_prefix" in model_params:
        if isinstance(model_params["root_prefix"], str):
            if len(model_params["root_prefix"]) > 0:
                if model_params["root_prefix"][-1] != "/":
                    model_params["root_prefix"] += "/"

    params = dict_to_test.get_params()
    assert isinstance(params, dict)
    assert params == model_params


@pytest.mark.parametrize("DictToTest, kwargs", mutable_tests)
@mock_aws
def test_get_default_params(tmpdir, DictToTest, kwargs):
    # dict_to_test_1 = DictToTest(base_dir=tmpdir)
    # dict_to_test_2 = DictToTest(**{
    #     **DictToTest.get_default_params()
    #     ,**dict(base_dir=tmpdir)})
    # assert dict_to_test_1.get_params() == dict_to_test_2.get_params()


    dict_to_test_1 = DictToTest()
    dict_to_test_2 = DictToTest(**{
        **DictToTest.get_default_params()
        ,**dict()})
    assert dict_to_test_1.get_params() == dict_to_test_2.get_params()
