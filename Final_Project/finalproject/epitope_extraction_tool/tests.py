from django.test import TestCase
from .clustal_omega import *

class SequenceAlignmentTestCase(TestCase):

    def setUp(self):
        pass

    def test_simple_sequence_alignment(self):
        sequences = ">seq1\nACDEFGHIKLMNPQRSTVWY\n>seq2\nXXXXACDEFGHIMNXXXPQR\n>seq3\nACDEFGHILMNXXXXXPQRS\n>seq4\nXXXACDEFGHIKLMNPQRST"
        expected_result = b">seq1\n----ACDEFGHIKLM----NPQRSTVWY\n>seq2\nXXXXACDEFGHIMNXXXP---QR-----\n>seq3\n----ACDEFGHILMNXXXXXPQRS----\n>seq4\n-XXXACDEFGHIKLM----NPQRST---\n"
        
        aligned_sequences = align_sequences(sequences)

        self.assertEqual(expected_result, aligned_sequences)


    def test_create_fasta_string(self):
        sequences = ["ACDEFGHIKLMNPQRSTVWY", "XXXXACDEFGHIMNXXXPQR", "ACDEFGHILMNXXXXXPQRS", "XXXACDEFGHIKLMNPQRST"]
        expected_result = ">seq1\nACDEFGHIKLMNPQRSTVWY\n>seq2\nXXXXACDEFGHIMNXXXPQR\n>seq3\nACDEFGHILMNXXXXXPQRS\n>seq4\nXXXACDEFGHIKLMNPQRST\n"
        fasta_str = create_fasta_string(sequences)
        self.assertEqual(expected_result, fasta_str)


    def test_extract_sequences_from_fasta(self):
        fasta_str = ">seq1\nACDEFGHIKLMNPQRSTVWY\n>seq2\nXXXXACDEFGHIMNXXXPQR\n>seq3\nACDEFGHILMNXXXXXPQRS\n>seq4\nXXXACDEFGHIKLMNPQRST"
        expected_result = ["ACDEFGHIKLMNPQRSTVWY", "XXXXACDEFGHIMNXXXPQR", "ACDEFGHILMNXXXXXPQRS", "XXXACDEFGHIKLMNPQRST"]

        sequences = extract_sequences_from_fasta(fasta_str)

        self.assertEqual(expected_result, sequences)

    
    def test_remap_epitopes(self):
        epitopes = [[1,2,10], [5,7,20], [43], []]
        aligned_sequences = ["----ACDEFGHIKLM----NPQRSTVWY", "XXXXACDEFGHIMNXXXP---QR-----", "----ACDEFGHILMNXXXXXPQRS----", "-XXXACDEFGHIKLM----NPQRST---"]

        expected_results = [[5,6,14], [5,7,23], [], []]

        remapped_epitopes = remap_epitopes(epitopes, aligned_sequences)
        self.assertEqual(expected_results, remapped_epitopes)