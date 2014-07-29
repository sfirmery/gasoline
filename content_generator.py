import random

from flask.ext.script import Command, Option


class Markov(object):
    """content generator
    source: https://gist.github.com/agiliq/131679/"""

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words

    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i + 1], self.words[i + 2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size - 3)
        seed_word, next_word = self.words[seed], self.words[seed + 1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in xrange(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)


class GenerateContent(Command):
    """gen random documents"""

    def __init__(self):
        self.default_number = 1
        self.default_space = u'main'

    def get_options(self):
        return [
            Option('-n', '--number', dest='number',
                   default=self.default_number),
            Option('-s', '--space', dest='space',
                   default=self.default_space),
        ]

    def run(self, number, space):
        from gasoline.models import BaseDocument, User
        from codecs import open

        file_ = open('./poe.txt',
                     encoding='utf-8')
        self.markov = Markov(file_)

        try:
            space = unicode(space.encode('utf-8'))
        except ValueError:
            pass

        user = User.objects(name="doe").first()

        for i in range(int(number)):
            title = self.title()
            content = u''
            for i in range(random.randint(1, 4)):
                content += '<h3>' + self.h3() + '</h3>'
                for paragraph in range(random.randint(1, 4)):
                    content += '<p>' + self.p() + '</p>'
            new_doc = BaseDocument(space=space,
                                   title=title, content=content,
                                   author=user)
            new_doc.save()

    def title(self):
        return self.markov.\
            generate_markov_text(size=random.randint(1, 6)).title()

    def h3(self):
        return self.markov.\
            generate_markov_text(size=random.randint(1, 8)).title()

    def p(self):
        return self.markov.\
            generate_markov_text(size=random.randint(64, 256)).capitalize()
