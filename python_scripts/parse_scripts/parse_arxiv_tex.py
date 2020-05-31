import re
from nltk import word_tokenize

# Reads data from .tex file and
def latex_parser(tex_file):
    # Only grab info from these sections.
    sections = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph', 'chapter', 'part']
    # Info we can skip used by commands
    commands = ['equation', 'table', 'align', 'keyword', 'figure', 'flalign', 'proof', 'longtab', 'longtable', 'CCSXML', 'gather', 'flush', 'multline', 'example','matrix', 'tabular', 'eqnarray', 'array']
    macros = ['beq', 'bmat', 'bea', 'be']
    # Keywords to indicate when to end early. Info we do not need follows these sections.
    end_early_commands = ['acknowledgment', 'reference', 'thebibliography', 'bibliography', 'appendices', 'appendix', 'acknowledgement', 'references', 'acknowledgments', 'acknowledgements']
    tokens = []
    with open(tex_file) as f:
        end_condition = False
        while True:
            line = f.readline()
            if [s for s in sections if line.lstrip().startswith('\\{}'.format(s.lower()))]:
                tokens, position, end_early = in_section(f, f.tell(), tokens, sections, commands, macros, end_early_commands)
                if end_early:
                    return tokens
                else:
                    f.seek(position)
            elif re.search(r'\\begin{abstract', line, re.IGNORECASE):
                tokens, position = in_abstract(line, f, tokens, True, sections, f.tell())
                f.seek(position)
            elif re.search(r'\\abstract', line, re.IGNORECASE):
                tokens, position = in_abstract(line, f, tokens, False, sections, f.tell())
                f.seek(position)
            end_early = [end for end in end_early_commands if stop_searching(line,end)]
            if not line:
                break
            elif len(end_early) > 0:
                return tokens
    return tokens


# Skip commands that include equations, figures, tables, etc.
def skip_commands(command, macro, file, position):
    # Sets the position of the file pointer
    file.seek(position)
    ending_macro = {'beq': 'eeq', 'bmat': 'emat', 'bea': 'eea', 'be': 'ee'}
    line = file.readline()
    
    if command:

        ## I noticed that equation and eqnarray for some files had differend ending commands so these are the cases that I observed.
        if (command == 'equation'):
            while (not re.search(r'\\end{equation|\\eeq|\\ee\s', line, re.I)) and (len(line) != 0):
                line = file.readline()
        elif (command == 'eqnarray'):
            while (not re.search(r'\\end{eqnarray|\\eea', line, re.I)) and (len(line) != 0):
                line = file.readline()
        else:
            while (not re.search(r'\\end\s*{{{}'.format(command), line, re.I)) and (len(line) != 0):
                line = file.readline()
    elif macro:
        while (not re.search(r'\\{}\s'.format(ending_macro[macro]), line, re.I)) and (len(line) != 0):
                line = file.readline()
    return file.tell()

# Stops searching once bibliography, references, or appendices section are encountered.
def stop_searching(line, command):
    line = line.strip()
    #print(line)
    #stop_a = (line.startswith('\\begin') or line.startswith('\\section')) and re.search(command, line, re.IGNORECASE)
    stop_b = line.lower() == '\\{}'.format(command)
    stop_c = True if re.search(r'\{%s\}'%command, line, re.IGNORECASE) else False
    return stop_b or stop_c
  
# Removes other tex commands.
def clean_up_line(line):
    # Removes $...$
    line = re.sub(r'\$[^\$]*?\$', '', line)
    # Removes [...]
    line = re.sub(r'\[[^\]]*?\]', '', line)
    # Removes \...{...}
    line = re.sub(r'\\[\w]*?\{[^\}]*?\}', '', line)
    # Removes @...
    line = re.sub(r'@\w*', '', line)
    # Removes {...}
    line = re.sub(r'\{[^\}]*?\}', '', line)
    # Removes %
    line = re.sub(r'\\%', '', line)
    # Removes inline comments
    line = re.sub(r'%.*', '', line)
    # Removes ...\\
    # line = re.sub(r'.*\\\\', '', line)
    # Removes \...
    line = re.sub(r'\\\w*', '', line)
    # Removes <...>
    line = re.sub(r'<[^<]*?>', '', line)
    # Removes digits
    line = re.sub(r'\d', '', line)
    # Removes underscores
    line = re.sub(r'_', '', line)
    # Removes {...
    line = re.sub(r'\{.*', '', line)
    # Removes ...}
    line = re.sub(r'.*\}', '', line)
    # Removes inline equations
    line = re.sub(r'\w*=\w*', '', line)
    # Removes all non-alpha-numeric characters (exept: space, hyphens, & apostrophes)
    line = re.sub(r'[^\w\s]', '', line)

    return line.lstrip()

def in_abstract(line, f, tokens, starts_with_begin, sections, pos):
    #print(line)
    f.seek(pos)
    if starts_with_begin:
        while (not re.search(r'\\end{abstract', line, re.IGNORECASE) and len(line) != 0):
            if not line.lstrip().startswith('%'):
                line = re.sub('^\{|\}$', '', line)
                line = clean_up_line(line.lstrip())
                tokens.extend(word_tokenize(line))
            line = f.readline()
        if not line.lstrip().startswith('%'):
            line = clean_up_line(line.lstrip())
            tokens.extend(word_tokenize(line))
        line = f.readline()
    else:
        while True:
            #print(line)
            if [s for s in sections if line.lstrip().startswith('\\{}'.format(s.lower()))]:
                return tokens, f.tell()-len(line)
            if not line:
                return tokens, f.tell()-len(line)
            else:
                line = re.sub(r'^\{|\}$', ' ', re.sub(r'\\abstract', '', line.lower()))
                if not line.lstrip().startswith('%'):
                    #print(line)
                    line = clean_up_line(line.lstrip())
                    tokens.extend(word_tokenize(line))
            line = f.readline()
    return tokens, f.tell()
def in_section(f, pos, tokens, sections, commands, macros, end_early_commands):
    f.seek(pos)
    while True:
        line = f.readline()
        if [s for s in sections if line.lstrip().startswith('\\{}'.format(s))]:
            end_early = [end for end in end_early_commands if stop_searching(line, end)]
            if len(end_early) > 0:
                return tokens, f.tell(), True
            return tokens, f.seek(f.tell() - len(line)), False
        else:
            # Check if a command is met in order to skip.
            command = [c for c in commands if line.lstrip().startswith('\\begin{{{}'.format(c))]
            if command:
                position = skip_commands(command[0], None, f, f.tell() - len(line))
                f.seek(position)
            # Check if a macro is met in order to skip
            macro = [m for m in macros if line.lstrip().startswith(r'\\{}\s'.format(m))]
            if macro:
                position = skip_commands(None, macro[0], f, f.tell() - len(line))
                f.seek(position)
            end_early = [end for end in end_early_commands if stop_searching(line, end)]
            if not line:
                break
            elif len(end_early) > 0:
                return tokens, f.tell(), True
            else:
                if not line.lstrip().startswith('%'):
                    line = clean_up_line(line.lstrip())
                    tokens.extend(word_tokenize(line))
    return tokens, f.tell(), False
