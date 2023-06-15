import re
import string
import stanza
import PySimpleGUI as sg
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import PyPDF2
import pyperclip

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

# Function to generate and display the word cloud
def generate_word_cloud(story_text):
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(story_text)

    # Display word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Function to export questions as a PDF file
def export_to_pdf(file_path, questions):
    # Create a PDF file
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_writer.addPage(PyPDF2.PageObject.createBlankPage())  # Add a blank page

    # Set the questions as the content of the page
    page = pdf_writer.getPage(0)
    page.mergePage(PyPDF2.PdfFileReader(io.BytesIO(questions.encode())).getPage(0))

    # Save the PDF file
    with open(file_path, 'wb') as f:
        pdf_writer.write(f)

# Function to copy questions to clipboard
def copy_to_clipboard(questions):
    # Copy the questions to the clipboard
    pyperclip.copy(questions)

sg.theme('Topanga')
sg.set_options(element_padding=(5, 5))

# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Arial', 24, 'bold'), justification='center')],
    [sg.Text('Team Name: Team DoNut Give Up', font=('Arial', 14), justification='center')],
    [sg.Text('Select Story File:', font=('Arial', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), font=('Arial', 12),
               button_color=('white', '#008080')),
    #  sg.Button('Generate Wordcloud', key='-WORDCLOUD-', size=(20, 2), font=('Arial', 12),
    #            button_color=('white', '#008080')),
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

                # Calculate and display word count
                word_count = len(story_text.split())
                print(f'Word Count: {word_count}')

                # Calculate and display character count
                character_count = len(story_text)
                print(f'Character Count: {character_count}')

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
            [sg.Image(filename='gs.jpeg', size=(100, 100)),
             sg.Image(filename='sj.jpeg', size=(100, 100)),
             sg.Image(filename='ks.jpeg', size=(100, 100))],
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

    # If the 'Clear Output' button is clicked, clear the output area
    if event == '-CLEAR-':
        window['-OUTPUT-'].update('')

    # If the 'Generate Wordcloud' button is clicked, generate and display the word cloud
    # if event == '-WORDCLOUD-':
    #     story_file = values['-STORY_FILE-']

        # Check if the story file is provided
        if story_file:
            try:
                # Read story from file
                with open(story_file, 'r', encoding='utf-8') as file:
                    story_text = file.read()

                # Generate and display the word cloud
                generate_word_cloud(story_text)
            except Exception as e:
                # Display error message
                print(f'Error generating word cloud: {str(e)}')
        else:
            # Display error message if no story file is provided
            print('Please select a story file')

    # If the 'Export Questions' button is clicked, offer export options for the generated questions
    if event == '-EXPORT-':
        output_file = values['-OUTPUT_FILE-']
        if output_file:
            try:
                # Export the questions to the selected format
                if values['-FORMAT-'] == 'PDF':
                    export_to_pdf(output_file)
                elif values['-FORMAT-'] == 'Clipboard':
                    copy_to_clipboard(output_file)
                

                # Display success message
                print(f'Successfully exported questions to {values["-FORMAT-"]}')
            except Exception as e:
                # Display error message
                print(f'Error exporting questions: {str(e)}')
        else:
            # Display error message if no output file is provided
            print('Please select an output file')

window.close()
