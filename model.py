import nltk
nltk.download('nps_chat')
nltk.download('pi')
posts = nltk.corpus.nps_chat.xml_posts()[:10000]

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features


featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]

# 10% of the total data
size = int(len(featuresets) * 0.1)

train_set, test_set = featuresets[size:], featuresets[:size]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
question_types = ["whQuestion","ynQuestion"]
command_types = ['System']

def is_ques_using_nltk(ques):
    question_type = classifier.classify(dialogue_act_features(ques)) 
    print(question_type)
    return question_type in question_types

def is_command_using_nltk(command):
    command_type = classifier.classify(dialogue_act_features(command))
    print(command_type)
    return command_type in command_types

question_pattern = ["do i", "do you", "what", "who", "is it", "why","would you", "how","is there",
                    "are there", "is it so", "is this true" ,"to know", "is that true", "are we", "am i", 
                   "question is", "tell me more", "can i", "can we", "tell me", "can you explain",
                   "question","answer", "questions", "answers", "ask"]

command_pattern = ['!']

helping_verbs = ["is","am","can", "are", "do", "does"]

# check with custom pipeline if still this is a question mark it as a question

def is_question(message):
    message = message.lower().strip()
    if not is_ques_using_nltk(message):
        is_ques = False
        # check if any of pattern exist in sentence
        for pattern in question_pattern:
            is_ques  = pattern in message
            if is_ques:
                break
    elif not is_command_using_nltk(message):
        is_command = False
        for pattern in command_patterns:
            is_command = pattern in message
            if is_command:
                break

        # there could be multiple sentences so divide the sentence
        sentence_arr = message.split(".")
        for sentence in sentence_arr:
            if len(sentence.strip()):
                # if question ends with ? or start with any helping verb
                # word_tokenize will strip by default
                first_word = nltk.word_tokenize(sentence)[0]
                if sentence.endswith("?") or first_word in helping_verbs:
                    is_ques = True
                    break
        return is_ques    
    else:
        return True