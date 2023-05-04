import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

# Define a list of possible responses to customer queries
responses = {
    "greeting": ["Hello, how may I assist you?", "Welcome, how can I help you today?"],
    "booking": ["You may proceed to FishAirline.com for booking!"],
    "support_channel": ["You can contact our support team at support@example.com or by calling 1-800-123-4567."],
    "available-country": ["\nOur flights only operate within Southeast Asian countries.\nWhich only included:\n1. Brunei\n2. Cambodia\n3. Indonesia\n4. Laos\n5. Malaysia\n6. Myanmar\n7. Philippines\n8. Singapore\n9. Thailand\n10. Timor-Leste\n11. Vietnam"],
    "country_name": ["Fuck {country_name} people"],
    "not_understand": ["Fuck you, humans, please type something that I can understand", "I'm sorry, I didn't understand your query. Please try again."],
    "packages": ["2 Way Tickets", "1 Way Tickets"],
    "user_Intro": ["Hello {name}"],
    "my_name": ["Your name is {name}"],
    "task": ["Sure, let me assist you with that. Please provide your account information and I'll reset your password for you.",
             "I can definitely help you with that. Please give me a moment to update your account information."],
    "feedback": ["Thank you for your feedback. We'll take that into consideration as we continue to improve our services.", 
                 "We appreciate your feedback and will use it to improve our products and services."]
}

# Create a lemmatizer object
lemmatizer = WordNetLemmatizer()
name = ""
asean_countries = {'Brunei', 'Cambodia', 'Indonesia', 'Laos', 'Malaysia', 'Myanmar', 'Philippines', 'Singapore', 'Thailand', 'Vietnam'}

# Define a function to lemmatize a given sentence
def lemmatize_sentence(sentence):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)
    # Lemmatize each word
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    # Join the lemmatized words back into a sentence
    lemmatized_sentence = " ".join(lemmatized_words)
    return lemmatized_sentence

# Define a function to extract names from a sentence
def extract_names(query):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(query)
    # Tag the words with their part of speech
    tagged_words = nltk.pos_tag(words)
    # Extract the named entities from the tagged words
    named_entities = nltk.ne_chunk(tagged_words)
    # Filter out non-person named entities
    person_entities = [entity for entity in named_entities if isinstance(entity, nltk.tree.Tree) and entity.label() == "PERSON"]
    # Extract the person names from the person named entities
    person_names = [ " ".join([word[0] for word in entity.leaves()]) for entity in person_entities]
    return person_names

def extract_country_names(query):
    # tokenize the text
    tokens = nltk.word_tokenize(query)

    # use Part-of-Speech (POS) tagging to tag the words with their part of speech
    tagged_words = nltk.pos_tag(tokens)

    # use Named Entity Recognition (NER) to label the named entities in the text
    ner_tagged = nltk.ne_chunk(tagged_words)

    # Filter out non-person named entities
    country_entities = [entity for entity in ner_tagged if isinstance(entity, nltk.tree.Tree) and entity.label() == "GPE"]
    # Extract the person names from the person named entities
    country_names = [ " ".join([word[0] for word in entity.leaves()]) for entity in country_entities]
    return country_names

def booking_synonym(query):
    synonyms = []
    words = ["book", "buy"]
    for word in words:
        for syn in wordnet.synsets(word, pos=['n', 'v']):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
    return synonyms


# Define a function to handle customer queries and generate responses
def chatbot_response(query):
    global name  # Declare global variable to modify name inside the function

    # Lemmatize the query
    query_lemmas = lemmatize_sentence(query.lower())
    names = extract_names(query)
    country_names = extract_country_names(query)
    booking_synonym(query)
    if "hello" in query_lemmas or "hi" in query_lemmas and ("my" in query_lemmas and "name" in query_lemmas):
        # Check if the query includes the user's name
        if names:
            name = names[0]
            return responses["user_Intro"][0].format(name=name)
        else:
            return random.choice(responses["greeting"])
    elif "what" in query_lemmas and "is" in query_lemmas and "my" in query_lemmas and "name" in query_lemmas:
        if name:
            return responses["my_name"][0].format(name=name)
        else:
            return "I'm sorry, I didn't catch your name. Can you please tell me your name?"
    elif query in booking_synonym(query):
        return responses["booking"][0]
        #elif "country" in query_lemmas:
        #return responses["available-country"][0]
    elif country_names:
        country_name = country_names[0]
        if country_name not in asean_countries:
            return responses["not_understand"][0]
            # Country is not in ASEAN
            #return "I'm sorry, we currently only support countries in ASEAN."
        else:
            for country in asean_countries:
                if country == country_name:
                    return responses["country_name"][0].format(country_name=country_name)
    elif "support" in query_lemmas or "contact" in query_lemmas:
        return random.choice(responses["support_channel"])
    elif "reset" in query_lemmas or "update" in query_lemmas:
        return random.choice(responses["task"])
    elif "feedback" in query_lemmas or "review" in query_lemmas:
        return random.choice(responses["feedback"])
    else:
        return responses["not_understand"][1]
        #return "I'm sorry, I didn't understand your query. Please try again."



# Define a function to handle user interaction
'''
def chatbot():
    print("Welcome to our customer service chatbot!")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        response = chatbot_response(query)
        print("Chatbot: " + response)
        #print(person_names)

# Run the chatbot function
chatbot()
'''