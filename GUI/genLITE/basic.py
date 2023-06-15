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
        for i in range(i, min(i + 500, count)):  # Use min() to avoid index out of range error
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

    # Return the generated questions
    return questions

def main():
    print('Hindi Fable Story Question Generator')
    print('Team Name: Team DoNut Give Up')
    story_file = input('Enter the path to the story file: ')

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
        print('Please provide a path to the story file')

if __name__ == '__main__':
    main()
