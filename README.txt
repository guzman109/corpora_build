Author: Carlos Guzman
Bash scripts:
    Make sure to change the DIRECTORY variable to the location of your test data in both files. Also if you are getting
    a permissions error. Make sure to run
        $ chmod +x change_encoding
        $ chmod +x run_py_script
    To run both files simply use './' (current directory), for example,
        $ ./change_encoding
        $ ./run_py_script
    change_encoding:
        This file changes the encoding of text files with 'iso-8859-1' to 'utf-8' in order for the python script
        to recognize it. Make sure to change the DIRECTORY variable to the location of your test data.
    run_py_script:
        I used this mainly to gather all the tex files from all directories (test_data) and pass them to the python
        script as an argument.
Python scripts:
    main.py, refactor_parse_arxiv_tex.py, & tex_word_processing.py:
        main.py calls refactor_parse_arxiv_tex.py to read data from the tex file and tokenize
        the 'useful' information. Then main.py calls tex_word_processing.py to normalize the tokens some more and then
        categorize them into their respective categories.
