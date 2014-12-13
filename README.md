# Basic session generator and 'concatenator'

Use this sofware to hash and concate automatically large files

## Session generator

```
python session_generator.py
usage: session_generator.py [-h] [-F FILE [FILE ...]] [-t TEXT [TEXT ...]]
                            [-T TIME [TIME ...]] [-d DURATION]
                            [-e ENCODING [ENCODING ...]] [-cf]
                            [-s DESTINATION] [--version]

Basic session generator

optional arguments:
  -h, --help            show this help message and exit
  -F FILE [FILE ...]    File(s) to encode.
  -t TEXT [TEXT ...]    Text(s) to encode
  -T TIME [TIME ...]    Time(s) to encode, format -> d/m/y h:min:s Or type
                        'current' to use the current time
  -d DURATION           Duration after the start time in minutes.
  -e ENCODING [ENCODING ...]
                        Enconding wished. Currently support : 'base64', 'md5',
                        'sha1', 'sha224', 'sha256', 'sha384', 'sha512'. Type
                        'all' to use them all this order. By default : None
  -cf                   The output will be cookie friendly.
  -s DESTINATION        File to save the output
  --version             show program's version number and exit
```
  
### Examples

```
python session_generator.py -t paul -e all

cGF1bA==
6c63212ab48e8401eaf6b59b95d816a9
a027184a55211cd23e3f3094f1fdc728df5e0500
ab16de0656382d91838914109ab89a0a4e04321550a1a20ace7a8b66
0357513deb903a056e74a7e475247fc1ffe31d8be4c1d4a31f58dd47ae484100
d36b920f6497109f764c45ec52720b588b6b478a7705d91895087c53e4ee2466b223d1ade57d15c47adb5482ab59125f
23277b9f367aa558b865028f4e8be799561ca52d157b55f93713adecc1529d7cf8ce29b024888cb04217620b1dd933d6510ead16dda1a44bba5bbc220316dca0
```

```
python session_generator.py -T current -e base64 -cf

MTQxODQ5Mzc1Mg
```

```
python session_generator.py -T current -d 1 -e md5

11fd6a6ce69176bc15a6320290425e5f
130bbebed68d78c79d40578e467f943c
6785a008470af09afcba9ee518567bab
64c7d91a5ff136a31844859cb5515726
fd45f740d9d1be38d003781abf4bc53d
...
```

## Concatenation program

```
python concatenator.py         
usage: concatenator.py [-h] [-F SOURCE [SOURCE ...]] [-t TEXT [TEXT ...]]
                       [-o ORDER [ORDER ...]] [-s DESTINATION] [--version]

Basic concatenation program

optional arguments:
  -h, --help            show this help message and exit
  -F SOURCE [SOURCE ...]
                        File(s) to concatenate.
  -t TEXT [TEXT ...]    Text(s) to concatenate.
  -o ORDER [ORDER ...]  Set the order. Type 'text' and 'file' in the order you
                        want. By default the texts is after the files.
  -s DESTINATION        File to save the output.
  --version             show program's version number and exit
```
  
### Examples

```
python concatenator.py -t test1 test2

test1test2
```

```
ython concatenator.py -F test -t string1 string2 -o text file text

string11astring2
string11bstring2
string11cstring2
string11dstring2
```
With file 'test' :
```
1a
1b
1c
1d
```



## License

This source code is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
