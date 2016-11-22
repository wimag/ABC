
# coding: utf-8

# In[24]:

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument


# In[33]:

RG_DATA = "../../data/researchgate/"
import os
import json
import re
docs = []
i = 0
for dirname, subdirList, fileList in os.walk(RG_DATA):
    for file in fileList:
        with open(os.path.join(dirname, file), 'r') as inp:
            obj = list(json.load(inp).values())[0][0]
        abstract = obj['abstract']
        text = abstract if abstract is not None else obj['title']
        text = re.sub('[^0-9a-zA-Z]+', ' ', text).lower()
        docs.append(TaggedDocument([x for x in text.split() if x.isalpha()], [str(i)]))
        i+= 1


# In[ ]:




# In[35]:

model = Doc2Vec(docs, size=150, window=8, min_count=5, workers=4)


# In[36]:

model.init_sims()


# In[42]:

model.save('../data/sims.bin')


# In[ ]:



