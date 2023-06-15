import PySimpleGUI as sg
import nltk
import string
import re
import stanza
from stanza.models.common.doc import Document

# Function to clean the text
import re
import string
import stanza

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

    # Generate questions
    questions = []
    for sentence in doc.sentences:
        question = ""
        num_nouns = 0
        marker = 0
        for word in sentence.words:
            if word.upos != 'PUNCT':
                if word.feats and 'Case=Nom' in word.feats:
                    if num_nouns == marker:
                        question += "कौन"
                        question += " "
                        marker += 1
                    else:
                        question += word.text
                        question += " "
                        num_nouns += 1
                else:
                    question += word.text
                    question += " "
        question = question.strip()
        question = question.strip(string.punctuation)
        question = re.sub(r'\s+', ' ', question)
        if len(question) > 0:
            questions.append(question)

    return questions


# Set the theme and element styling
sg.theme('Topanga')
sg.set_options(element_padding=(5, 5))

# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Arial', 24, 'bold'), justification='center')],
    [sg.Text('Team Name: Team DoNut Give Up', font=('Arial', 14), justification='center')],
    [sg.Text('Enter Story:', font=('Arial', 12))],
    [sg.Multiline(key='-STORY-', size=(80, 10))],
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
        story_text = values['-STORY-']

        # Check if the story text is provided
        if story_text:
            try:
                # Generate questions from the story
                questions = generate_questions(story_text)

                # Display the questions
                print("Generated Questions:")
                for question in questions:
                    print(question)

            except Exception as e:
                # Display error message
                print(f'Error generating questions: {str(e)}')
        else:
            # Display error message if no story text is provided
            print('Please enter a story')

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

        about_window = sg.Window('About Us', about_layout, finalize=True)

        while True:
            event, values = about_window.read()

            # If the window is closed or the 'Close' button is clicked, exit the loop
            if event == sg.WINDOW_CLOSED or event == '-CLOSE-':
                break

        about_window.close()

# Close the GUI window
window.close()
