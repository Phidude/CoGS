
def get_salient_data(content, skip_lines):
    content = content[skip_lines:] # skips the first X number of lines containing metadata in the gamry data file
    return content
