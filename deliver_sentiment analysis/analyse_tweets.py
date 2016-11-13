import csv
import os.path
import re
import string



def load_data(file_name, line_limit):
    """"Use to load data from CSV file to a dictionary"""
    if os.path.isfile(file_name):
        reader = csv.reader(open(file_name, 'r', encoding="latin-1"))
        csv_list = []
        for row in reader:
            csv_list += row
        return csv_list
    else:
        raise "File does not exist on path {0}".format(file_name)

def cleanse_data(csv_list):
    """Use to clean data beofre processing"""
    tweets_without_rt = []
    clean_tweets = []
    for tweet in csv_list:
        #Check if tweet is a retweet , if yes then ignore
        if tweet.startswith("RT"):
            continue
        else :
        # Eliminate @ from the string
            #tweets_without_atrate += [re.sub(r'(\s)@\w+', r'\1', tweet)]
            tweet_without_atrate = ' '.join(word for word in tweet.split(' ') if not word.startswith('@'))
        #Eliminate all comma from a tweet

            tweet_without_comma =  str(tweet_without_atrate).replace(",","")

        #Eliminate all fulllstops form tweet
            tweet_without_fullstop = str(tweet_without_comma).replace(".","")

        #Eliminate all question mark form tweet
            tweet_without_question_mark= str(tweet_without_fullstop).replace("?","")

        # Eliminate all Exclamation form tweet
            tweet_without_exclamation =str(tweet_without_question_mark).replace("!","")

        # Eliminate all hash form tweet
            tweet_without_hash=str(tweet_without_exclamation).replace("#","")

        # Eliminate all appostophy form tweet
            tweet_without_appostophy =str(tweet_without_hash).replace("'","")

        # Eliminate all appostophy form tweet
            tweet_without_backslash =str(tweet_without_appostophy).replace("\\", "")

        # Eliminate html URL form tweet
            tweet_without_URL = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet_without_backslash, flags=re.MULTILINE)

        #Eliminate un-necessary space
            tweet_without_extraspace = str(tweet_without_URL).replace("  ", " ")

        #Lower all alphabetes in the tweet
            tweet_with_lower_alphabets = tweet_without_extraspace.lower()

            clean_tweets += [tweet_with_lower_alphabets]
    return clean_tweets

