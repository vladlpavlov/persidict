# persidict

Simple persistent dictionaries for Python.

## What Is It?

`persidict` offers a simple persistent key-value store for Python. 
It saves the content of the dictionary in a folder on a disk 
or in an S3 bucket on AWS. Each value is stored as a separate file / S3 object.
Only text strings, or sequences of strings, are allowed as keys.

Unlike other Python persistent dictionaries (e.g. Python's native `shelve`), 
`persidict` is suitable for work in highly **distributed environments**, 
where multiple instances of a program run in parallel on 
a large number of different machines.

## Usage
Class 'FileDirDict' is a persistent dictionary that stores its content 
in a folder on a disk.

    from persidict import FileDirDict    
    my_dictionary = FileDirDict(dir_name="my_folder")

Once created, it can be used as a regular Python dictionary:

    my_dictionary["Eliza"] = "MIT Eliza was a mock Rogerian psychotherapist."
    my_dictionary["Eliza","year"] = 1965
    my_dictionary["Eliza","authors"] = ["Joseph Weizenbaum"
        ,"George Bernard Shaw"]
    
    my_dictionary["Shoebox"] = ("IBM Shoebox performed arithmetic on voice command.")
    my_dictionary["Shoebox", "year"] = 1961
    my_dictionary["Shoebox", "authors"] = ["W.C. Dersch", "E.A. Quade"]

    for k in my_dictionary:
        print(list(k), "==",  my_dictionary[k])

    assert "Eliza" in my_dictionary, "Something is wrong"

If you run the code above, it will produce the following output:

    >>> ['Eliza'] == MIT Eliza was a mock Rogerian psychotherapist.
    >>> ['Shoebox'] == IBM Shoebox performed arithmetic on voice command.
    >>> ['Shoebox', 'authors'] == ['W.C. Dersch', 'E.A. Quade']
    >>> ['Shoebox', 'year'] == 1961
    >>> ['Eliza', 'authors'] == ['Joseph Weizenbaum', 'George Bernard Shaw']
    >>> ['Eliza', 'year'] == 1965


Persistent dictionaries only accept sequences 
of URL/filename-safe non-empty strings as keys. 
Any pickleable Python object can be used as a value. 
Unlike regular Python dictionaries, insertion order is not preserved.

    del my_dictionary
    new_dict = FileDirDict(dir_name= "my_folder")
    print("len(new_dict) == ",len(new_dict))

The code above will print 

    >>> len(new_dict) == 6

because the data was stored on a disk.

Technically, FileDirDict saves its content in a folder on a local disk. 
But you can share this folder with other machines 
(for example, using Dropbox or NFS), and work with the same dictionary 
on multiple machines (from multiple instances of your program) simultaneously. 
This approach would allow you to use a persistent dictionary in 
a system that is distributed over dozens, even hundreds of computers.

If you anticipate to run your program on thousands (or more) computers, 
class 'S3Dict' is a better choice: it's a persistent dictionary that 
stores its content in an AWS S3 bucket.

    from persidict import S3Dict
    my_cloud_dictionary = S3Dict(bucket_name="my_bucket")

Once created, it can be used as a regular Python dictionary.

## Key Classes

* `SafeStrTuple` - an immutable sequence of URL/filename-safe non-empty strings.
* `PersiDict` - an abstract base class for persistent dictionaries. 
* `FileDirDict` - a persistent dictionary that stores its content 
in a folder on a disk.
* `S3Dict` - a persistent dictionary that stores its content 
in an AWS S3 bucket.

## Key Similarities With Python Built-in Dictionaries

`PersiDict` and its subclasses can be used as regular Python dictionaries. 

* You can use square brackets to get, set, or delete values. 
* You can iterate over keys, values, or items. 
* You can check if a key is in the dictionary. 
* You can check whether two dicts are equal 
(meaning they contain the same key-value pairs).
* You can get the length of the dictionary.
* Methods `keys()`, `values()`, `items()`, `get()`, `clear()`
, `clear()`, `setdefault()`, `update()` etc. work as expected.

## Key Differences From Python Built-in Dictionaries

`PersiDict` and its subclasses persist values between program executions, 
as well as allow simultaneously run programs to work with the same instance 
of a dictionary.

* Insertion order is not preserved
* Keys must be sequences of URL/filename-safe non-empty strings
* Values must be pickleable Python objects
* Methods `quiet_delete()`, `mtimestamp()`, `get_subdict()` and `subdicts()` 
are available
* You can not assign initial key-value pairs to a dictionary in its constructor

## How To Get It?

The source code is hosted on GitHub at:
[https://github.com/vladlpavlov/persidict](https://github.com/vladlpavlov/persidict) 

Binary installers for the latest released version are available at the Python package index at:
[https://pypi.org/project/persidict](https://pypi.org/project/persidict)

        pip install persidict

## Dependencies

* [jsonpickle](https://jsonpickle.github.io)
* [pandas](https://pandas.pydata.org)
* [numpy](https://numpy.org)
* [boto3](https://boto3.readthedocs.io)
* [pytest](https://pytest.org)
* [moto](http://getmoto.org)

## Key Contacts

* [Vlad (Volodymyr) Pavlov](https://www.linkedin.com/in/vlpavlov/) - Initial work