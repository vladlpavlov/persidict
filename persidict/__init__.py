""" Persistent dictionaries that store key-value pairs on local disks or AWS S3.

The package offers a few classes:

PersiDict: base class in the hierarchy, defines unified interface
for all persistent dictionaries.

SafeStrTuple: a flat tuple of URL/filename-safe strings
that can be used as a key for PersiDict objects

FileDirDict (inherited from PersiDict) : a dictionary that
stores key-value pairs as files on a local hard-drive.
A key is used to compose a filename, while a value is stored
as a pickle or a json object in the file.

S3_Dict (inherited from PersiDict): a dictionary that
stores key-value pairs as S3 objects on AWS.
A key is used to compose an objectname, while a value is stored
as a pickle or a json S3 object.
"""

from .safe_str_tuple import SafeStrTuple, get_safe_chars
from .persi_dict import PersiDict
from .file_dir_dict import FileDirDict
from .s3_dict import S3Dict