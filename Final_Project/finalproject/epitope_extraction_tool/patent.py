from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import re

class PatentExtractor:
    def __init__(self, patent_id):
        self.url = f'https://patents.google.com/patent/{patent_id}'
        self.patent_id = patent_id
        self.__fetch_patent()


    def __fetch_patent(self):
        request = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(request).read()
        self.soup = BeautifulSoup(page, features="lxml")

        raw_claims = self.soup.find('section', itemprop='claims').get_text()
        self.claims_text = [claim.strip() for claim in raw_claims.split('\n') if claim.strip() != '']
        self.__extract_epitopes()

    
    def __extract_epitopes(self):
        patterns = [
            r'''([^.]*?antibody(.*)binds(.*)residues[^.]*\.)''',
            r'''([^.]*?antibody(.*)binds(.*)residue[^.]*\.)''',
            r'((epitope[s\s])(.{0,250})(residue[s|\s])(.{0,250})(([A-Z][0-9]{1,5})+(,|and|to|\s?)?([A-Z][0-9]{1,5})?)+(.{0,30})(SEQ ID NO:\s?([0-9])))',
            r'((bind[s\s])(.{0,250})(residue[s|\s])(.{0,250})(([A-Z][0-9]{1,5})+(,|and|to|\s?)?([A-Z][0-9]{1,5})?)+(.{0,30})(SEQ ID NO:\s?([0-9])))',
            r'((bind[s\s])(.{0,250})(residue[s|\s])(.{0,250})(([A-Z]?[0-9]{1,5})+(,|and|to|\s|-)?([A-Z]?[0-9]{1,5})?)+(.{0,30})(SEQ ID NO:\s?([0-9])))'
        ]

        claims = {}

        for claim in self.claims_text:
            sentences = sent_tokenize(claim)
            for sentence in sentences:
                for pattern in patterns:
                    match = re.search(pattern, sentence)
                    if match:
                        full_match = match.group(0)
                        seq_id_regex = r'(SEQ ID NO[:]?\s?)([0-9]{1,5})'
                        matching_seq_id_no = re.search(
                            seq_id_regex, sentence).group(2)
                        if matching_seq_id_no not in claims:
                            claims[matching_seq_id_no] = set()
                        epitope_seq_ranges = [r'([A-Z])?([0-9]{1,5})(-|([\s]?to[\s]?))([A-Z])?([0-9]{1,5})',
                                          r'(between\s)([A-Z])?([0-9]{1,5})\s(and)\s([A-Z])?([0-9]{1,5})',
                                          r'(from\s)([A-Z])?([0-9]{1,5})\s(to)\s([A-Z])?([0-9]{1,5})'
                                        ]
                        epitope_numbers_statements = [
                            r'\s([A-Z])?([0-9]{1,5})(\s|,|and)?([A-Z])?([0-9]{1,5})?(?=.*SEQ)']
                        for range_regex in epitope_seq_ranges:
                            ranges = re.search(range_regex, full_match)
                            if ranges == None:
                                continue
                            for val in range(int(ranges.group(2)), int(ranges.group(6))):
                                claims[matching_seq_id_no].add(val)

                        for epitope_numbers_regex in epitope_numbers_statements:
                            for num in re.finditer(epitope_numbers_regex, full_match):
                                claims[matching_seq_id_no].add(int(num.group(2)))
                        
        self.claims = claims
                            


