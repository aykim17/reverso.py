'''
reverso.py: a script for translation + context in the command-line using the Reverso Context API
https://github.com/flagist0/reverso_context_api
'''

from reverso_context_api import Client
from reverso_context_api import misc
import configparser
import argparse
import itertools

# Gets translation and context lists, then prints them
def _translate(client, source_text):
    print('Translation for ' + source_text + ':')

    try:
        translations = list(itertools.islice(client.get_translations(source_text), 3))

        if len(translations) == 0:
            print('Did you mean:')
            translations = list(client.get_search_suggestions(source_text))

        for translation in translations:
            print(translation)

        contexts = list(itertools.islice(client.get_translation_samples(source_text), 5))

        for context in contexts:
            print(context[0] + ' ' + context[1] + '\n')

    except requests.exceptions.HTTPError:
        print('Sorry, no translation found.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translation + Context using Reverso Context')
    parser.add_argument('word', metavar='word', type=str, nargs='+', help='word or phrase to translate')
    parser.add_argument('-k', '--keepalive', action='store_true', dest='keepalive', default=False, 
                        help='keep the program running after initial translation')

    args = parser.parse_args()

    # Can change the languages
    client = Client("de", "en")

    # Parse input to translate
    source_text = ''
    for word in args.word:
        source_text += word + ' '

    _translate(client, source_text)
    
    # Keep the program running for future translations
    if args.keepalive:
        print('Keep-alive mode enabled. * to end.')
        while True:
            source_text = input('Enter word/phrase: ')
            if source_text.strip() == '*':
                break

            _translate(client, source_text)
