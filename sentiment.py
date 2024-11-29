
import re
import praw
import boto3

from anthropic import AnthropicBedrock
from comprehend_detect import ComprehendDetect

input_text = "What are the best stocks to buy if I like environment? Please return the ticker at the very end."
client = AnthropicBedrock(
    # Authenticate by either providing the keys below or use the default AWS credential providers, such as
    # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
    aws_access_key="your_access_key",
    aws_secret_key="your_secret_key",

    # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
    # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
    aws_region="us-west-2",
)

message = client.messages.create(
    model="anthropic.claude-3-sonnet-20240229-v1:0",
    max_tokens=256,
    messages=[{"role": "user", "content": input_text}],
)
texte = message.content[0].text
print(texte)


# Utilisation d'une expression régulière pour trouver les sigles
sigles = re.findall(r'\(([A-Z]+)\)', texte)

# Affichage des résultats
print(sigles)


url = "https://www.reddit.com/r/stocks/"
# page = requests.get(url)
# soup = BeautifulSoup(page.text, 'html.parser')
# soup = soup.getText(strip=True)

reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="yout_client_secret",
    password="yout_password",
    user_agent="your_user_agent",
    username="your_username",
)

reddit.read_only = True
subreddit = reddit.subreddit("stocks")



for submission in subreddit.new(limit=10):
    top_level_comments = list(submission.comments)


# Loop through stock symbols
for sigle in sigles:
    file_name = 'stocks/' + sigle + '_reddit.txt'
    
    # Create or clear the file initially
    open(file_name, 'w', encoding="utf-8").close() 
    
    # Open the file with encoding="utf-8" to write content
    with open(file_name, "w", encoding="utf-8") as write_to_file:
        for submission in subreddit.search(sigle, limit=10, sort="new"):
            write_to_file.write('Title : {}\n'.format(submission.title))
            write_to_file.write(submission.selftext + "\n")

            # Retrieve all comments
            all_comments = submission.comments.list()
            for comment in all_comments:
                # Check if comment is an instance of praw.models.Comment
                if isinstance(comment, praw.models.Comment):
                    write_to_file.write('Comment by {}: {}\n'.format(comment.author, comment.body))


### Amazon comprehend sentiment analysis

list_of_sentiments = []
s3_client = boto3.client('comprehend', 
                            aws_access_key_id='your_access_key',
                            aws_secret_access_key='your_secret_key',
                            region_name='us-west-2')
comprehendDetect_obj = ComprehendDetect(s3_client)

for sigle in sigles:
    file_name = 'stocks/' + sigle +'_reddit.txt'

    text = open(file_name, "r", encoding="utf-8").read()
    text = text[:3990] # Comprehend can only process 5000 bytes at a time
    comprehendDetect_obj.detect_sentiment(text, 'en')
    sentiment = comprehendDetect_obj.detect_sentiment(text, 'en')['Sentiment']
    sentiment_score = comprehendDetect_obj.detect_sentiment(text, 'en')['SentimentScore']
    sentiment_well_formatted = sentiment[0].upper() + sentiment.lower()[1:]
    output = {
        "Stock": sigle,
        "sentiment": sentiment_well_formatted,
        "sentiment_Score": sentiment_score[sentiment_well_formatted],
        }
    print(output)
    list_of_sentiments.append(output)

