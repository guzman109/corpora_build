import re
from nltk import word_tokenize

# Reads data from .tex file and
def latex_parser(tex_file):
    # Info we can skip used by commands
    commands = ['equation', 'table', 'align', 'keyword', 'figure', 'flalign', 'proof', 'CCSXML', 'flush', 'example','matrix', 'tabular', 'eqnarray', 'array']
    macros = ['beq', 'bmat', 'bea', 'be']
    # Keywords to indicate when to end early. Info we do not need follows these sections.
    end_early_commands = ['acknowledgements', 'references', 'bibliography', 'appendices']
    tokens = []
    try:
        with open(tex_file) as f:
            while True:
                line = f.readline()

                # Check if a command is met in order to skip.
                command = [c for c in commands if line.lstrip().startswith('\\begin{{{}'.format(c))]
                if command:
                    position = skip_commands(command[0], None, f, f.tell()-len(line))
                    f.seek(position)
                    line = f.readline()

                # Check if a macro is met in order to skip
                macro = [m for m in macros if line.lstrip().startswith(r'\\{}\s'.format(m))]
                if macro:
                    position = skip_commands(None, macro[0], f, f.tell()-len(line)) 
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
    except IOError as e:
        print('Operation failed: %s' % e.strerror)
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
    
    # This is used incase the original author did not include an ending macro or command for the particular section.
    #  if encountered then reset the position of the file pointer to the begining of the command and continue.
    if (line == ''):
        file.seek(position)
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
