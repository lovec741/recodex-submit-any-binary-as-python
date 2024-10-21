import argparse
import os
import base64
import zlib

parser = argparse.ArgumentParser(description="Convert compiled binary and source code to a Python script for Recodex submission.")
parser.add_argument("binary", help="Path to the compiled binary to be run")
parser.add_argument("src", help="Path to the source directory (should only include text files)")
parser.add_argument("output", nargs="?", default="./out.py", help="Path to the output script (default: ./out.py)")

args = parser.parse_args()

runner_code_text = """
import ctypes
import subprocess
import os
import base64
import zlib

decoded_data = base64.b85decode(encoded_string)
binary_data = zlib.decompress(decoded_data)

libc = ctypes.CDLL(None)
memfd_create = libc.memfd_create
memfd_create.restype = ctypes.c_int
memfd_create.argtypes = [ctypes.c_char_p, ctypes.c_uint]
fd = memfd_create(b"", 0)
if fd == -1:
	raise OSError("Failed to create memfd")
os.write(fd, binary_data)
pid = os.getpid()
try:
	subprocess.run([f"/proc/{pid}/fd/{fd}"])
finally:
	os.close(fd)
"""

def generate_file_tree(root_dir):
    tree = []
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            tree.append(f"{subindent}{file}")
    return '\n'.join(tree)

def combine_source_code_files(root_dir):
    combined_text = "File Tree:\n\n"
    combined_text += generate_file_tree(root_dir)
    combined_text += "\n\n\nFile Contents:"
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir)
            combined_text += f"\n\n----- {relative_path} -----\n"
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    combined_text += infile.read()
            except Exception as e:
                combined_text += f"Error reading file: {str(e)}\n"
    return combined_text

def encode_binary_data(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    compressed_data = zlib.compress(binary_data)
    encoded_data = base64.b85encode(compressed_data)
    return '"""' + encoded_data.decode('utf-8') + '"""'

src_code_text = combine_source_code_files(args.src)

binary_file_text = f"encoded_string = {encode_binary_data(args.binary)}\n"

with open(args.output, 'w', encoding='utf-8') as outfile:
	outfile.write(f"'''\n{src_code_text}\n'''\n\n{binary_file_text}{runner_code_text}")