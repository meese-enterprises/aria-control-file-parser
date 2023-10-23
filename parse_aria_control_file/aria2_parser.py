#!/usr/bin/env python
import argparse
import os
import glob
import textwrap
"""
Usage:

Windows: python aria2_parser.py [path]|[-r --recursive]
Bash:    python3 aria2_parser.py [path]|[-r --recursive]
Example: python aria2_parser.py ./
"""

def main():
  file_parser(parse_aria_control_file)


def indentedPrint(string, indent=1):
  indentation = "  " * indent
  if args.unwrapped:
    print(indentation + string)
  else:
    new_text = textwrap.fill(string, initial_indent=indentation, subsequent_indent=indentation, width=80)
    print(new_text)


# Source: https://stackoverflow.com/a/71309268/6456163
def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)


def file_parser(handler_func):
  # Source: https://gist.github.com/89465127/5273149
  parser = argparse.ArgumentParser(
    description="Read in a file or set of files, and return the result.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument("path", nargs="+", help="Path of a singular file or a directory to search.")
  parser.add_argument("-e", "--extension", default=".aria2", help="File extension to filter by.")
  parser.add_argument("-r", "--recursive", action="store_true", default=False, help="Search through subfolders")
  parser.add_argument("-m", "--magnet", action="store_true", default=False, help="Print out the magnet link (for torrent files).")
  parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Print out ALL the information, including the long fields.")
  parser.add_argument("-u", "--unwrapped", action="store_true", default=False, help="Print out the information without wrapping the text (useful for copying).")
  
  # Allow access to args from anywhere
  global args
  args = parser.parse_args()

  # Parse paths
  full_paths = [os.path.join(os.getcwd(), path) for path in args.path]
  files = set()
  for path in full_paths:
    if os.path.isfile(path):
      _fileName, fileExt = os.path.splitext(path)
      if args.extension == "" or args.extension == fileExt:
        files.add(path)
    else:
      if (args.recursive):
        full_paths += glob.glob(path + "/*")
      else:
        files |= set(glob.glob(path + "/*" + args.extension))

  for i, f in enumerate(files):
    print(f"File name: {os.path.basename(f)}")
    handler_func(f)
    if i != len(files) - 1:
      # Print a line between files
      print("-" * 80)


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
def parse_aria_control_file(file_name):
  global args
  try:
    with open(file_name, "rb") as f:
      # Go to beginning, read VER
      f.seek(0)
      version_binary = f.read(2)
      version = int.from_bytes(version_binary, "big")
      indentedPrint(f"Version: {version}")

      # Read EXT
      f.seek(2)
      ext = f.read(4)
      indentedPrint(f"Ext: {ext}")

      # Find INFO HASH LENGTH
      f.seek(6)
      hash_length_binary = f.read(4)
      hash_length = int.from_bytes(hash_length_binary, "big")
      indentedPrint(f"Hash length: {hash_length}")

      # Read INFO HASH
      f.seek(10)
      info_hash_binary = f.read(hash_length)
      info_hash = info_hash_binary.hex().upper()
      indentedPrint(f"Info hash: {info_hash}")

      # Generate magnet link to torrent file
      if args.magnet:
        magnet_link = "magnet:?xt=urn:btih:" + info_hash
        hyperlink = link(f"https://btdig.com/{info_hash}", magnet_link)
        if args.unwrapped:
          indentedPrint(f"Magnet link: {hyperlink}")
        else:
          # TODO: Clean this up, the underline still wraps and prints
          indentedPrint("Magnet link:")
          indentedPrint(hyperlink, 2)

      # Read PIECE LENGTH
      f.seek(10 + hash_length)
      piece_length_binary = f.read(4)
      piece_length = int.from_bytes(piece_length_binary, "big")
      indentedPrint(f"Piece length: {piece_length} bytes")

      # Read TOTAL LENGTH
      f.seek(14 + hash_length)
      total_length_binary = f.read(8)
      total_length = int.from_bytes(total_length_binary, "big")
      indentedPrint(f"Total length: {total_length} bytes")

      # Read UPLOAD LENGTH
      f.seek(22 + hash_length)
      upload_length_binary = f.read(8)
      upload_length = int.from_bytes(upload_length_binary, "big")
      indentedPrint(f"Upload length: {upload_length} bytes")

      # Read BITFIELD LENGTH
      f.seek(30 + hash_length)
      bitfield_length_binary = f.read(4)
      bitfield_length = int.from_bytes(bitfield_length_binary, "big")
      indentedPrint(f"Bitfield length: {bitfield_length} bytes")

      # Read BITFIELD
      f.seek(34 + hash_length)
      bitfield_binary = f.read(bitfield_length)
      bitfield = bitfield_binary.hex().upper()
      if args.verbose:
        indentedPrint(f"Bitfield: {bitfield}")

      # Read NUM IN-FLIGHT PIECE
      f.seek(34 + hash_length + bitfield_length)
      num_inflight_piece_binary = f.read(4)
      num_inflight_piece = int.from_bytes(num_inflight_piece_binary, "big")
      indentedPrint(f"Number of in-flight pieces: {num_inflight_piece}")

      # Read INDEX, LENGTH, PIECE BITFIELD LENGTH, PIECE BITFIELD for each in-flight piece
      if args.verbose:
        for i in range(num_inflight_piece):
          indentedPrint(f"Piece {i + 1}:", 2)

          # Read INDEX
          f.seek(38 + hash_length + bitfield_length + i * 8)
          index_binary = f.read(4)
          index = int.from_bytes(index_binary, "big")
          indentedPrint(f"Index: {index}", 3)

          # Read LENGTH
          f.seek(42 + hash_length + bitfield_length + i * 8)
          length_binary = f.read(4)
          length = int.from_bytes(length_binary, "big")
          indentedPrint(f"Length: {length}", 3)

          # Read PIECE BITFIELD LENGTH
          f.seek(46 + hash_length + bitfield_length + i * 8)
          piece_bitfield_length_binary = f.read(4)
          piece_bitfield_length = int.from_bytes(piece_bitfield_length_binary, "big")
          indentedPrint(f"Piece bitfield length: {piece_bitfield_length}", 3)

          # Read PIECE BITFIELD
          f.seek(50 + hash_length + bitfield_length + i * 8)
          piece_bitfield_binary = f.read(piece_bitfield_length)
          piece_bitfield = piece_bitfield_binary.hex().upper()
          # Each one is a 16KiB chunk
          indentedPrint(f"Piece bitfield: {piece_bitfield}", 3)

  except FileNotFoundError:
    indentedPrint(f"File not found: {file_name}")


if __name__ == "__main__":
  main()
