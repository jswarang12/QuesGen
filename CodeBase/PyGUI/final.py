import re
import string
import stanza
import PySimpleGUI as sg
import os
import matplotlib.pyplot as plt
import io

# Function to clean the text
def clean_text(text):
    text = re.sub(r'\d+', '', text)
    text = text.replace(u'।', ' । ')
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Function to generate questions from the story
def generate_questions(story_text):
    cleaned_text = clean_text(story_text)
    # DEPENDENCY PARSING
    nlp = stanza.Pipeline(lang='hi', processors='tokenize,pos,lemma,depparse', tokenize_no_ssplit=True)
    doc = nlp(cleaned_text)

    output_list = []  # List to store the output words with their properties

    # Iterate through the parsed sentences and extract word properties
    for sent in doc.sentences:
        for word in sent.words:
            word_tuple = (word.text, word.upos, word.head, word.feats)
            output_list.append(word_tuple)

    question_list = []  # List to store the generated questions

    # NOMINATIVE CASE
    nominative_questions = []  # List to store questions for nominative case
    count = 0
    for item in output_list:
        if isinstance(item, tuple):
            count += 1
    j = 0
    i = 0
    num = 0
    marker = 0
    iter = 0
    while j < count:
        str_question = ""
        i = j
        flag = 0
        num = 0
        marker = 0
        for i in range(i, i + 500):
            red = 0
            if output_list[i][1] != 'PUNCT':
                properties = output_list[i][3]
                if properties is not None:
                    pairs = properties.split('|')
                    case_value = None
                    for pair in pairs:
                        key, value = pair.split('=')
                        if key == 'Case' and value == 'Nom' and (output_list[i][1] == 'NOUN' or output_list[i][1] == 'PRON'):
                            if flag == 0:
                                if marker == iter:
                                    temp = "कौन"
                                    str_question += temp
                                    str_question += " "
                                    i = i + 1
                                    flag = 1
                                    break
                                else:
                                    str_question += output_list[i][0]
                                    str_question += " "
                                    i = i + 1
                                marker = marker + 1
                                break
                            else:
                                str_question += output_list[i][0]
                                str_question += " "
                                i = i + 1
                                num = num + 1
                                break
                        else:
                            str_question += output_list[i][0]
                            str_question += " "
                            i = i + 1
                            break
                else:
                    str_question += output_list[i][0]
                    str_question += " "
                    i = i + 1
            else:
                break
        if num == 0:
            str_question += "?"
            j = i + 1
            if flag != 0:
                nominative_questions.append(str_question)
            marker = 0
            iter = 0
        else:
            iter = iter + 1
            str_question += "?"
            if flag != 0:
                nominative_questions.append(str_question)

    question_list.append(nominative_questions)

    # ACCUSATIVE CASE
    accusative_questions = []  # List to store questions for accusative case
    count = 0
    for item in output_list:
        if isinstance(item, tuple):
            count += 1
    j = 0
    i = 0
    num = 0
    marker = 0
    iter = 0
    while j < count:
        str_question = ""
        i = j
        flag = 0
        num = 0
        marker = 0
        for i in range(i, i + 500):
            red = 0
            if output_list[i][1] != 'PUNCT':
                properties = output_list[i][3]
                if properties is not None:
                    pairs = properties.split('|')
                    case_value = None
                    for pair in pairs:
                        key, value = pair.split('=')
                        if key == 'Case' and value == 'Acc' and (output_list[i][1] == 'NOUN' or output_list[i][1] == 'PRON'):
                            if flag == 0:
                                if marker == iter:
                                    temp = "किसे"
                                    str_question += temp
                                    str_question += " "
                                    i = i + 1
                                    flag = 1
                                    break
                                else:
                                    str_question += output_list[i][0]
                                    str_question += " "
                                    i = i + 1
                                marker = marker + 1
                                break
                            else:
                                str_question += output_list[i][0]
                                str_question += " "
                                i = i + 1
                                num = num + 1
                                break
                        else:
                            str_question += output_list[i][0]
                            str_question += " "
                            i = i + 1
                            break
                else:
                    str_question += output_list[i][0]
                    str_question += " "
                    i = i + 1
            else:
                break
        if num == 0:
            str_question += "?"
            j = i + 1
            if flag != 0:
                accusative_questions.append(str_question)
            marker = 0
            iter = 0
        else:
            iter = iter + 1
            str_question += "?"
            if flag != 0:
                accusative_questions.append(str_question)

    question_list.append(accusative_questions)

    # CARDINAL NUMBERS
    cardinal_questions = []  # List to store questions for cardinal numbers
    count = 0
    for item in output_list:
        if isinstance(item, tuple):
            count += 1
    j = 0
    i = 0
    num = 0
    marker = 0
    iter = 0
    while j < count:
        str_question = ""
        i = j
        flag = 0
        num = 0
        marker = 0
        for i in range(i, i + 500):
            red = 0
            if output_list[i][1] != 'PUNCT':
                properties = output_list[i][3]
                if properties is not None:
                    pairs = properties.split('|')
                    case_value = None
                    for pair in pairs:
                        key, value = pair.split('=')
                        if key == 'NumType' and value == 'Card' and (output_list[i][1] == 'NUM'):
                            if flag == 0:
                                if marker == iter:
                                    temp = "कितने"
                                    str_question += temp
                                    str_question += " "
                                    i = i + 1
                                    flag = 1
                                    break
                                else:
                                    str_question += output_list[i][0]
                                    str_question += " "
                                    i = i + 1
                                marker = marker + 1
                                break
                            else:
                                str_question += output_list[i][0]
                                str_question += " "
                                i = i + 1
                                num = num + 1
                                break
                        else:
                            str_question += output_list[i][0]
                            str_question += " "
                            i = i + 1
                            break
                else:
                    str_question += output_list[i][0]
                    str_question += " "
                    i = i + 1
            else:
                break
        if num == 0:
            str_question += "?"
            j = i + 1
            if flag != 0:
                cardinal_questions.append(str_question)
            marker = 0
            iter = 0
        else:
            iter = iter + 1
            str_question += "?"
            if flag != 0:
                cardinal_questions.append(str_question)

    question_list.append(cardinal_questions)

    return question_list


