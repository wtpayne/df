# ----------------------------------------------------------------------------
def _reindent_yaml(str_yaml):
    """
    Return a reformatted version of the input YAML.

    This function tries to make values line up
    vertically (within reason).

    If this is done, it makes the resulting
    YAML document MUCH easier to read.

    """

    # First pass. Work out maximum character
    # index of a key-value separator as well
    # as indentation blocks.
    #
    # TOOD: Handle string values
    #
    char_comment  = '#'  # Line comment character.
    char_kvsep    = ':'  # Key-value separator.
    idx_kvsep_max = -1   # Maximum column for key-value separator in doc.
    tup_lines     = tuple(str_yaml.splitlines())
    for line in tup_lines:

        is_comment = line.strip().startswith(char_comment)
        if is_comment:
            continue

        try:
            idx_kvsep_max = max(idx_kvsep_max, line.index(char_kvsep))
        except ValueError:
            continue

    # No key-value separator found.
    #
    if idx_kvsep_max == -1:
        return str_yaml

    # Work out a target indent index which
    # is a multiple of the tab size at least
    # two whitespace characters further than
    # the maximum index found of key-value
    # separators in the document.
    #
    min_sep_wspace = 2
    idx_val_min    = idx_kvsep_max + min_sep_wspace
    sz_tab         = 2
    idx_tgt_indent = ((idx_val_min + (sz_tab-1)) // sz_tab) * sz_tab
    idx_tgt_indent = min(36, idx_tgt_indent)

    list_lines = list()
    for line in tup_lines:

        is_comment = line.lstrip().startswith(char_comment)
        if is_comment:
            list_lines.append(line)
            continue

        idx_insert = line.index(char_kvsep) + 1

        if idx_insert >= len(line):
            list_lines.append(line)
            continue

        num_pad = idx_tgt_indent - idx_insert
        if num_pad <= 0:
            list_lines.append(line)
            continue

        char_pad = ' ' * num_pad
        line = line[:idx_insert] + char_pad + line[idx_insert:]
        list_lines.append(line)

    return '\n'.join(list_lines)