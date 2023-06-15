import PySimpleGUI as sg
import os
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import indian
from nltk.tag import tnt
import string
import re
import stanza
from stanza.models.common.doc import Document

# Function to clean the text
def clean_text(text):
    text = re.sub(r'(\d+)', r'', text)
    text = text.replace(u'।', ' । ')
    text = text.replace(u',', '')
    text = text.replace(u'"', '')
    text = text.replace(u'(', '')
    text = text.replace(u')', '')
    text = text.replace(u'"', '')
    text = text.replace(u':', '')
    text = text.replace(u"'", '')
    text = text.replace(u"‘", '')
    text = text.replace(u"’", '')
    text = text.replace(u"''", '')
    text = text.replace(u".", '')
    text = text.replace(u"!", '')
    text = text.replace(u'“', '')
    text = text.replace(u'”', '')
    return text

# Function to generate questions from the story
def generate_questions(story_file):
    with open(story_file, 'r', encoding='utf-8') as f:
        story_text = f.read()

    cleaned_text = clean_text(story_text)

    # DEPENDENCY PARSING
    nlp = stanza.Pipeline(lang='hi', processors='depparse', depparse_pretagged=True)
    pretagged_doc = Document(cleaned_text)
    doc = nlp(pretagged_doc)

    # NOMINATIVE CASE
    questions = []
    output_list = []  # Replace this with your actual output list
    text = ""
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
        text = ""  
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
                        if (key == 'Case' and value == 'Nom' and output_list[i][1] == 'NOUN') or (
                                key == 'Case' and value == 'Nom' and output_list[i][1] == 'PRON'):
                            if flag == 0:
                                if marker == iter:
                                    temp = "कौन"
                                    text += temp
                                    text += " "
                                    i = i + 1
                                    flag = 1
                                    break
                                else:
                                    text += output_list[i][0]
                                    text += " "
                                    i = i + 1
                                marker = marker + 1
                                break
                            else:
                                text += output_list[i][0]
                                text += " "
                                i = i + 1
                                num = num + 1
                                break
                        else:
                            text += output_list[i][0]
                            text += " "
                            i = i + 1
                            break
                else:
                    text += output_list[i][0]
                    text += " "
                    i = i + 1
                    num = num + 1
                    break
            else:
                text += output_list[i][0]
                text += " "
                i = i + 1
                num = num + 1
                break
        text = text.strip()
        text = text.strip(string.punctuation)
        text = text.replace('  ', ' ')
        text = text.replace('  ', ' ')
        if len(text) > 0:
            questions.append(text)
        j = j + 1

  


# Set the theme and element styling
sg.theme('Topanga')
sg.set_options(element_padding=(5, 5))

# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Arial', 24, 'bold'), justification='center')],
    [sg.Text('Team Name: Team DoNut Give Up', font=('Arial', 14), justification='center')],
    [sg.Text('Select Story File:', font=('Arial', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), font=('Arial', 12), button_color=('white', '#008080')),
     sg.Button('About Us', key='-ABOUT-', size=(10, 2), font=('Arial', 12), button_color=('white', '#800080'))],
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

    # If the 'Generate Questions' button is clicked, generate the questions
    if event == '-GENERATE-':
        story_file = values['-STORY_FILE-']

        # Check if the story file is provided
        if story_file:
            try:
                # Generate questions from the story
                questions = generate_questions(story_file)

                # Save the questions to the output file
                base_name = os.path.basename(story_file)
                output_file = os.path.splitext(base_name)[0] + '_questions.txt'
                with open(output_file, 'w') as f:
                    for question in questions:
                        f.write(question + '\n')

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
            [sg.Image(filename='gargi_shroff.jpg', size=(100, 100)),
             sg.Image(filename='swarang_joshi.jpg', size=(100, 100)),
             sg.Image(filename='ketaki_shetye.jpg', size=(100, 100))],
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
