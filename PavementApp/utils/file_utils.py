import fnmatch
import os

def delete_pattern(path, pattern):
    """ Deletes a set of files at a directory matching a pattern

    Args:
        string path: the path to the directory to iterate over
        string pattern: the pattern to match files against. We use the fnmatch
            pattern-set of 
            *	matches everything
            ?	matches any single character
            [seq]	matches any character in seq
            [!seq]	matches any character not in seq

    Returns:
        Nothing

    Raises:
        none
    """
    # Find all the files in the path given
    for root, _, files in os.walk(path):
        # Find the files that matches the given patterm
        for filename in fnmatch.filter(files, pattern):
            try:
                os.remove(os.path.join(root, filename))
            except (...):
                pass # If there was no file, silently fail. 
                