import PySimpleGUI as sg

# Function to generate questions from the story
def generate_questions(story_file):
    # Your code to generate questions goes here...
    # Replace this placeholder code with your actual implementation
    questions = ['Question 1', 'Question 2', 'Question 3']
    return questions

# Set the theme and element styling
sg.theme('LightBlue3')
sg.set_options(element_padding=(5, 5))

# Create the GUI window layout
layout = [
    [sg.Text('Hindi Fable Story Question Generator', font=('Helvetica', 20), justification='center')],
    [sg.Text('Select Story File:', font=('Helvetica', 12)), sg.Input(key='-STORY_FILE-'), sg.FileBrowse()],
    [sg.Button('Generate Questions', key='-GENERATE-', size=(20, 2), pad=((120, 0), 10))],
    [sg.Output(size=(80, 20), key='-OUTPUT-', font=('Helvetica', 12), background_color='white')]
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

window.close()
