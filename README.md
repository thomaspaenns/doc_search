# MSCI-541

Thomas Enns

This repository consists of 11 programs which work together to create then query an index of files, then to evaluate search results and performance.

The first, IndexEngine.py, accepts two arguments: the filepath to latimes.gz, and the filepath to a folder that will be created and will house all the files/documents. The program will split the gzip into the approx. 131 000 files, create an inverted index of each token (word) present linked to all the docs in which it appears, store the index, store their metadata, and store the files in the specified folder, divided by date.  An example of the appropriate way to run this program from the console is as follows:
python IndexEngine.py C:\Users\thoma\Documents\3Bterm\MSCI541\latimes.gz C:\Users\thoma\Documents\3Bterm\MSCI541\testdir

The second, GetDoc.py, accepts three arguments: the filepath to the document store, the type of identifier used to request a document (either DOCNO or doc id), and the identifier itself. The program will then return the corresponding document along with it's metadata to the console. An example of the appropriate way to run this program from the console is as follows:
python GetDoc.py C:\Users\thoma\Documents\3Bterm\MSCI541\testdirectory docno LA123190-0134

The third, BooleanAND.py, accepts three arguments: the location of the index file, the name of a query input file, and the name of a query output file. The program will parse and tokenize the queries and print the list of documents containing all the query terms in the output file. An example of the appropriate way to run this program from the console is as follows:
python BooleanAND.py C:\Users\thoma\Documents\3Bterm\MSCI541\testdir queries.txt hw2-results-tenns.txt

The fourth program, Helper.py, is not meant to be run. It only contains methods that can be used by the other programs such as a tokenizer and a method to convert tokens to ids. The tokenizer is used by both the InvertedIndex program and all querying programs. It has an option to use the stemmer or not.

The fifth program, Evaluate.py, accepts two arguments: the name of the .txt file of relevance judgements for the queries and the name of the run file with the results of the queries. It computes effectiveness measures for each query and outputs them to both a .txt and a .csv in the measures folder. An example of the appropriate way to run this program from the console is as follows:
python Evaluate.py LA-only.trec8-401.450.minus416-423-437-444-447.txt hw4-bm25-stem-tenns.txt

The sixth program, Summarize.py, accepts no arguments. It iterates over all the results files created by the Evaluate program and outputs a table of the average performance metrics for each run file. An example of the appropriate way to run this program from the console is as follows:
python Summarize.py

The seventh program, compare.py, accepts three arguments, the names of the two .csv files created by the Evaluate program which the user wishes to compare, and a number corresponding to the desired metric 1-MAP. 2-AP@10, 3-Mean NDCG@10, 4-Mean NDCG@1000, 5-Mean TBG. The program outputs a simple .csv file with the desired metric for each run, the percent improvement of the better performing run over the worse performing run, and the p-value. An example of the appropriate way to run this program from the console is as follows:
python compare.py hw4-bm25-baseline-tenns-measures.csv hw4-bm25-stem-tenns-measures.csv 1

The 8th program, Calc.py, accepts no arguments, and simply computes the number of words in collection, number of non-zero instances of terms in documents, and the average document length in collection. It outputs these to the console. (This was used for Q5 and for avg doc length for BM25) An example of the appropriate way to run this program from the console is as follows:
python Calc.py

The ninth program BM25.py, accepts three arguments: the location of the index file, the name of a query input file, and the name of a query output file. The program will parse and tokenize the queries and print the list of the top 1000 ranking documents according to the BM25 equation in the output file. An example of the appropriate way to run this program from the console is as follows: 
python BM25.py C:\Users\thoma\Documents\3Bterm\MSCI541\testdirS queries.txt hw4-bm25-stem-tenns.txt

The tenth program, docIndex.py, accepts one argument, the location of the gzip file containing the documents. The program will esentially only parse the documents to create an index which maps from the docno to the text of each document and then save that index as a pickle file. An example of the appropriate way to run this program from the console is as follows:
python docIndex.py C:\Users\thoma\Documents\3Bterm\MSCI541\latimes.gz 

The eleventh program hw-5-tenns.ipynb, is essentially to re-rank the top 100 results from the BM25 run file using the monoBERT machine learning algorith. It has a number of codeblocks that can be run sequencially. The ones with reference to github can be ignored



