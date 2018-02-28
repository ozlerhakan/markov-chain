''' This is a module to create markup chains.

The underlying data structure is:

>>> get_table('ab')
{'a': {'b': 1}}
>>> get_table('abcd')
{'a': {'b': 1}, 'b': {'c': 1}, 'c': {'d': 1}}

# m - instance
# Markov
>>> m = Markov('abcda')  # creating an instance of a class
>>> m.predict('a')
'b'
    >>> m.predict('z')
    Traceback (most recent call last):
      ...
    KeyError: 'z not in table'
'''
# std imports
import argparse
import random
import sys

# 3rd party imports
import requests

def write_http_contents(url, filename):
    r = requests.url(url)
    data = r.text
    with open(filename, mode='w', encoding='utf-8') as fout:
        fout.write(data)

def get_markov(filename, split=True, size=1, encoding='utf-8'):
    with open(filename, encoding=encoding) as fin:
        data = fin.read()
        clazz = Markov
        if not split:
            data = data.split()
            clazz = WordMarkov
        return clazz(data, size)

def test_predict(m, num_chars, start, sep=''):
    res = [start]
    size = len(m.tables)
    for i in range(num_chars):
        out = m.predict(start)
        res.append(out)
        start = sep.join(res[-size:])
    return sep.join(res)         
    
class Markov:
    """Markov is a class behaves as a factory"""
    
    def __init__(self, data, size=1):
        '''
        This is the constructor , it is called when
        the class creates a new instance.
        
        In python, everything is object!
        
        'self' is the 'instance'.
        >>> m = Markov('abcs', size=3)
        >>> m.tables
        {'a': {'b': 1}, 'b': {'c': 1}, 'c': {'s': 1}}, {'ab': {'c': 1}, 'bc': {'s': 1}}, {'abc': {'s': 1}}]

        >>> m = Markov('abcs', size=5)
        >>> m.tables
        {'a': {'b': 1}, 'b': {'c': 1}, 'c': {'s': 1}}, {'ab': {'c': 1}, 'bc': {'s': 1}}, {'abc': {'s': 1}}, {}, {}]
        5 dictionaries
        '''
        #self.table = get_table(data) # data is an attribute
        self.tables = []
        self.size = size
        for i in range(size):
            self.tables.append(get_table(data, i+1))

    def _get_table(self, data_in):
        return self.tables[len(data_in) - 1]
    
    def predict(self, data_in):
        '''This is a method on Markov

        let's say table is:
        >>> get_table('abcdabc')
        {'a': {'b': 2}, 'b': {'c': 2}, 'c': {'d': 1}, 'd': {'a': 1}}
        >>> table = get_table('abcdabc')
        >>> table.get('a', {})
        {'b': 2}
        >>> table.get('a').items()
	dict_items([('b', 2)])
        '''
        if self.size < len(data_in):
            raise IndexError(f'{data_in}\'s length exceeds the size {self.size}')
        
        # m.tables[len('ab')-1]
        # 'ab': {'c': 1}, 'bc': {'s': 1}}
        table = self._get_table(data_in)
        # m.tables[len('ab')-1].get('ab',{})
        # {'c': 1}
        options = table.get(data_in, {})
        # options = {'b': 2}

        if not options:
            raise KeyError(f'{data_in} not in table')
        
        possibles = []
        for out , count in options.items():
            # out = b, count = 2
            possibles.extend([out] * count)
        result = random.choice(possibles)
        return result

class WordMarkov(Markov):
    def _get_table(self, data_in):
        idx = len(data_in.split()) - 1
        return self.tables[idx]

def main(args):
    """
    >>> python markov.py -h
    usage: markov.py [-h] [-f FILE] [-s SIZE] [--encoding ENCODING] [--word]

    Markov chain app

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  Input file
      -s SIZE, --size SIZE  Markov size
      --encoding ENCODING   Input encoding (default utf-8)
      --word                Create a Word Markov
    """
    parser = argparse.ArgumentParser(description='Markov chain app')

    parser.add_argument('-f', '--file', help='Input file')
    parser.add_argument('-s', '--size', help='Markov size', default=1, type=int)
    parser.add_argument('--encoding', help='Input encoding (default utf-8)',
                        default='utf-8')
    parser.add_argument('--word', action='store_true', default=False,
                        help='Create a Word Markov')
    opts = parser.parse_args(args)
    if opts.file:
        m = get_markov(opts.file, split=not opts.word,
                       size=opts.size, encoding=opts.encoding)
        repl(m)
    
def repl(m):
    while 1:
        txt = input('>')
        try:
            res = m.predict(txt)
        except KeyError:
            print(f'{txt} missing')
        except KeyboardInterrupt:
            print("Goodbye")
            break
        except EOFError:
            break
        else:
            print(res)
        
def get_table(line, size=1):
    '''This is a method
    >>> get_table('abcd')
    {'a': {'b': 1}, 'b': {'c': 1}, 'c': {'d': 1}}
    >>> get_table(['hadi', 'ama', 'hadi', 'neden'])
    {'hadi': {'ama': 1, 'neden': 1}, 'ama': {'hadi': 1}}
    >>> get_table('abcs', size=3)
    {'abc': {'s': 1}}
    >>> get_table(['abcs','skd','abcd','aaa'], size=3)
    {'abcs skd abcd': {'aaa': 1}}
    '''
    results = {}
    # obj = 'superdegilmiama' 
    # list(zip(obj, obj[1:]))
    # [('s', 'u'), ('u', 'p'), ('p', 'e'), ('e', 'r'), ('r', 'd'), ('d', 'e'), ('e', 'g'), ('g', 'i'), ('i', 'l'), ('l', 'm'), ('m', 'i'), ('i', 'a'), ('a', 'm'), ('m', 'a')]
    #for c, out in zip(line, line[1:]):
    for i, _ in enumerate(line):
        chars = line[i:i+size]
        try:
            out = line[i+size]
        except IndexError:
            break
        if isinstance(chars, list):
            # ' '.join(['a','b','c'])
            # 'a b c'
            chars = ' '.join(chars)
        char_dict = results.get(chars, {})
        char_dict.setdefault(out, 0)
        char_dict[out] += 1
        results[chars] = char_dict
    return results

def get_table_with_enumerate(line):
    '''This is a method using enumerate()
    '''
    results = {}
    for i,c in enumerate(line):
        try:
           out = line[i + 1]
        except IndexError:
           break
        char_dict = results.get(c, {})
        char_dict.setdefault(out, 0)
        char_dict[out] += 1
        results[c] = char_dict
    return results

def get_table_with_range(line):
    '''This is a method using range()
    '''
    results = {}
    for i in range(len(line)):
        c = line[i]
        try:
           out = line[i + 1]
        except IndexError:
           break
        char_dict = results.get(c, {})
        char_dict.setdefault(out, 0)
        char_dict[out] += 1
        results[c] = char_dict
    return results

if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    main(sys.argv[1:]) # do not include markov.py itself
