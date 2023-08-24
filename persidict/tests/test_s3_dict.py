from persidict.tests.test_persi_dict import *
from persidict import S3Dict
from moto import mock_s3

@mock_s3
def test_S3_Dict(tmpdir):
    d = S3Dict(bucket_name ="TEST",dir_name = tmpdir)
    validate_dict_object(d)

    d_j = S3Dict(bucket_name ="TEST", file_type="json",dir_name = tmpdir)
    validate_dict_object(d_j)

    d_p = S3Dict(bucket_name="TEST", file_type="pkl",dir_name = tmpdir)
    validate_dict_object(d_p)