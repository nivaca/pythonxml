# pythonxml

## Synopsis
Python3 scripts to diff TEI-XML files

## Requirements
* Python 3.6+
* google-diff-match-patch Python 3 module (https://bitbucket.org/cowwoc/google-diff-match-patch/src)
* pyprind module (https://github.com/rasbt/pyprind) [Optional. This is module to display nice progress bars. If not found, the scripts will display a warning but continue running without problems.]

## Detailed Description
This script parses all the TEI-XML files in the `/data` directory, and compares them using the `diff-match-patch` algorithm by Google. The script can then return an output text file (`output.txt`) and/or html-prettified file (`output.html`) containing the diff of the files.

The source TEI-XML files have to be encoded following the *LombardPress Diplomatic Transcription Guidelines*. (See https://github.com/lombardpress/lombardpress-schema/blob/develop/docs/1.0/diplomatic/index.md) This makes sure, amongst other things, that all witnesses being compared have the same structure (same number of `<p>` elements, same `@xml:id`s for the `<p>`s, etc.).

## Installation
Clone the GitHub repository. Put your source TEI-XML files in the `\data` directory. (This can be changed in the global variable `directory` in the `collator.py` file.) Make sure all module requirements have been fulfilled. 

The `diff-match-patch` module can be installed in the following way (Linux or MacOS):

```sh
pip install diff-match-patch
```

### Why Python 3.6+?
Python 3.6 introduces a nice way of managing formatted string literals. See [PEP 498](https://www.python.org/dev/peps/pep-0498/). Our scripts make use of that new feature. 

If the user wishes use a previous version of Python 3 (not Python 2!), he/she may simply change the formatted string literals. For example:

```python
message = f'\nChecking {file_num} files...'
```

should be changed to:

```python
message = '\nChecking %d files...' %file_num 
```


## Tests
To test the scripts, simply run `python3 collator.py` inside the downloaded directory structure.

## Contributors
Nicolas Vaughan (n.vaughan [at] uniandes.edu.co).

Universidad de los Andes, Bogotá, Colombia.

## License
Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) 
http://creativecommons.org/licenses/by-nc/3.0/