sg.theme('Topanga')
sg.set_options(element_padding=(5, 5))

# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Arial', 24, 'bold'), justification='center')],
    [sg.Text('Team Name: Team DoNut Give Up', font=('Arial', 14), justification='center')],
    [sg.Text('Select Story File:', font=('Arial', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), font=('Arial', 12),
               button_color=('white', '#008080')),
    
     sg.Button('About Us', key='-ABOUT-', size=(10, 2), font=('Arial', 12), button_color=('white', '#800080')),
     sg.Button('Clear Output', key='-CLEAR-', size=(10, 2), font=('Arial', 12), button_color=('white', '#FF0000'))],
    [sg.Output(size=(80, 20), key='-OUTPUT-', font=('Arial', 12), background_color='#FFFFFF', text_color='#000000')]
]

# Create the GUI window
window = sg.Window('Hindi Fable Story Question Generator', layout, finalize=True)

# Event loop to process GUI events

while True:
    event, values = window.read()

    # If the window is closed or the 'Exit' button is clicked, exit the loop
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    if event == '-CLEAR-':
        window['-OUTPUT-'].update('')

    # If the 'Generate Questions' button is clicked, generate the questions
    if event == '-GENERATE-':
        story_file = values['-STORY_FILE-']

        # Check if the story file is provided
        if story_file:
            try:
                # Read story from file
                with open(story_file, 'r', encoding='utf-8') as file:
                    story_text = file.read()

                # Generate questions from the story
                questions = generate_questions(story_text)

                
                # Save the questions to the output file
                base_name = os.path.basename(story_file)
                output_file = os.path.splitext(base_name)[0] + '_questions.txt'
                with open(output_file, 'w', encoding='utf-8') as f:
                    for case_questions in questions:
                        for question in case_questions:
                            f.write(question)
                            f.write('\n')  # Add a new line after each question





                # Display success message
                print(f'Successfully generated questions. Saved to {output_file}')
            except Exception as e:
                # Display error message
                print(f'Error generating questions: {str(e)}')
        else:
            # Display error message if no story file is provided
            print('Please select a story file')

    # If the 'About Us' button is clicked, display information about the team members
    if event == '-ABOUT-':
        about_layout = [
            [sg.Text('About Us', font=('Arial', 20, 'bold'), justification='center')],
            
            [sg.Text('Gargi Shroff - 2022114009', font=('Arial', 12)),
             sg.Text('Swarang Joshi - 2022114010', font=('Arial', 12)),
             sg.Text('Ketaki Shetye - 2022114013', font=('Arial', 12))],
            [sg.Button('Close', key='-CLOSE-', size=(10, 2), font=('Arial', 12), button_color=('white', '#800080'))]
        ]

        about_window = sg.Window('About Us', about_layout, modal=True)

        while True:
            event, values = about_window.read()
            if event == '-CLOSE-' or event == sg.WINDOW_CLOSED:
                break

        about_window.close()

window.close()
