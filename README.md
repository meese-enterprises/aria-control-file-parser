# aria-control-file-parser

[![PyPI](https://img.shields.io/pypi/v/parse_aria_control_file.svg)](https://pypi.org/project/parse_aria_control_file/)

> Parse `aria2c` control files from the command line.

The _.aria2_ (Control File) contains the hash info of the magnet link, so we can parse the file to get the original magnet link. This allows you to resume the download where it left off if it was cancelled or interrupted.

See [this issue](https://github.com/aria2/aria2/issues/792).

```log
# ================================================================
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +---+-------+-------+-------------------------------------------+
# |VER|  EXT  |INFO   |INFO HASH ...                              |
# |(2)|  (4)  |HASH   | (INFO HASH LENGTH)                        |
# |   |       |LENGTH |                                           |
# |   |       |  (4)  |                                           |
# +---+---+---+-------+---+---------------+-------+---------------+
# |PIECE  |TOTAL LENGTH   |UPLOAD LENGTH  |BIT-   |BITFIELD ...   |
# |LENGTH |     (8)       |     (8)       |FIELD  | (BITFIELD     |
# |  (4)  |               |               |LENGTH |  LENGTH)      |
# |       |               |               |  (4)  |               |
# +-------+-------+-------+-------+-------+-------+---------------+
# |NUM    |INDEX  |LENGTH |PIECE  |PIECE BITFIELD ...             |
# |IN-    |  (4)  |  (4)  |BIT-   | (PIECE BITFIELD LENGTH)       |
# |FLIGHT |       |       |FIELD  |                               |
# |PIECE  |       |       |LENGTH |                               |
# |  (4)  |       |       |  (4)  |                               |
# +-------+-------+-------+-------+-------------------------------+
#
#         ^                                                       ^
#         |                                                       |
#         +-------------------------------------------------------+
#                 Repeated in (NUM IN-FLIGHT) PIECE times

# More information available at:
# https://aria2.github.io/manual/en/html/technical-notes.html
# ================================================================
```

## How to Use

```shell
python3 aria2_parser.py dahufa.aria2
```

With multiple files or with a directory:

```shell
python3 aria2_parser.py dahufa.aria2 dahufa.aria2 ./folder
```

Reading _aria2_ files from folder recursively:

```shell
python3 aria2_parser.py ./ -r
```

## Build

```shell
python3 setup.py build
python3 setup.py install
```
