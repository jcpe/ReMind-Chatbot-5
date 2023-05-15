import os
from llama_index import GPTSimpleVectorIndex, download_loader

ReadwiseReader = download_loader("ReadwiseReader")
token = os.getenv("READWISE_API_KEY")
loader = ReadwiseReader(api_key=token)
documents = loader.load_data()
index = GPTSimpleVectorIndex.from_documents(documents)
# save index to disk
index.save_to_disk("readwise.json")
index = GPTSimpleVectorIndex.load_from_disk("readwise.json")
print(index.query("What's the difference between explanation and prediction?"))
