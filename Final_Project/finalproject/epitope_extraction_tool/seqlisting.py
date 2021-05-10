import re
import xml.etree.ElementTree as et
from string import digits
import requests
import os

PROJECT_PATH = os.path.join(os.path.abspath(""), "epitope_extraction_tool/")
LISTINGS_BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/seq/'
TMP_DIR_PATH = os.path.join(PROJECT_PATH, "tmp/")

def find_all(tree, element):
    elems = tree.findall(element)
    res = []
    for elem in elems:
        res.append(elem.text)
    return res


class SeqListing:
    def __init__(self, patent_id):
        self.patent_id = patent_id
        self.__process_listings_xml()
        
    def __process_listings_xml(self):
        fname = self.patent_id + '.xml'
        resp = requests.get(LISTINGS_BASE_URL + fname)
        with open(TMP_DIR_PATH + fname, 'wb') as f:
            f.write(resp.content)

        tree = et.parse(TMP_DIR_PATH + fname)
        root = tree.getroot()
        sequences_raw = find_all(root, './/s400')
        self.sequences = []
        for seq in sequences_raw:
            remove_digits = str.maketrans('', '', digits)
            sequence = seq.translate(remove_digits)
            sequence = sequence.replace(" ", "")
            self.sequences.append(self.convert_three_one(sequence))

        # try parsing the new seq_listing format
        if(len(self.sequences) == 0):
            entries = find_all(root, './/entry')
            full_table_text = ''
            for entry in entries:
                if entry != None:
                    full_table_text += entry
            
            # split by the 210 to segments
            segments = full_table_text.split('<210>')

            for segment in segments:
                txt = re.findall(r"(?:SEQUENCE:)([\s\w\W]+)", segment)                                
                if len(txt) == 0:
                    continue
                full_seq = ''
                for seq in txt:
                    full_seq+=seq

                remove_digits = str.maketrans('', '', digits)
                sequence = full_seq.translate(remove_digits)
                sequence = sequence.replace(" ", "")
                self.sequences.append(self.convert_three_one(sequence))

    def convert_three_one(self, sequence):
        sequence = sequence.replace("Ala", "A")
        sequence = sequence.replace("Asx", "B")
        sequence = sequence.replace("Cys", "C")
        sequence = sequence.replace("Asp", "D")
        sequence = sequence.replace("Glu", "E")
        sequence = sequence.replace("Phe", "F")
        sequence = sequence.replace("Gly", "G")
        sequence = sequence.replace("His", "H")
        sequence = sequence.replace("Ile", "I")
        sequence = sequence.replace("Lys", "K")
        sequence = sequence.replace("Leu", "L")
        sequence = sequence.replace("Met", "M")
        sequence = sequence.replace("Asn", "N")
        sequence = sequence.replace("Pro", "P")
        sequence = sequence.replace("Gln", "Q")
        sequence = sequence.replace("Arg", "R")
        sequence = sequence.replace("Ser", "S")
        sequence = sequence.replace("Thr", "T")
        sequence = sequence.replace("Val", "V")
        sequence = sequence.replace("Trp", "W")
        sequence = sequence.replace("Xaa", "X")
        sequence = sequence.replace("Tyr", "Y")
        sequence = sequence.replace("Glx", "Z")
        return sequence
