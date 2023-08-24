""" Persistent dictionaries that store key-value pairs on local disks.

This functionality is implemented by the class FileDirDict
(inherited from PersiDict): a dictionary that
stores key-value pairs as files on a local hard-drive.
A key is used to compose a filename, while a value is stored
as a pickle or a json object in the file.
"""
from __future__ import annotations

import os
import pickle
from typing import Any


import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
import jsonpickle.ext.pandas as jsonpickle_pandas

from .safe_str_tuple import SafeStrTuple
from .safe_str_tuple_signing import sign_safe_str_tuple, unsign_safe_str_tuple
from .persi_dict import PersiDict

jsonpickle_numpy.register_handlers()
jsonpickle_pandas.register_handlers()

class FileDirDict(PersiDict):
    """ A persistent Dict that stores key-value pairs in local files.

    A new file is created for each key-value pair.
    A key is either a filename (without an extension),
    or a sequence of directory names that ends with a filename.
    A value can be any Python object, which is stored in a file.
    Insertion order is not preserved.

    FileDirDict can store objects in binary files (as pickles)
    or in human-readable text files (using jsonpickles).
    """

    def __init__(self
                 , dir_name: str = "FileDirDict"
                 , file_type: str = "pkl"
                 , immutable_items:bool = False
                 , digest_len:int = 8):
        """A constructor defines location of the store and file format to use.

        dir_name is a directory that will contain all the files in
        the FileDirDict. If the directory does not exist, it will be created.

        file_type can take one of two values: "pkl" or "json".
        It defines which file format will be used by FileDirDict
        to store values.
        """

        super().__init__(immutable_items = immutable_items
                ,digetst_len = digest_len)

        self.file_type = file_type

        assert file_type in {"json", "pkl"}, (
            "file_type must be either pkl or json")
        assert not os.path.isfile(dir_name)
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        assert os.path.isdir(dir_name)

        self.base_dir = os.path.abspath(dir_name)

    def __repr__(self):
        """Return repr(self)."""

        repr_str = super().__repr__()
        repr_str = repr_str[:-1] + f", dir_name={self.base_dir}"
        repr_str += f", file_type={self.file_type}"
        repr_str += " )"

        return repr_str


    def __len__(self) -> int:
        """ Get number of key-value pairs in the dictionary."""

        num_files = 0
        for subdir_info in os.walk(self.base_dir):
            files = subdir_info[2]
            files = [f_name for f_name in files
                     if f_name.endswith(self.file_type)]
            num_files += len(files)
        return num_files

    def clear(self):
        """ Remove all elements from the dictionary."""

        assert not self.immutable_items, (
            "Can't clear a dict that contains immutable items")

        for subdir_info in os.walk(self.base_dir, topdown=False):
            (subdir_name, _, files) = subdir_info
            for f in files:
                if f.endswith(self.file_type):
                    os.remove(os.path.join(subdir_name, f))
            if (subdir_name != self.base_dir) and (
                    len(os.listdir(subdir_name)) == 0 ):
                os.rmdir(subdir_name)

    def _build_full_path(self
                         , key:SafeStrTuple
                         , create_subdirs:bool=False
                         , is_file_path:bool=True) -> str:
        """Convert a key into a filesystem path."""

        key = sign_safe_str_tuple(key, self.digest_len)
        key = [self.base_dir] + list(key.str_chain)
        dir_names = key[:-1] if is_file_path else key

        if create_subdirs:
            current_dir = dir_names[0]
            for dir_name in dir_names[1:]:
                new_dir = os.path.join(current_dir, dir_name)
                if not os.path.isdir(new_dir):
                    os.mkdir(new_dir)
                current_dir = new_dir

        if is_file_path:
            file_name = key[-1] + "." + self.file_type
            return os.path.join(*dir_names, file_name)
        else:
            return os.path.join(*dir_names)


    def get_subdict(self, key:SafeStrTuple):
        """Get a subdictionary containing items with the same prefix_key.

        This method is absent in the original dict API.
        """
        key = SafeStrTuple(key)
        full_dir_path = self._build_full_path(
            key, create_subdirs = True, is_file_path = False)
        return FileDirDict(
            dir_name = full_dir_path
            , file_type=self.file_type
            , immutable_items= self.immutable_items)

    def _read_from_file(self, file_name:str) -> Any:
        """Read a value from a file. """

        if self.file_type == "pkl":
            with open(file_name, 'rb') as f:
                result = pickle.load(f)
        elif self.file_type == "json":
            with open(file_name, 'r') as f:
                result = jsonpickle.loads(f.read())
        else:
            raise ValueError("file_type must be either pkl or json")
        return result

    def _save_to_file(self, file_name:str, value:Any) -> None:
        """Save a value to a file. """

        if self.file_type == "pkl":
            with open(file_name, 'wb') as f:
                pickle.dump(value, f)
        elif self.file_type == "json":
            with open(file_name, 'w') as f:
                f.write(jsonpickle.dumps(value, indent=4))
        else:
            raise ValueError("file_type must be either pkl or json")

    def __contains__(self, key:SafeStrTuple) -> bool:
        """True if the dictionary has the specified key, else False. """
        key = SafeStrTuple(key)
        filename = self._build_full_path(key)
        return os.path.isfile(filename)

    def __getitem__(self, key:SafeStrTuple) -> Any:
        """ Implementation for x[y] syntax. """
        key = SafeStrTuple(key)
        filename = self._build_full_path(key)
        if not os.path.isfile(filename):
            raise KeyError(f"File {filename} does not exist")
        result = self._read_from_file(filename)
        return result

    def __setitem__(self, key:SafeStrTuple, value:Any):
        """Set self[key] to value."""
        key = SafeStrTuple(key)
        filename = self._build_full_path(key, create_subdirs=True)
        if self.immutable_items:
            assert not os.path.exists(filename), (
                "Can't modify an immutable item")
        self._save_to_file(filename, value)

    def __delitem__(self, key:SafeStrTuple) -> None:
        """Delete self[key]."""
        key = SafeStrTuple(key)
        assert not self.immutable_items, "Can't delete immutable items"
        filename = self._build_full_path(key)
        if not os.path.isfile(filename):
            raise KeyError(f"File {filename} does not exist")
        os.remove(filename)

    def _generic_iter(self, iter_type: str):
        """Underlying implementation for .items()/.keys()/.values() iterators"""
        assert iter_type in {"keys", "values", "items"}
        walk_results = os.walk(self.base_dir)
        ext_len = len(self.file_type) + 1

        def splitter(dir_path: str):
            """Transform a dirname into a PersiDictKey key"""
            result = []
            if dir_path == ".":
                return result
            while True:
                head, tail = os.path.split(dir_path)
                result = [tail] + result
                dir_path = head
                if len(head) == 0:
                    break
            return tuple(result)

        def step():
            for dir_name, _, files in walk_results:
                for f in files:
                    if f.endswith(self.file_type):
                        prefix_key = os.path.relpath(
                            dir_name, start=self.base_dir)

                        result_key = (*splitter(prefix_key), f[:-ext_len])
                        result_key = SafeStrTuple(result_key)

                        if iter_type == "keys":
                            yield unsign_safe_str_tuple(
                                result_key, self.digest_len)
                        elif iter_type == "values":
                            yield self[result_key]
                        else:
                            yield (unsign_safe_str_tuple(
                                result_key, self.digest_len), self[result_key])

        return step()


    def mtimestamp(self, key:SafeStrTuple) -> float:
        """Get last modification time (in seconds, Unix epoch time).

        This method is absent in the original dict API.
        """
        filename = self._build_full_path(key)
        return os.path.getmtime(filename)