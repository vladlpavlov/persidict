""" Persistent dictionaries that store key-value pairs on local disks or AWS S3.

The module offers 3 main classes:

PersiDict: base class in the hierarchy, defines unified interface
of all persistent dictionaries.

FileDirDict (inherited from PersiDict) : a dictionary that
stores key-value pairs as files on a local hard-drive.
A key is used to compose a filename, while a value is stored
as a pickle or a json object in the file.

S3_Dict (inherited from PersiDict): a dictionary that
stores key-value pairs on AWS S3.
A key is used to compose an objectname, while a value is stored
as a pickle or a json S3 object.
"""

from .persi_dict import PersiDict, PersiDictKey
from .file_dir_dict import FileDirDict