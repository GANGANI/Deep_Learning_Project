import json
import math
import random
import re
import sys
import statistics
import csv
import gzip
import json

from random import randint, shuffle
from sklearn import metrics

# from rapidfuzz import fuzz


from collections import Counter
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from sklearn.metrics.pairwise import cosine_similarity

# from bloc.util import cosine_sim
from bloc.util import get_bloc_variant_tf_matrix
from bloc.util import conv_tf_matrix_to_json_compliant
from bloc.util import fold_word
from bloc.generator import add_bloc_sequences 
from bloc.util import genericErrorInfo
from bloc.util import get_default_symbols
from bloc.util import getDictFromJson

from scipy.stats import entropy


def get_n_gram(user_id, bloc_tweets):
    
    if( len(bloc_tweets) == 0 ):
        return {}
    if(len(bloc_tweets)%2 != 0):
        bloc_tweets = bloc_tweets[:-1]

    number_of_bins = len(bloc_tweets)//2
    time_bins = {}
    for bin in range (0, number_of_bins):
        time_bins[bin] = []

    for i in range( len(bloc_tweets) ):
        bin = i//2
        time_bins[bin].append(i)

    prev_tweet_indices = []
    user_action_bloc = ''
    user_content_bloc = ''
    for bin, tweet_indices in time_bins.items():
        if( len(tweet_indices) == 0 ):
            continue

        if( set(prev_tweet_indices) == set(tweet_indices) ):
            continue

        action_doc = ''
        content_doc = ''
        for indx in tweet_indices:
            if( 'bloc' not in bloc_tweets[indx] ):
                continue
            if( 'bloc_sequences_short' not in bloc_tweets[indx]['bloc'] ):
                continue
            
            action_doc = action_doc + bloc_tweets[indx]['bloc']['bloc_sequences_short']['action']
            content_doc = content_doc + bloc_tweets[indx]['bloc']['bloc_sequences_short']['content_syntactic']
        user_action_bloc = user_action_bloc + "|" + action_doc
        user_content_bloc = user_content_bloc + "|" + content_doc
        
    return user_action_bloc[1:], user_content_bloc[1:], user_id

def get_bloc_string(tweets_files, entry, bloc_params):
    all_data = []
    min_tweets = 20

    user_class = ''
    all_bloc_symbols = get_default_symbols()

    tweets_files = entry['src']
    f = tweets_path + tweets_files  + '/tweets.jsons.gz'
    cf = '/'.join( f.split('/')[:-1] ) + '/userIds.txt'
    src = f.split('/')[-2]

    encoding = None
    if( src.find('stock') != -1 ):
        encoding = 'windows-1252'

    def get_user_id_class_map(f):

            user_id_class_map = {}
            all_classes = set()

            try:
                with open(f) as fd:
                    
                    rd = csv.reader(fd, delimiter='\t')
                    for user_id, user_class in rd:
                        user_id_class_map[user_id] = user_class
                        all_classes.add(user_class)
            except:
                genericErrorInfo()

            return user_id_class_map, all_classes

    with gzip.open(f, 'rt', encoding=encoding) as infile:
        # i =0
        for line in infile:      
            # if(i>2):
            #     continue
            # i +=1    
            try:

                line = line.split('\t')

                if( len(line) != 2 ):
                    continue
                
                user_id_class_map, all_classes = get_user_id_class_map( cf )
                user_class = user_id_class_map[ line[0] ]
                if tweets_files == 'astroturf':
                    user_class = 'bot'
                elif tweets_files == 'cresci-17' and (
                        user_class == 'bot-socialspam' or user_class == 'bot-traditionspam' or user_class == 'bot-fakefollower'):
                    user_class = 'bot'
                elif tweets_files == 'zoher-organization':
                    user_class = 'human'

                if( user_class == '' ):
                    continue
                
                tweets = getDictFromJson( line[1] )

                if( len(tweets) < min_tweets ):
                    continue

                bloc_payload = add_bloc_sequences(tweets, all_bloc_symbols=all_bloc_symbols, **bloc_params)
                
                action_bloc, content_bloc, user_id = get_n_gram(line[0], bloc_payload['tweets'])

                all_data.append({
                    'action_string':  action_bloc,
                    'content_string': content_bloc,
                    'user_id':user_id,
                    'useraccount': line[0],
                    'user_class' : user_class,
                    'src' : tweets_files,
                    'tweet_count':  len(bloc_payload['tweets']) if len(bloc_payload['tweets'])%2 == 0 else len(bloc_payload['tweets']) -1      
                })

            except:
                print("error")
                genericErrorInfo()

    return all_data

bot_dataset_files = [
    {'src': 'astroturf', 'classes': ['political_Bot']},
    {'src': 'kevin_feedback', 'classes': ['human', 'bot']},
    {'src': 'botwiki', 'classes': ['bot']},
    {'src': 'zoher-organization', 'classes': ['human', 'organization']},
    {'src': 'cresci-17', 'classes': ['human', 'bot-socialspam', 'bot-traditionspam', 'bot-fakefollower']},
    {'src': 'rtbust', 'classes': ['human', 'bot']},
    {'src': 'stock', 'classes': ['human', 'bot']},
    {'src': 'gilani-17', 'classes': ['human', 'bot']},
    {'src': 'midterm-2018', 'classes': ['human']},
    {'src': 'josh_political', 'classes': ['bot']},
    {'src': 'pronbots', 'classes': ['bot']},
    {'src': 'varol-icwsm', 'classes': ['bot', 'human']},
    {'src': 'gregory_purchased', 'classes': ['bot']},
    {'src': 'verified', 'classes': ['human']}
]

tweets_files = 'kevin_feedback'
tweets_path = "../retraining_data/"


bloc_params =  {'blank_mark': 60, 'bloc_alphabets': ['action', 'content_syntactic'], 'days_segment_count': -1, 'fold_start_count': 10, 'gen_rt_content': True, 'keep_bloc_segments': True, 'keep_tweets': True, 'minute_mark': 5, 'segmentation_type': 'segment_on_pauses', 'segment_on_pauses': 300, 'sort_action_words': False, 'tweet_order': 'sorted'}

output_data = []
for entry in bot_dataset_files:
    data = get_bloc_string(tweets_files, entry, bloc_params)
    output_data.extend(data)

with open('output_file.json', 'w', encoding='utf-8') as file:
    json.dump(output_data, file, indent=4, ensure_ascii=False)

print("All objects saved in 'output_file.json'")