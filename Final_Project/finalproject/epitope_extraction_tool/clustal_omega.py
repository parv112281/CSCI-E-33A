from datetime import datetime
import subprocess
import os, re

PROJECT_PATH = os.path.join(os.path.abspath(""), "epitope_extraction_tool/")
CLUSTAL_OMEGA_LOCATION = os.path.join(PROJECT_PATH, "clustal/clustal")
TMP_DIR_PATH = os.path.join(PROJECT_PATH, "tmp/")

def align_sequences(sequences):
    if not os.path.exists(TMP_DIR_PATH):
        os.mkdir(TMP_DIR_PATH)

    temp_file = f'{TMP_DIR_PATH}{datetime.now().strftime("%m%d%Y_%H%M%S")}.fasta'

    with open(temp_file, "w") as seq_file:
        seq_file.write(sequences)
    
    cmd = [CLUSTAL_OMEGA_LOCATION, "-i", temp_file, "--outfmt=fasta"]

    try:
        result = subprocess.run(cmd, capture_output=True).stdout.decode("utf-8")
    except Exception as e:
        result = f"Error: {e}"

    if os.path.exists(temp_file):
        os.remove (temp_file)

    return result


def create_fasta_string(sequences):
    curr_seq_number = 1
    fasta_str = ""
    for sequence in sequences:
        if sequence is not None and sequence != "":
            fasta_str += f">seq{curr_seq_number}\n"
            fasta_str += sequence + "\n"
            curr_seq_number += 1
    return fasta_str
    


def extract_sequences_from_fasta(fasta_string):
    return re.split(">seq\d+", re.sub("\s+", "", fasta_string))[1:]


def remap_epitopes(epitopes, aligned_sequences):
    new_epitopes = []
    for i in range(len(aligned_sequences)):
        curr_new_epitopes = []
        epitopes_ptr = 0
        residue_pos = 1
        curr_sequence = aligned_sequences[i]
        curr_epitopes = epitopes[i]

        for j in range(len(curr_sequence)):
            if len(curr_epitopes) <= 0:
                break
            if curr_sequence[j] == "-":
                continue
            if residue_pos == curr_epitopes[epitopes_ptr]:
                curr_new_epitopes.append(j+1)
                epitopes_ptr += 1
                if (epitopes_ptr >= len(curr_epitopes)):
                    break
            residue_pos += 1
        new_epitopes.append(curr_new_epitopes)
    return new_epitopes
