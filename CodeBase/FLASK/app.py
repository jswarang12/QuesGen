import re
import string
import stanza
from flask import Flask, render_template, request

app = Flask(__name__)

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

    # ADJECTIVE
    adjective_questions = []  # List to store questions for adjective
    count = 0
    for item in output_list:
        if isinstance(item, tuple):
            count += 1
    j = 0
    i = 0
    num = 0
    marker = 0
    iter = 0
    while j < count :
        str=""
        i = j
        flag = 0
        num = 0
        marker = 0
        for i in range (i, i+30):
            red = 0
            if output_list[i][1]!='PUNCT':
                properties = output_list[i][3]
                if properties is not None :
                        pairs = properties.split('|')
                            #print(pairs)
                        case_value = None
                        for pair in pairs:
                            key, value = pair.split('=')
                        if output_list[i][1]=='ADJ' and key == 'Gender' and value == 'Masc':
                            if flag == 0 :
                                if marker == iter :
                                    temp="कैसा"
                                    str+=temp
                                    str+=" "
                                    i = i+1
                                    flag = 1
                                    break
                                else :
                                    str += output_list[i][0]
                                    str+=" "
                                    i=i+1
                                    marker = marker+1
                                    break
                            else :
                                str += output_list[i][0]
                                str+=" "
                                i=i+1
                                num = num + 1
                                break
                        elif output_list[i][1]=='ADJ' and key == 'Gender' and value == 'Fem':
                            if flag == 0 :
                                if marker == iter :
                                    temp="कैसी"
                                    str+=temp
                                    str+=" "
                                    i = i+1
                                    flag = 1
                                    break
                            else :
                                str += output_list[i][0]
                                str+=" "
                                i=i+1
                                marker = marker+1
                                break
                        else :
                            str += output_list[i][0]
                            str+=" "
                            i=i+1
                            num = num + 1
                            break
                elif output_list[i][1]=='ADJ':
                        if flag == 0 :
                            if marker == iter :
                                    temp="कैसे"
                                    str+=temp
                                    str+=" "
                                    i = i+1
                                    flag = 1
                                    break
                            else :
                                    str += output_list[i][0]
                                    str+=" "
                                    i=i+1
                                    marker = marker+1
                                    break
                        else :
                                str += output_list[i][0]
                                str+=" "
                                i=i+1
                                num = num + 1
                                break
                else:
                            str += output_list[i][0]
                            str+=" "
                            i=i+1
                            break
            else :
              str += output_list[i][0]
              str+=" "
              i=i+1

        else :
            break
        # print(str)
    if num == 0 :
        str += "?"
        j = i + 1
        if flag!=0:
          adjective_questions.append[str]
        marker = 0
        iter = 0
    else :
        iter = iter + 1
        str += "?"
        if flag!=0:
          adjective_questions.append[str]
    question_list.append(adjective_questions)

    return question_list

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Read story from the submitted file
        story_file = request.files['story_file']
        story_text = story_file.read().decode('utf-8')

        # Generate questions from the story
        questions = generate_questions(story_text)

        # Render the template with the generated questions
        return render_template('index.html', questions=questions)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5051)
