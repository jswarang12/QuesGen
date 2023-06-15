import re
import string
import stanza
import PySimpleGUI as sg
import os


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
    [sg.Text('Select Story File:', font=('Arial', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), font=('Arial', 12),
               button_color=('white', '#008080')),
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
                # Read story from file
                with open(story_file, 'r', encoding='utf-8') as file:
                    story_text = file.read()

                # Generate questions from the story
                questions = generate_questions(story_text)

                # Save the questions to the output file
                base_name = os.path.basename(story_file)
                output_file = os.path.splitext(base_name)[0] + '_questions.txt'
                with open(output_file, 'w', encoding='utf-8') as f:
                    for question in questions:
                        f.write(question.strip() + '?\n')

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
