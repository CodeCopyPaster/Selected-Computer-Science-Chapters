import re
import zipfile


class TextAnalyzer:
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.text = file.read()
        self.output = []

    def lowercase_words_and_punctuation(self):
        '''Print words started with little letter and punctuation marks'''
        words = re.findall(r'\b[a-z]\w*', self.text)
        punctuation = re.findall(r'[^\w\s]', self.text)
        self.output.append(f"Слова с маленькой буквы: {words}, знаки пунктуации: {punctuation}")
        return words, punctuation


    class TextAnalyzer:
        def __init__(self, text):
            self.text = text
            self.output = []

    def is_valid_mac_address(self):
        """Searches and validate MAC"""
        pattern = r'(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}'
        candidates = re.findall(pattern, self.text)
        unique_candidates = set(candidates)
        valid_macs = [mac for mac in unique_candidates if re.fullmatch(pattern, mac)]
        if valid_macs:
            self.output.append(f"Найденные корректные MAC-адреса: {valid_macs}")
        else:
            self.output.append("Корректные MAC-адреса в тексте не найдены.")

        return valid_macs

    def count_consonant_starting_words(self):
        '''Count of words starting with consonant letter'''
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        words = re.findall(r'\b[{}]'.format(consonants), self.text)
        self.output.append(f"Кол-во слов с согласной буквы: {len(words)}")
        return len(words)

    def find_double_letter_words(self):
        '''Finds with 2 same letters and their index'''
        words = re.split(r'\s+', self.text)
        result = []
        for idx, word in enumerate(words, start=1):
            if re.search(r'(.)\1', word):
                result.append((word, idx))
        self.output.append(f"Слова с двумя одинаковыми буквами и их индекс: {result}")
        return result

    def analyze_sentences(self):
        '''Counts an amount of every sentence'''
        questions = len(re.findall(r'\?', self.text))
        dots = len(re.findall(r'\.', self.text))
        exclamations = len(re.findall(r'\!', self.text))
        total = questions + dots + exclamations

        self.output.extend([
            f"Всего предложений: {total}",
            f"Повествовательных: {dots}",
            f"Вопросительных: {questions}",
            f"Побудительных: {exclamations}"
        ])
        return total, dots, questions, exclamations

    def calculate_averages(self):
        '''Counts length of words and sentences'''
        letters = len(re.findall(r'[a-zA-Z]', self.text))
        words = len(re.findall(r'\b[A-Za-z]+\b', self.text))
        sentences = len(re.findall(r'[.!?]', self.text))

        avg_sent_len = letters / sentences if sentences else 0
        avg_word_len = letters / words if words else 0

        self.output.extend([
            f"Средняя длина предложения: {avg_sent_len:.1f}",
            f"Средняя длина слова: {avg_word_len:.1f}"
        ])
        return avg_sent_len, avg_word_len

    def count_smiles(self):
        '''Counts smiles in text'''
        smiles = len(re.findall(r'[\;\:]-*[\(\)\[\]]+', self.text))
        self.output.append(f"Количество смайликов: {smiles}")
        return smiles

    def save_results(self, output_filename='task2output.txt', zip_filename='results.zip'):
        '''Writes results into the file and then saves it in the zip-file'''
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.output))

        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(output_filename)

        return output_filename, zip_filename

    def analyze_all(self):
        '''Starts all the analysis'''
        self.lowercase_words_and_punctuation()
        self.is_valid_mac_address()
        self.count_consonant_starting_words()
        self.count_consonant_starting_words()
        self.analyze_sentences()
        self.calculate_averages()
        self.count_smiles()
        return self.save_results()


def task2():
    analyzer = TextAnalyzer('task2input.txt')
    output_file, zip_file = analyzer.analyze_all()

    print("Анализ завершен. Результаты:")
    print('\n'.join(analyzer.output))
    print(f"\nРезультаты сохранены в {output_file} и заархивированы в {zip_file}")


