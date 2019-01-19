# encoding=utf8

import sys
import spacy as sp
from flask import Flask, request, jsonify, session, make_response, current_app
from flask_cors import CORS, cross_origin
import urllib.request
import urllib.parse
import csv
import os.path
import json
import gensim
from datetime import timedelta
from functools import update_wrapper
from PhraseVector import PhraseVector
from NumpyEncoder import NumpyEncoder

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app, support_credentials=True)
#print('Initiating ontology server...', file=sys.stderr)

# Load language model
#print('Preloading language model...', file=sys.stderr)
nlp = sp.load('en')
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

# Load ontology model
print('Initiating ontology server...', file=sys.stderr)
from owlready2 import *
import os
cwd = os.getcwd()
ontology_base = 'data/ontology/'
ontology_path = ontology_base + 'maintenance.'
onto_path.append(ontology_base)
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, ontology_path + "owl"))
ontology_prefix = basepath + '/' + ontology_path
ontology_prefix_clean = basepath + '/' + ontology_base
ontology = get_ontology(filepath).load()
ontology.load()
ontology_prefix = cwd + ontology_prefix 
iteration = 0


# test_issue = ontology.MaintenanceIssue("test_issue")
# test_use = ontology.BadUse("test_use")

# sync_reasoner()

# print("TEST1: ")
# print("-------")
# print()
# print(test_issue.__class__)

# print()
# print()

# print("TEST2: ")
# print("-------")
# print()

# test_issue.causedBy = [ test_use ]

# sync_reasoner()

# print(test_issue.__class__)

# print()
# print()

