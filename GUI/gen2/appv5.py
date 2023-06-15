import PySimpleGUI as sg

# Function to generate questions from the story
def generate_questions(story_file):
    # Your code to generate questions goes here...
    # Replace this placeholder code with your actual implementation
    questions = ['Question 1', 'Question 2', 'Question 3']
    return questions


# Set the theme and element styling
sg.theme('Material2')
sg.set_options(element_padding=(5, 5))


# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Google Sans', 24, 'bold'), justification='center')],
    [sg.Text('Team Name: Team Acute Triangle', font=('Google Sans', 14), justification='center')],
    [sg.Text('Select Story File:', font=('Google Sans', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), font=('Google Sans', 12), button_color=('white', '#008080')),
     sg.Button('About Us', key='-ABOUT-', size=(10, 2), font=('Google Sans', 12), button_color=('white', '#800080'))],
    [sg.Output(size=(80, 20), key='-OUTPUT-', font=('Google Sans', 12), background_color='white')]
]

# Create the GUI window
window = sg.Window('Hindi Fable Story Question Generator', layout, finalize=True)

#
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
                output_file = 'outputquestions.txt'
                with open(output_file, 'w') as f:
                    for question in questions:
                        f.write(question + '\n')

                # Display success message
                sg.popup_ok('Successfully generated questions. Saved to {output_file}', font=('Google Sans', 12), text_color='#008080')
            except Exception as e:
                # Display error message
                print(f'Error generating questions: {str(e)}')
        else:
            # Display error message if no story file is provided
            print('Please select a story file')

    # If the 'About Us' button is clicked, display information about the team members
    if event == '-ABOUT-':
        about_layout = [
            [sg.Text('About Us', font=('Google Sans', 24, 'bold'), justification='center', size=(30, 1))],
            [sg.Image(filename='gargi_shroff.jpg', size=(100, 100)),
             sg.Image(filename='swarang_joshi.jpg', size=(100, 100)),
             sg.Image(filename='ketaki_shetye.jpg', size=(100, 100))],
            [sg.Text('Gargi Shroff', font=('Google Sans', 12)), sg.Text('Swarang Joshi', font=('Google Sans', 12)), sg.Text('Ketaki Shetye', font=('Google Sans', 12))],
            [sg.Button('Close', key='-CLOSE-', font=('Google Sans', 12), button_color=('white', '#008080'), pad=(20, 10))]
        ]

        about_window = sg.Window('About Us', about_layout, modal=True, background_color='#282a36')

        while True:
            event, values = about_window.read()
            if event == '-CLOSE-' or event == sg.WINDOW_CLOSED:
                break

        about_window.close()

window.close()
