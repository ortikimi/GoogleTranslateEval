import csv
import matplotlib.pyplot as plt

class SpredSheetResults():

    def __init__(self):
        self.google_evaluator = []
        self.gold_evaluator = []
        self.bleu_1gram = []
        self.bleu_2gram = []

    def write_spreadsheet(self, results):
        self.file_name = 'translated' + self.source_language + '.csv'
        with open(self.file_name, encoding='utf-16', mode='w') as lang_file:
            results_writer = csv.writer(lang_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            results_writer.writerow(['Original Sentence', 'Translated Sentence', 'Gold translated Sentence',
                                      'Hebrew Tagging', 'English Tagging', 'Google Evaluation Result',
                                      'Gold Evaluation Result' 'Bleu Result 1 ngram', 'Bleu Result 2 ngram'])
            for r in results:
                results_writer.writerow([r.original_sentence, r.translated_sentence, r.gold_sentence,
                                         r.hebrew_tag, r.english_tag, r.score, r,gold_score,
                                         r.bleu_1ngram_score, r.bleu_2ngram_score])

    def get_data_from_csv(self):
        with open(self.file_name, encoding='utf-16', mode='r') as csvfile:
            plots = list(csv.reader(csvfile, delimiter='\t'))
            for row in plots:
                if len(row) > 0:
                    try:
                        self.google_evaluator.append(float(row[5]))
                        self.gold_evaluator.append(float(row[6]))
                        self.bleu_1gram.append(float(row[7]))
                        self.bleu_2gram.append(float(row[8]))
                    except ValueError:
                        print()

    def draw_graph(self):
        self.get_data_from_csv()
        self.draw_comparison_graph()
        self.draw_gold_graph()

    def draw_comparison_graph(self):
        # Plot the data
        plt.plot(self.google_evaluator, label='Google Evaluator')
        plt.plot(self.bleu_1gram,  label='Bleu 1-ngram')
        plt.plot(self.bleu_2gram,  label='Bleu 2-ngram')

        # Add a legend
        plt.legend()
        plt.title('Compare between Bleu and Google Evaluator')
        plt.xlabel('Sentences')
        plt.ylabel('Evaluation')
        plt.show()

    def draw_gold_graph(self, file_name):
        # Plot the data
        plt.plot(self.gold_evaluator, label='Gold Evaluator')

        # Add a legend
        plt.legend()
        plt.title('Compare between Bleu and Google Evaluator')
        plt.xlabel('Sentences')
        plt.ylabel('Evaluation')
        plt.show()