#Define ontology classes
# with ontology:
#     class LegalIssue(Thing):
#         response_classmap = {
#             ontology_prefix + 'MaintenanceIssue': 'Maintenance related issue.',
#             ontology_prefix + 'MinorIssue': 'The tenant is responsible for resolving the issue because:',
#             ontology_prefix + 'MajorIssue': 'The landlord is responsible for resolving the issue because:',
#             ontology_prefix + 'BadUse': 'The damage is caused by the tenants negligence (<a href="http://wetten.overheid.nl/BWBR0005290/2018-06-13#Boek7_Titeldeel4_Afdeling5_ParagraafOnderafdeling1_Artikel218">Section 218, Book 7</a>).',
#             ontology_prefix + 'NaturalCalamity': 'The damage has not been caused by the tenant (<a href="http://wetten.overheid.nl/BWBR0005290/2018-06-13#Boek7_Titeldeel4_Afdeling5_ParagraafOnderafdeling1_Artikel218">Section 218, Book 7</a>).',
#             ontology_prefix + 'SmallObject': 'The damaged object is small (<a href="http://wetten.overheid.nl/BWBR0005290/2018-06-13#Boek7_Titeldeel4_Afdeling5_ParagraafOnderafdeling1_Artikel240">Section 240, Book 7</a>).',
#             ontology_prefix + 'BigObject': 'The damaged object is large (<a href="http://wetten.overheid.nl/BWBR0005290/2018-06-13#Boek7_Titeldeel4_Afdeling5_ParagraafOnderafdeling1_Artikel240">Section 240, Book 7</a>).',
#             ontology_prefix + 'HighCost': 'The damage requires extensive actions to be resolved. (<a href="http://wetten.overheid.nl/BWBR0014931/2003-08-01">Minor Repairs Decree</a>).',
#             ontology_prefix + 'LowCost': 'The damage requires minor actionsto be resolved (<a href="http://wetten.overheid.nl/BWBR0014931/2003-08-01">Minor Repairs Decree</a>).',
#         }
#         ontology_properties = {
#             'causedBy': 'Was the damage caused by your actions?',
#             'associatedWithObject': 'What object was damaged?',
#             'hasCost': 'Does this object require more than 100 EURO to fix?'
#         }
#         ontology_property_classes = {
#             'causedBy': ['BadUse', 'NaturalCalamity'],
#             'associatedWithObject': ['BigObject', 'SmallObject'],
#             'hasCost': ['LowCost', 'HighCost']
#         }

        # Map resolved classes to their chatbot response
        # def GetResolvedOutput(self, resolved_class):
        #     return self.response_classmap.get(resolved_class)

        # # Get an explenation from a resolved class
        # def GetResolvedExplenation(self, resolved_class):
        #     explenation = []
        #     for property in self.ontology_properties:
        #         if property in dir(resolved_class):
        #             reasons = getattr(resolved_class, property)
        #             if len(reasons) > 0:
        #                 for reason in reasons:
        #                     class_str = str(reason.__class__).replace('\\', '/')
        #                     if '/' not in class_str:
        #                         class_str = ontology_prefix_clean + class_str
        #                     explenation.append(self.response_classmap.get(class_str))
        #     return explenation

        # # Get options
        # def GetOptionsByProperty(self, propertyName):
        #     if propertyName not in self.ontology_property_classes:
        #         return False
        #     propertyClasses = self.ontology_property_classes[propertyName]
        #     options = []
        #     for propertyClass in propertyClasses:
        #         for instance in ontology[propertyClass].instances():
        #             instance.lemma_ = lemmatizer(instance.name, 'VERB')[0]
        #             options.append(instance)
        #     return options

        # iteration = 0

        # def ResolveMaintenanceIssue(self, properties):
        #     self.iteration += 1
        #     print()
        #     print()
        #     # Create an instance from the given properties
        #     onto_instance = ontology.LegalIssue("maintenanceissue_" + str(self.iteration))
        #     #print("instance: " + str(onto_instance))
        #     print()
        #     print()
        #     print("properties: " + str(properties))
        #     print()
        #     print()
        #     for property in properties:
        #         #print("property: " + str(property))
        #         #print("other: " + str(properties.get(property)))
        #         setattr(onto_instance, property, properties.get(property))

        #     # Resolve the instance
        #     sync_reasoner()
        #     resolved_class = onto_instance.__class__
        #     print()
        #     print()
        #     print("TEST: " + str(resolved_class))
        #     print()
        #     print()
        #     resolved_classes = {
        #         ontology_prefix + 'MinorIssue',
        #         ontology_prefix + 'MajorIssue',
        #     }
        #     print()
        #     print()
        #     print("prefix: "  + str(ontology_prefix))
        #     print()
        #     print()
        #     resolved_class_str = str(resolved_class).replace('/', '\\')
            
        #     print("resolved: " + str(resolved_class_str))
        #     #
        #     #print("resolved class str" + str(resolved_class_str))

        #     if '\\' not in resolved_class_str:
        #         print("Kody1")
        #         resolved_class_str = ontology_prefix_clean + resolved_class_str
        #     if resolved_class_str in resolved_classes:
        #         print("Kody2")
        #         conclusion = self.GetResolvedOutput(resolved_class_str)
        #         support = self.GetResolvedExplenation(onto_instance)
        #         del onto_instance
        #         # close_world(onto_instance)
        #         return True, conclusion, support
        #     else:
        #         print("Kody3")
        #         conclusion = 'Not yet resolved! Need more facts.'
        #         missing = []
        #         for property in self.ontology_properties:
        #             if property not in properties:
        #                 missing.append({property: self.ontology_properties.get(property)})
        #         del onto_instance
        #         # close_world(onto_instance)
        #         print()
        #         print()
        #         print("missing: " + str(missing))
        #         print()
        #         print()
        #         return False, conclusion, missing

    # # Define possible maintenance conclusions
    # class MinorIssue(LegalIssue):
    #     equivalent_to = [
    #         ontology.MaintenanceIssue
    #         & (ontology.causedBy.some(ontology.BadUse) |
    #            ontology.associatedWithObject.some(ontology.SmallObject) |
    #            ontology.hasCost.some(ontology.LowCost))
    #     ]

    # class MajorIssue(LegalIssue):
    #     equivalent_to = [
    #         ontology.MaintenanceIssue
    #         & (ontology.causedBy.some(ontology.NaturalCalamity) &
    #            ontology.associatedWithObject.some(ontology.BigObject) &
    #            ontology.hasCost.some(ontology.HighCost))
    #     ]

# global sess
# sess = {}

# def set_errcnt(user, message):
#     # setattr(g, '_err_cnt', message)
#     sess[user] = message
#     return sess[user]


# def get_errcnt(user):
#     # err_cnt = getattr(g, '_err_cnt', None)
#     if not user in sess:
#         sess[user] = 0
#     return sess[user]


# conversations = {}
# asking = 'çausedBy'
# maint = LegalIssue()

from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

#################################################################################################################
# word2vec part
#################################################################################################################

print ( 'Initiating word2vec server...', file=sys.stderr)
assert gensim.models.word2vec.FAST_VERSION > -1, "Gensim fast version is disabled!"

# Load word2vec model
print ('Preloading word2vec model...', file=sys.stderr)
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "model/GoogleNews-vectors-negative300.bin"))
wordvec_model = gensim.models.keyedvectors.KeyedVectors.load_word2vec_format(filepath, binary=True)

print ('Preheating word2vec model...', file=sys.stderr)
wordvec_model.similar_by_word("heat")

# Load sample questions
print ('Preloading question-answer vectors...', file=sys.stderr)
question_vector_array = []
datapath = os.path.abspath(os.path.join(basepath, "model/civil_law_qa_en.csv"))
# datapath = os.path.abspath(os.path.join(basepath, "model/qa_unofficial.csv"))
f = open(datapath, 'rt', encoding="utf8")
reader = csv.reader(f)
# row = question,answer (row[0] = question, row[1] = answer)
# getting the (vector) embeddings for each question-answer pair
for row in reader:
    qa = row[0] + row[1]
    #for now we will compare question to question and not combined
    question_vector_array.append([PhraseVector(wordvec_model, row[0]), row[1]])
f.close()

print ('Starting server...', file=sys.stderr)

# Communication with frontend stuff and other models e.g. Watson, ontology reasoner etc: allow cross domain connections
def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, (str,bytes)):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, (str,bytes)):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/get_w2v", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_bot_response():
	# get question from the user
    userText = request.args.get('msg')

    # Create phrase vector from user input
    userVector = PhraseVector(wordvec_model, userText)

    # Match input vector with qa data
    bestScore = 0
    bestScoring = ''
    for question_vector in question_vector_array:
        similarity_to_query = userVector.CosineSimilarity(question_vector[0].vector)
        if similarity_to_query > bestScore:
            bestScore = similarity_to_query
            bestScoring = question_vector[1]

    if bestScoring == '' or bestScore < 0.5: bestScoring = 'Sorry, I can not help you with that problem.'
    return bestScoring

@app.route("/classify", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def classify_phrases():
    # Classify the given text as belonging to phrase1 or phrase2
    text = request.args.get('text')
    phrase1 = request.args.get('phrase1')
    phrase2 = request.args.get('phrase2')

    # Create phrase vector from user input
    userVector = PhraseVector(wordvec_model, text)
    phrase1Vector = PhraseVector(wordvec_model, phrase1)
    phrase2Vector = PhraseVector(wordvec_model, phrase2)

    # Classify
    sim_1 = userVector.CosineSimilarity(phrase1Vector.vector)
    sim_2 = userVector.CosineSimilarity(phrase2Vector.vector)

    if sim_1 + sim_2 < 0.5:
        return 'UNCLASSIFIED'
    elif sim_1 > sim_2:
        return 'phrase1'
    else:
        return 'phrase2'

@app.route("/getsimilar", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_similar_words():
    word = request.args.get('word')

    try:
        similar_words = wordvec_model.similar_by_word(word)
        return json.dumps(similar_words, cls=NumpyEncoder)
    except KeyError:
        return False


@app.route("/language", methods=['GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def detect_language():
    userText = request.args.get('msg')

    probabilities = {}

    tokens = wordpunct_tokenize(userText)
    words = [word.lower() for word in tokens]

    for lang in stopwords.fileids():
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        common_words = words_set.intersection(stopwords_set)
        probabilities[lang] = len(common_words)

    return max(probabilities, key=probabilities.get)


@app.route("/get_ont", methods=['GET', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def get_bot_response2():
    global iteration
    iteration += 1
    issue = ontology.MaintenanceIssue("issue" + str(iteration))
    if (request.args.get('usage') == '0'):
        print('seun0')
        use = ontology.BadUse("use" + str(iteration))
    else:
        print('seun1')
        use = ontology.WearAndTear("use" + str(iteration))

    if (request.args.get('propertyitem') == '0'):
        print('seun2')
        obj = ontology.BigObject("obj" + str(iteration))
    else:
        print('seun3')
        obj = ontology.SmallObject("obj" + str(iteration))

    if (request.args.get('actioncost') == '0'):
        print('seun4')
        cost = ontology.HighCost("cost" + str(iteration))
    else:
        print('seun5')
        cost = ontology.SmallObject("cost" + str(iteration))

    # link issue to properties using ontology relations
    issue.causedBy = [ use ]
    issue.associatedWithObject = [ obj ]
    issue.hasCost = [ cost ]

    sync_reasoner()

    print(issue.__class__)

    if ("MajorIssue" in str(issue.__class__)):
        response = {'text': 'The landlord may be responsible for resolving this issue.'}
        return jsonify(response)
    elif ("MinorIssue" in str(issue.__class__)):
        response = {'text': 'The tenant is generally responsible for repairing, replacing or maintaining such items in this case.'}
        return jsonify(response)
    else:
        response = {'text': 'I am not sure if the tenant or landlord is responsible for resolving this particular issue.'}
        return jsonify(response)

if __name__ == "__main__":
    port = 8080
    # Before was 5577
    # print('Starting ontology server on port  ' + str(port), file=sys.stderr)
    app.run(host='0.0.0.0', port=port)
    # app.run(port=port)
