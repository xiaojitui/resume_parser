# resume_parser

The scripts are used to parse resumes. 

### The functions include:
    (1) create_name_record.py
        Used to map "candidate name -> resume_filename -> resume_text -> interview pass/not".
        Final output format is: record[name]['X'] = resume's text, record[name]['y'] = 1/0 # pass/not
    
    (2) parse_cv_detail.py:
        - Used to parse candidate's school, degree, location, position, company
    
    (3) create_skillset_profile.py:
        Used to generate skillset profile database for each candidate
    
    (4) plot_wordcloud.py:
        Used to show word clouds of a resume
