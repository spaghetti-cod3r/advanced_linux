def patch_binary_file(input_file, output_file, original_line, patched_line):
    # hex strings to bytes
    if isinstance(original_line, str):
        original_line = bytes.fromhex(original_line.replace(" ", ""))
    if isinstance(patched_line, str):
        patched_line = bytes.fromhex(patched_line.replace(" ", ""))
    
    # open first file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # replace line
    modified_data = data.replace(original_line, patched_line)
    
    if modified_data == data:
        print("warning: the sequence was not found")
    else:
        print("patched Successfully!")
    
    # update the second file
    with open(output_file, 'wb') as f:
        f.write(modified_data)

# original line
original = "48 8D 3D A9 3A 00 00 E8 B4 FB FF FF 85 C0 75 07"
# patched line 
patched = "48 8D 3D A9 3A 00 00 31 C0 90 90 90 85 C0 75 07"


patch_binary_file("hack_app", "patched", original, patched)