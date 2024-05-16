### Application:

[**RAG Chatbot for Safe Travelling in New York**](https://www.linkedin.com/feed/update/urn:li:activity:7184559186045767680/)

- Ask about the safety of a particular suburb, and the chatbot will provide insights on what to be cautious about.

### Overview:

We have developed a Django project and app to facilitate this functionality. The project can be found [here](https://github.com/Tilemachoc/streetappOpenAI/tree/main/web_proj), with the app nested within it [here](https://github.com/Tilemachoc/streetappOpenAI/tree/main/web_proj/street).

For the database, we utilize MySQL, although you have the flexibility to choose any database through [Django settings](https://github.com/Tilemachoc/streetappOpenAI/blob/main/web_proj/web_proj/settings.py). Our frontend is powered by JavaScript with the addition of Django's template-view features.

### How it Works:

1. **Simplifying Messages:**
   - Send a message with a `top_k` integer (in the video, `top_k=1`). Our model simplifies it into core keywords and specific terms, stripping away unnecessary details.
  
2. **Finding Similarities:**
   - We convert this simplified text into vectors and compare them with our extensive dataset using cosine similarity. The top_k most similar embeddings reveal relevant information.
  
3. **Understanding Context:**
   - Using these embeddings, we provide context to another model, ensuring to adhere to its special tokens and prompt engineering rules.
  
4. **Result:**
   - The model is less likely to hallucinate since we provide it with context. Therefore, it can utilize real, relevant, and new information to generate a response to the user's message.

### Deep Understanding of the Backend:

We begin with a `jsonl` dataset, then create two Django models, [TextDataset and VectorDataset](https://github.com/Tilemachoc/streetappOpenAI/blob/main/web_proj/street/models.py). TextDataset chunks each line of the `jsonl` dataset and VectorDataset vectorizes it. TextDataset contains one column for text and another as a primary key (Django's default), while VectorDataset comprises two columns: original primary key and vector data, where the vector data represents the embeddings of TextDataset.

After migrations and migration, using the command `python manage.py import_jsonl_data.py data.json`, we can add rows to our TextDataset model.

To create the transformed dataset (VectorDataset) from the original TextDataset, substantial work is required. We utilize a custom command called [db_to_vectordb](https://github.com/Tilemachoc/streetappOpenAI/blob/main/web_proj/street/management/commands/db_to_vectordb.py). This command counts the rows in VectorDataset and uses that number as a starting index to avoid vectorizing the same rows. We then employ [generate_embeddings_from_database](https://github.com/Tilemachoc/streetappOpenAI/blob/main/web_proj/street/utils/functions.py), utilizing the `intfloat/e5-large-v2` model to yield embeddings. Before creating a new VectorDataset object, we check if it already exists.

Now that we have rows for both TextDataset and VectorDataset, we use them as context to provide relevant responses to the client's questions:

1. We simplify the text of the client's question to retain only relevant keywords and remove unnecessary details.
2. We then compare the vector of the simplified text with every row of VectorDataset using cosine similarity and return the top_k most relevant results.
3. Since the primary key of VectorDataset is the same as that of TextDataset, we can access the original text using that primary key. We feed this text to OpenAI's GPT-3.5 in the [get_response function](https://github.com/Tilemachoc/streetappOpenAI/blob/main/web_proj/street/utils/functions.py).
