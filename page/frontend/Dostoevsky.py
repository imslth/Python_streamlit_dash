from annotated_text import annotated_text
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


def main(content):

    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    messages = content.split(' ')
    results = model.predict(messages, k=1)
    word = list()
    for message, sentiment in zip(messages, results):
        if list(sentiment.keys()) == ['positive']:
            word.append((message, "pos", 'green'))
        elif list(sentiment.keys()) == ['negative']:
            word.append((message, "neg", 'red'))
        else:
            word.append(message)
        word.append(' ')

    return annotated_text(*word)

if __name__ == '__main__':
    main()