
from sentence_transformers import SentenceTransformer
from ..models import TextDataset,VectorDataset
from typing import List
import logging
import numpy as np
from .my_config import model7, tokenizer7, model7x8, tokenizer7x8


def logging_variable(name,variable):
    logging.basicConfig(filename="variable_logs.log", level=logging.DEBUG)
    logging.info("%s= %s" % (name,variable))


def logging_function(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            with open(filename, 'a') as f:
                f.write(f"Function '{func.__name__}' returned: {result}\n")
            
            return result
        
        return wrapper
    
    return decorator


@logging_function("function_logs.log")
def generate_embeddings_from_database(start_idx: int,database_model=TextDataset):
    model = SentenceTransformer('intfloat/e5-large-v2')

    articles = database_model.objects.values_list('text', flat=True)


    for article in articles[start_idx:]:
        input_text = "passage: " + article

        embeddings = model.encode(input_text, normalize_embeddings=True, convert_to_numpy=True)
        yield embeddings


@logging_function("function_logs.log")
def simplify_text(message):
    instructions = "<s>[INST]:\nGiven a user's question, extract and list only the most relevant keywords and specific terms that define the core subject or intention of the query. Remove all filler words, general inquiries, and unnecessary details to simplify the question to its essence, focusing on actions, product names, or specific features involved.[/INST] "
    text = instructions + message

    inputs = tokenizer7(text, return_tensors='pt')
    outputs = model7.generate(**inputs, max_new_tokens=256)

    answer = tokenizer7.decode(outputs[0], skip_special_tokens=True)
    return answer


@logging_function("function_logs.log")
def cosine_compare(q_vector,vectordataset_rows, top_k):
    similarities = []
    logging_variable("q_vector",q_vector)
    logging_variable("q_vector.T",q_vector.T)
    query_norm = np.linalg.norm(q_vector)
    logging_variable("query_norm",query_norm)
    
    for vd_row in vectordataset_rows:
        vd_vector = vd_row.get_vector_data()
        logging_variable("vd_vector",vd_vector)
        dot_product = np.dot(vd_vector, q_vector.T)
        logging_variable("dot_product",dot_product)
        embedding_norm = np.linalg.norm(vd_vector)
        cosine_similarity = dot_product / (embedding_norm * query_norm)
        similarities.append([vd_row.pk,cosine_similarity])
    
    similarities.sort(key=lambda x: x[1], reverse=True)

    closest_k = similarities[:top_k]
    
    return closest_k


@logging_function("function_logs.log")
def get_response(message: str, list_ids: List):
    #If i wasn't using openai api, this would be the format of context: https://youtu.be/biJmRQF8bmY?si=jY0KjHsGpRKcAUDx&t=1370
    context = "<s>[INS]Method: rag_context\nPrompt: <context>\n"

    textdataset_list = TextDataset.objects.filter(pk__in=list_ids)

    for i,td_row in enumerate(textdataset_list, start=1):
        td_text = td_row.text
        context += f"<Section_{i}>\n"
        context += td_text
        context += f"\n</Section_{i}>\n"
    context += "</context>\nIn answering the following question, you may choose - if appropriate - to make use of the above context:[/INT]"

    text = context + f"\n{message}"

    inputs = tokenizer7x8(text, return_tensors='pt')
    outputs = model7x8.generate(**inputs, max_new_tokens=256)

    answer = tokenizer7x8.decode(outputs[0], skip_special_tokens=True)
    return answer


@logging_function("function_logs.log")
def generate_response(message: str, top_k=1):
    model = SentenceTransformer('intfloat/e5-large-v2')

    simplified_message = simplify_text(message)
    query_message = "query: " + simplified_message
    vector_message = model.encode(query_message, normalize_embeddings=True, convert_to_numpy=True)

    all_vector_rows = VectorDataset.objects.all()

    topk_list = cosine_compare(vector_message,all_vector_rows, top_k)
    topk_ids = [item[0] for item in topk_list]

    gpt_response = get_response(message,topk_ids)

    rows_used = "For the following response, these rows were used: "
    for id in topk_ids:
        id = int(id)
        rows_used += f"{id},"

    OUTGOING_MESSAGE = rows_used[:-1] + "\n\n" + gpt_response

    return {"message": OUTGOING_MESSAGE}