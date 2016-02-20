BigramStrength

This directory contains the scripts for deriving bigram collocation strength values for the bigrams in the Dissertation Experiment 1 recall study stimuli. 

I will derive collocation strength values from two sources: 

1) The spoken portion of the OpenANC corpus (Switchboard and Charlotte)
      Switchboard    telephone conversation   2,307 files    3,019,477 words
      Charlotte	     face to face conversation	    93 files 198,295  words		 
Ide, Nancy, and Suderman, Keith (2007). The Open American National Corpus (OANC). http://www.AmericanNationalCorpus.org/OANC

2) The entire Santa Barbara Corpus of Spoken American English (about 200,000 words), words extracted from the version in: /Users/heathersimpson/Documents/Corpora/SB_Corpus/CleanedText  (still needs a little cleanup though, some Turns are just a ( and there are a few timestamps left in there)

Switchboard has turns separated on each line, SBC has turns separated, Charlotte has a lot of narratives, and seems to have sentences on each line.

I will create a set of bigrams for each corpus

I will derive association strength for each word pair in the stimuli words separately

There may be some overlap, so it would overall be faster to do each as a set, but 

