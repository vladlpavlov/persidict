from persidict.tests.test_persi_dict import *

def test_FileDirDict(tmpdir):
    p = FileDirDict(dir_name = tmpdir, file_type="pkl")
    validate_dict_object(p)

    p1 = FileDirDict(dir_name=tmpdir, file_type="pkl")
    validate_dict_object(p1)

    j = FileDirDict(dir_name = tmpdir, file_type="json")
    validate_dict_object(j)