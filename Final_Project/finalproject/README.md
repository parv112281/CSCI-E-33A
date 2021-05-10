# Epitope Extraction Tool v1

## The inspiration for this tool
The purpose of this tool is to be able to extract claimed epitopes from patent documents along with the associated seq id. The tool will then use multiple sequence alignment to align the seq id's from each patent and display in a visualization. This will allow patent lawyers or researchers to quickly visualize protected regions of a protein or visualize hot spots on the protein where there seems to be a lot research. 

This is a simplified version of the app I've been working on with others called OpenPSV: https://main.d3nuz0k9umkypw.amplifyapp.com/. OpenPSV itself is implemented mostly in node express with the text analytics in python. It uses aws lambda functions for most of the compute needs. For this application, I implemented a backend in Django, which does not exist in OpenPSV since we use amplify which provides basic backend and CRUD functionality for free. 

Another key difference is that for OpenPSV we use USPTO data bulk downloaded in xml form to an S3 bucket, whereas this tool pulls the needed data from google patents and parses it using BeautifulSoup. The parsed data is then persisted to postgres for subsequent requests for the same patent. In addition, this tool uses an off the shelf msa viewer, https://github.com/plotly/react-msa-viewer, to visualize the sequence information, whereas OpenPSV implemented it's own visualization tools using Ant Design. 

The key benefit for reimplementing this in Django is that it gives me a platform independent implementation that I can work on post this semester.

## Explanation of files and folders

### models.py
Contains three models for patents, sequences and epitopes. A single patent can contain multiples sequences and epitopes.

### patent.py
Provides functionality for fetching patent information from google patents and extract the epitope information from the claims section. 

### seqlisting.py
Provides functionality for extracting sequences from an USPTO dataset hosted in an S3 bucket. This dataset is transient and will probably not exist far beyond the end of this semester since it's expensive to maintain.

### clustal_omega.py:
Provides the sequence alignment functionality, using clustal omega binary.

### clustal folder: 
This folder contains two binaries of the clustal omega program, one is for use locally on a mac and the other is for use in docker which uses linux.


## Work Completed
For this implementation, I'm using regular expressions pulled from OpenPSV for the epitope extraction part. The regular expressions are currently not very flexible and do not generalize well to other patents. 

For the sequence alignment, I'm using the Clustal Omega binary to perform the actual alignment and implemented a simple algorithm to remap the epitopes from the original sequence to the aligned sequence. This part works pretty well and probably needs no further work.

The multiple sequence alignment viewer is an existing open source component that I added a custom color scheme class with a simple algorithm to assign background colors to only epitopes in the sequence.

## Work remaining
The regex in the patent extraction part needs some work and an alternative strategy is needed to extract this information. 

The msa viewer could be improved considerably for ease of use and functionality. Currently the user has to scroll quite a bit in order to view all the epitopes and there are no visible scroll bars, user has to drag the sequences left and right.

## SetUp
This application has been dockerized and can be set up relatively easily. In order to start up, just run `docker-compose up`. This starts up a postgres container and a web container for the actual application. The user should then just need to navigate to the `127.0.0.1:8000` in their browser to bring up the app. The patend ids textbox has been pre-populated with several patents for PCSK9, these can be replaced with others if the user has some they wish to examine. 

Click the submit button to start the process, this could take up to a couple minutes as the information is extracted and aligned if this is the first time using the patents. The information from the patents is persisted, therefore subsequent runs with the same patents is much faster. After the patents have been processed, the msa viewer should appear with the aligned sequences and the epitopes in a colored background. 

The viewer can be used to navigate the sequences by dragging them left or right. There is also a back button on the top left to go back to the patent id entry screen.