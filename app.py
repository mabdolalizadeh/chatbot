import random
import nltk
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

words_that_express_want_need_or_search = [
    # Words that express "want"
    "want", "wanna", "desire", "wish", "long", "crave", "yearn", "fancy", "hanker", "prefer", "would like", "need",

    # Words that express "need"
    "require", "must", "have to", "essential", "obliged", "critical", "depend", "urgency", "indispensable",
    "necessitate", "compulsory",

    # Words that express "search"
    "search", "look for", "seek", "find", "hunt", "explore", "inquire", "seek out", "scavenge", "probe", "survey",
    "scrutinize", "dig", "scan"
]

greetings = [
    "hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy", "what's up",
    "what's happening",
    "how's it going", "how are you", "how do you do", "yo", "sup", "hi there", "hey there", "hola", "bonjour",
    "ciao", "salutations",
    "salud", "good day", "morning", "evening", "how’s everything", "what’s new", "long time no see",
    "hey, how are you"
]

nltk.download("wordnet")
nltk.download("omw-1.4")

lemmatizer = WordNetLemmatizer()


def check_msg(msg):
    for greeting in greetings:
        if fuzz.partial_ratio(msg.lower(), greeting) > 70:
            return 1, None

    words = msg.lower().split()
    for word in words:
        lemmatized_word = lemmatizer.lemmatize(word, pos='v')

        for need in words_that_express_want_need_or_search:
            if fuzz.partial_ratio(lemmatized_word, need) > 80:
                return 2, need

    return 0, None


def chatbot_response(msg):
    simple_answers = ['siktir', 'siiiiktir', 'siiiiiktiiiiiir', 'siiiiiiiiiiiiiiiiiiiiiktiiiiiiiiiiiiiiir']
    greeting = ['hi', 'hello', 'hey']
    start_msg = ['whats up?', 'how can i help you?', 'anything can i do?']

    msg_type, word = check_msg(msg)

    if msg_type == 1:
        return random.choice(greeting) + ', ' + random.choice(start_msg)
    elif msg_type == 2:
        if len(msg) < 20:
            return f'you {word} sth??, ' + simple_answers[0] + ' :/'
        elif len(msg) < 50:
            return f'you {word} sth??, ' + simple_answers[1] + ' :|'
        elif len(msg) < 80:
            return f'you {word} sth??, ' + simple_answers[2] + ' :('
        else:
            return f'you {word} sth??, ' + simple_answers[3] + ' :)'
    elif msg_type == 0:
        if len(msg) < 20:
            return simple_answers[0] + ' :/'
        elif len(msg) < 50:
            return simple_answers[1] + ' :|'
        elif len(msg) < 80:
            return simple_answers[2] + ' :('
        else:
            return simple_answers[3] + ' :)'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    bot_reply = chatbot_response(user_message)
    return jsonify({'reply': bot_reply})


if __name__ == '__main__':
    app.run(debug=False)
