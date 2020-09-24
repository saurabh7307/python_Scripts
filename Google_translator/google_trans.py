from googletrans import Translator
import pprint

data_file = 'data.txt'
pp = pprint.PrettyPrinter(indent=5)


def get_text_from_file(file):
    with open(file, 'r') as file:
        data = file.read()
        return data


def translate(source_language, desired_language):
    try:
        text = str(get_text_from_file(data_file))
        translator = Translator()
        return translator.translate(text, src=source_language, dest=desired_language)
    except Exception as exception:
        raise Exception("Exception while translating text : " + str(exception))


def print_data():
    data = translate('en', 'hi')
    before_translated = data.origin
    after_translated = data.text
    pp.pprint("Before : " + before_translated)
    pp.pprint("After : " + after_translated)


if __name__ == '__main__':
    print_data()
