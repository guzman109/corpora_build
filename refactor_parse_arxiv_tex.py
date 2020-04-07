import re
from nltk import word_tokenize

# Reads data from .tex file and
def latex_parser(tex_file):
    # Info we can skip used by commands
    commands = ['equation', 'table', 'align', 'keyword', 'figure', 'flalign', 'proof', 'CCSXML', 'flush', 'example']
    # Keywords to indicate when to end early. Info we do not need follows these sections.
    end_early_commands = ['acknowledgements', 'references', 'bibliography', 'appendices']
    tokens = []
    with open(tex_file) as f:
        while True:
            line = f.readline()
            # Check if a command is met in order to skip.
            command = [c for c in commands if line.lstrip().startswith('\\begin{{{}'.format(c))]
            if command:
                position = skip_commands(command[0], f, f.tell())
                f.seek(position)
                line = f.readline()
            if not line:
                break
            # Check if we have gotten to end of useful info in document.
            elif [end for end in end_early_commands if stop_searching(line, end)]:
                break
            else:
                if not line.lstrip().startswith('%'):
                    line = clean_up_line(line.lstrip())
                    tokens.extend(word_tokenize(line))

    return tokens


# Skip commands that include equations, figures, tables, etc.
def skip_commands(command, file, position):
    file.seek(position)
    while not file.readline().lstrip().startswith('\\end{{{}'.format(command)):
        continue
    return file.tell()


# Stops searching once bibliography, references, or appendices section are encountered.
def stop_searching(line, command):
    line = line.strip()
    stop_a = (line.startswith('\\begin') or line.startswith('\\section')) and re.search(command, line, re.IGNORECASE)
    stop_b = line.lower() == '\\{}'.format(command)
    return stop_a or stop_b

# Removes other tex commands.
def clean_up_line(line):
    # Removes $...$
    line = re.sub(r'\$[^\$]*\$', '', line)
    # Removes [...]
    line = re.sub(r'\[[^\]]*\]', '', line)
    # Removes \...{...}
    line = re.sub(r'\\[\w]*\{[^\}]*\}', '', line)
    # Removes @...
    line = re.sub(r'@\w*', '', line)
    # Removes {...}
    line = re.sub(r'\{[^\}]*\}', '', line)
    # Removes %
    line = re.sub(r'\\%', '', line)
    # Removes inline comments
    line = re.sub(r'%.*', '', line)
    # Removes ...\\
    line = re.sub(r'.*\\\\', '', line)
    # Removes \...
    line = re.sub(r'\\\w*', '', line)
    # Removes <...>
    line = re.sub(r'<[^<]*>', '', line)
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
    line = re.sub(r'[^\w\s\-\']', '', line)

    return line.lstrip()