def analyse_sentiment(clean_tweets, positive_corpus, negative_corpus):
    """use to performa actual sentiment analysis over the data"""

    with open('polarity.csv', 'w', encoding='latin-1') as csvfile:
        fieldnames = ['tweet_text', 'positive_score' , 'negative_score','neutral_score','total_score','polarity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()

        for tweet in clean_tweets:
            tweet_tokens = tweet.split()
            positive_score = 0
            negative_score = 0
            total_score = 0
            for each_token in tweet_tokens:
                if each_token in positive_corpus:
                    positive_score += 1
                elif each_token in negative_corpus:
                    negative_score += 1
                else:
                    neutral_score = 0
            total_score = positive_score - negative_score
            if total_score > 0 :
                polarity = 'positive'
            elif total_score < 0:
                polarity = 'negative'
            else:
                polarity = 'could not determine'

            writer.writerow({'tweet_text': tweet, 'positive_score': positive_score, 'negative_score' : negative_score,
                             'neutral_score' : neutral_score, 'total_score' : total_score, 'polarity' : polarity})


    return polarity



def analyse_sentiment_for_trustworthiness(user_list,trust_corpus,uuntrust_corpus):
    fieldnames = ['Username', 'tweet_text', 'trust_score', 'untrust_score', 'neutral_score', 'total_score',
                  'worthiness']
    with open('Worthiness.csv', 'w', encoding='latin-1') as csvfile:
    #with csv.DictWriter(open('Worthiness.csv', 'w'), delimiter=',', lineterminator='\n',fieldnames=fieldnames )  as csvfile:
        fieldnames = ['Username','tweet_text', 'trust_score', 'untrust_score', 'neutral_score', 'total_score', 'worthiness']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()

        for key ,values in user_list.items():
            for tweet_value in values:
                tweet_token=str(tweet_value).split()
                trust_score=0
                untrust_score=0
                for each_token in tweet_token:
                    if each_token in trust_corpus:
                        trust_score +=1
                    elif each_token in uuntrust_corpus:
                        untrust_score +=1
                    else:
                        neutral_socre =0
                total_score =trust_score -untrust_score
                if total_score > 0:
                    worthiness="Trustworthy"
                elif total_score <0:
                    worthiness ="Üntrustworthy"
                else:
                    worthiness ="Could Not Determine"

                writer.writerow({'Username':key,'tweet_text':tweet_value, 'trust_score': trust_score, 'untrust_score': untrust_score,
                                 'neutral_score': neutral_socre, 'total_score': total_score, 'worthiness': worthiness})

    return worthiness


def group_user_and_tweets(csv_list):
    """Used for grouping user and tweets, the result should be like this
    @abc : [tweet1, tweet2, tweet3]
    @dbc : [tweet 1, tweet 2, tweet3]
    """
    user_tweet_dict = {}
    existing_users = []
    for tweet in csv_list:
        # Check if tweet is a retweet , if yes then ignore
        if tweet.startswith("RT"):
            continue
        elif(tweet.startswith("@")):
            existing_users += [tweet.split(' ', 1)[0]]

    for each_user in set(existing_users):
        user_tweet_list=[]
        user_name  = each_user.replace("@","")
        for tweet in csv_list:
            if tweet.startswith("@") and tweet.split(' ', 1)[0] == each_user :
                user_tweet_list.append(tweet)
                #user_tweet_dict.update({user_name:tweet})
        user_tweet_dict.update({user_name:user_tweet_list})

    return user_tweet_dict

#Grouping each user along with its various wothiness
def grp_user_name_worthiness(worthiness_csv):
    reader = csv.reader(open('D:/myproj/sentiment analysis/Worthiness.csv', 'r', encoding="latin-1"))
    existing_user=[]
    user_worthiness_dict={}
    worthiness_data = []

    for row in reader:
        existing_user += [row[0]]
        worthiness_data += [row]

    for each_user in set(existing_user):
        worthiness_list = []
        user_name = each_user.replace("@", "")
        for row in worthiness_data:
            if row[0] == each_user:
                worthiness_list.append(row[6])
        user_worthiness_dict.update({each_user: worthiness_list})

    return user_worthiness_dict

#calculating worthiness /Unworthiness of a person and storing it in a dictonary
def sentiment_analysis_score(user_worthiness_dict):
    final_user_trust_dict={}


    could_not_determine=0
    for key,values in user_worthiness_dict.items():
        trustworthy_score = 0
        untrustworthy_score = 0
        #print (key,values)
        for worthiness_value in values:

            if worthiness_value =="Trustworthy":
                trustworthy_score +=1
            elif worthiness_value =="Üntrustworthy":
                untrustworthy_score +=1
            #else:
             #   could_not_determine +=1
        final_score =trustworthy_score-untrustworthy_score
        if final_score >0:
            sentiment ="Trustworthy"
        elif final_score <0:
            sentiment ="Untrustworthy"
        else :
            sentiment ="Could Not Determine"
        final_user_trust_dict.update({key:sentiment})
    return final_user_trust_dict


def main():
    """Main method to call"""
    #loading tweets from CSV
    csv_list = load_data("D:/myproj/sentiment analysis/tweet.csv", "1")
    # Cleaning tweets
    clenased_tweets =  cleanse_data(csv_list)
    #Loading negative_corpus
    negative_corpus = load_data("D:/myproj/sentiment analysis/negative_corpus.csv", "1")
    #loading positive_corpus
    positive_corpus = load_data("D:/myproj/sentiment analysis/positive_corpus.csv", "1")
    #loading trust corpus
    trust_corpus = load_data("D:/myproj/sentiment analysis/trust_corpus.csv", "1")
    #loading untrust_corpus
    untrust_corpus = load_data("D:/myproj/sentiment analysis/untrust_corpus.csv", "1")
    #calling analyse_sentiment function
    score = analyse_sentiment(clenased_tweets, positive_corpus, negative_corpus)
    #calling group_user_and_tweets
    user_list = group_user_and_tweets(csv_list)
    #calling load_data to load worthiness.csv
    worthiness_data = load_data("D:/myproj/sentiment analysis/worthiness.csv", "1")
    #calling analyse_sentiment_for_trustworthiness function
    worthiness_score = analyse_sentiment_for_trustworthiness(user_list, trust_corpus, untrust_corpus)
    #calling grp_user_worthiness to group user and their worthiness
    user_worthiness_dict =  grp_user_name_worthiness(worthiness_data)
    #final sentiment analysis score dictonary
    sentiment_analysis_score_result =sentiment_analysis_score(user_worthiness_dict)
    print(sentiment_analysis_score_result)

if __name__ == '__main__':
    main()