import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from spacy.util import filter_spans
import json

def clean_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
        
        training_data = {'classes' : ['MEDICINE', "MEDICALCONDITION", "PATHOGEN"], 'annotations' : []}
        for example in data['examples']:
            temp_dict = {}
            temp_dict['text'] = example['content']
            temp_dict['entities'] = []
            for annotation in example['annotations']:
                start = annotation['start']
                end = annotation['end']
                label = annotation['tag_name'].upper()
                temp_dict['entities'].append((start, end, label))
            training_data['annotations'].append(temp_dict)
        return training_data


def create_dataset(training_data, nlp, doc_bin):
    for training_example in tqdm(training_data['annotations']): 
        text = training_example['text']
        labels = training_example['entities']
        doc = nlp.make_doc(text) 
        ents = []
        for start, end, label in labels:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        filtered_ents = filter_spans(ents)
        doc.ents = filtered_ents 
        doc_bin.add(doc)

    doc_bin.to_disk("training_data.spacy")


def main():
    nlp = spacy.blank("en")
    doc_bin = DocBin()
    data = clean_data()
    create_dataset(data, nlp, doc_bin)


if __name__ == '__main__':
    main()