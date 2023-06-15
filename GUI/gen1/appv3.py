import PySimpleGUI as sg

# Function to generate questions from the story
def generate_questions(story_file):
    # Your code to generate questions goes here...
    # Replace this placeholder code with your actual implementation
    questions = ['Question 1', 'Question 2', 'Question 3']
    return questions

# Set the theme and element styling
sg.theme('Reddit')
sg.set_options(element_padding=(5, 5))

# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Arial', 24, 'bold'), justification='center')],
    [sg.Text('Team Name: Team Acute Triangle', font=('Arial', 14), justification='center')],
    [sg.Text('Select Story File:', font=('Arial', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), font=('Arial', 12), button_color=('white', '#008080')),
     sg.Button('About Us', key='-ABOUT-', size=(10, 2), font=('Arial', 12), button_color=('white', '#800080'))],
    [sg.Output(size=(80, 20), key='-OUTPUT-', font=('Arial', 12), background_color='white')],
    [sg.Image(filename='gargi_shroff.jpg', size=(100, 100)),
     sg.Image(filename='swarang_joshi.jpg', size=(100, 100)),
     sg.Image(filename='ketaki_shetye.jpg', size=(100, 100))],
    [sg.Text('Gargi Shroff', font=('Arial', 12)), sg.Text('Swarang Joshi', font=('Arial', 12)), sg.Text('Ketaki Shetye', font=('Arial', 12))]
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
                output_file = 'outputquestions.txt'
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
        sg.popup_ok('Team Acute Triangle\n\n'
                    'Team Members:\n'
                    '1. Gargi Shroff - Roll Number\n'
                    '2. Swarang Joshi - Roll Number\n'
                    '3. Ketaki Shetye - Roll Number\n')

window.close()