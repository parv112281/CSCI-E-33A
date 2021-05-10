from .seqlisting import SeqListing
from .patent import PatentExtractor
from .models import Patent, Sequence, Epitope
import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .clustal_omega import * 

# Create your views here.
def index(request):
    return render(request, "pages/index.html")

@csrf_exempt
def upload(request):
    if request.method == "POST":
        #try:
            patent_ids_str = json.loads(request.body)['patentIds']
            patent_ids = [id.strip() for id in patent_ids_str.split(',')]
            result_set = {}

            result_set = create_result_set(patent_ids)        

            aligned_seq, remapped_epitopes = perform_sequence_alignment(result_set)

            index = 0
            for key in result_set:
                result_set[key]["sequences"] = aligned_seq[index]
                result_set[key]["epitopes"] = remapped_epitopes[index]
                index += 1

            return JsonResponse({"message": result_set}, status=200)
        #except Exception as e:
            #return JsonResponse({"message": e.__str__()}, status=500)
    return JsonResponse({"message": "POST request required"}, status=400)

def perform_sequence_alignment(result_set):
    fasta_str = create_fasta_string([result_set[key]['sequences'] for key in result_set])
    aligned_fasta_str = align_sequences(fasta_str)
    aligned_seq = extract_sequences_from_fasta(aligned_fasta_str)
    epitopes = [result_set[key]['epitopes'] for key in result_set]
    remapped_epitopes = remap_epitopes(epitopes, aligned_seq)
    return aligned_seq,remapped_epitopes

def create_result_set(patent_ids):
    result_set = {}
    for id in patent_ids:
        patent = Patent.objects.filter(patent_id=id).first()
        if patent is None:    
            extract_patent_info(result_set, id)
        else:
            fill_patent_info(result_set, patent)
    return result_set

def extract_patent_info(result_set, id):
    patent = PatentExtractor(id)
    labels = [f"{id}_{seq_id}" for seq_id in patent.claims]
    epitopes = [sorted(patent.claims[seq_id]) for seq_id in patent.claims]
    all_sequences = SeqListing(id).sequences
    sequences = [all_sequences[int(seq_id) - 1] for seq_id in patent.claims]

    pat_model = Patent.objects.create(patent_id=id)
    pat_model.save()
    for seq_id in patent.claims:
        seq = Sequence.objects.create(seq_id=seq_id, 
                                    sequence=all_sequences[int(seq_id) - 1],
                                    patent=pat_model)
        seq.save()
    for epitope in epitopes:
        epi = Epitope.objects.create(epitope=",".join([str(epi) for epi in epitope]), patent=pat_model)
        epi.save()
    index = 0
    for label in labels:
        result_set[label] = {}
        result_set[label]['epitopes'] = epitopes[index]
        result_set[label]['sequences'] = sequences[index]
        index += 1

def fill_patent_info(result_set, patent):
    labels = [f"{patent.patent_id}_{sequence.seq_id}" for sequence in patent.sequences.all()]
    epitopes = []
    for epitope_model in patent.epitopes.all():
        epi_str = epitope_model.epitope.split(",")
        epitopes.append([int(pos) for pos in epi_str])

    sequences = patent.sequences.all()
    index = 0
    for label in labels:
        result_set[label] = {}
        result_set[label]['epitopes'] = epitopes[index]
        result_set[label]['sequences'] = sequences[index].sequence
        index += 1
    


