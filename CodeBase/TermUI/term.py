import re
import string
import stanza
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

    output_list = []  # List to store the output words with their properties

    # Iterate through the parsed sentences and extract word properties
    for sent in doc.sentences:
        for word in sent.words:
            word_tuple = (word.text, word.upos, word.head, word.feats)
            output_list.append(word_tuple)

    question_list = []  # List to store the generated questions

    # NOMINATIVE CASE
    nominative_questions = []  # List to store questions for nominative case
    count = len(output_list)
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
        for _ in range(500):
            if i >= count:
                break
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
                                    i += 1
                                    flag = 1
                                    break
                                else:
                                    str_question += output_list[i][0]
                                    str_question += " "
                                    i += 1
                                marker += 1
                                break
                            else:
                                str_question += output_list[i][0]
                                str_question += " "
                                i += 1
                                num += 1
                                break
                        else:
                            str_question += output_list[i][0]
                            str_question += " "
                            i += 1
                            break
                else:
                    str_question += output_list[i][0]
                    str_question += " "
                    i += 1
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
            iter += 1
            str_question += "?"
            if flag != 0:
                nominative_questions.append(str_question)

    question_list.append(nominative_questions)

    # ACCUSATIVE CASE
    accusative_questions = []  # List to store questions for accusative case
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
        for _ in range(500):
            if i >= count:
                break
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
                                    i += 1
                                    flag = 1
                                    break
                                else:
                                    str_question += output_list[i][0]
                                    str_question += " "
                                    i += 1
                                marker += 1
                                break
                            else:
                                str_question += output_list[i][0]
                                str_question += " "
                                i += 1
                                num += 1
                                break
                        else:
                            str_question += output_list[i][0]
                            str_question += " "
                            i += 1
                            break
                else:
                    str_question += output_list[i][0]
                    str_question += " "
                    i += 1
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
            iter += 1
            str_question += "?"
            if flag != 0:
                accusative_questions.append(str_question)

    question_list.append(accusative_questions)

    # INSTRUMENTAL CASE
    instrumental_questions = []  # List to store questions for instrumental case
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
        for _ in range(500):
            if i >= count:
                break
            if output_list[i][1] != 'PUNCT':
                properties = output_list[i][3]
                if properties is not None:
                    pairs = properties.split('|')
                    case_value = None
                    for pair in pairs:
                        key, value = pair.split('=')
                        if key == 'Case' and value == 'Ins' and (output_list[i][1] == 'NOUN' or output_list[i][1] == 'PRON'):
                            if flag == 0:
                                if marker == iter:
                                    temp = "किसके साथ"
                                    str_question += temp
                                    str_question += " "
                                    i += 1
                                    flag = 1
                                    break
                                else:
                                    str_question += output_list[i][0]
                                    str_question += " "
                                    i += 1
                                marker += 1
                                break
                            else:
                                str_question += output_list[i][0]
                                str_question += " "
                                i += 1
                                num += 1
                                break
                        else:
                            str_question += output_list[i][0]
                            str_question += " "
                            i += 1
                            break
                else:
                    str_question += output_list[i][0]
                    str_question += " "
                    i += 1
            else:
                break
        if num == 0:
            str_question += "?"
            j = i + 1
            if flag != 0:
                instrumental_questions.append(str_question)
            marker = 0
            iter = 0
        else:
            iter += 1
            str_question += "?"
            if flag != 0:
                instrumental_questions.append(str_question)

    question_list.append(instrumental_questions)

    

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
