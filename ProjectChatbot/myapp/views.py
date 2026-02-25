import faiss
import numpy as np
import os
from django.http import JsonResponse
from django.shortcuts import render
from langchain_community.embeddings import OllamaEmbeddings
from dotenv import load_dotenv
from groq import Groq
import pickle

# Load environment variables
load_dotenv()

# Initialize Groq API
llm = Groq(api_key=os.getenv("GROQ_API_KEY"))


##############################################################

# Load FAISS index
# index = faiss.read_index("faiss_index_ivf_trained.bin")

# # Load the embedding model (only once)
# embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# # Load the preprocessed document chunks
# import pickle
# with open("split_docs.pkl", "rb") as f:
#     split_docs = pickle.load(f)



# def chatbot_view(request):
#     if request.method == "POST":
#         user_message = request.POST.get("message")

#         if user_message:
#             # Convert query to embedding
#             query_embedding = np.array([embedding_model.embed_query(user_message)], dtype=np.float32)

#             # Perform FAISS search (top 3 chunks)
#             k = 3  # Get top 3 matching chunks
#             distances, indices = index.search(query_embedding, k)

#             # Retrieve the top 3 matching chunks
#             top_chunks = [split_docs[idx].page_content for idx in indices[0] if idx != -1]  # Avoid invalid indices
            
#             # Combine the top chunks into a single context
#             combined_context = "\n\n".join(top_chunks)
#             print(combined_context)

#             # Generate a response using Groq API
#             final_prompt = f"Answer the following question based on the provided context.\n\nContext: {combined_context}\n\nQuestion: {user_message}\n\nAnswer:"

#             llm_response = llm.chat.completions.create(
#                 messages=[{"role": "user", "content": final_prompt}],
#                 model="llama-3.3-70b-versatile",
#             )

#             # Extract the response
#             bot_response = llm_response.choices[0].message.content

#             return JsonResponse({"response": bot_response})

#     return render(request, "interface.html")

#################################################################


# Load FAISS index
index = faiss.read_index("final_faiss_index_ivf_trained.bin")

# Load split_docs from file
with open("final_split_docs.pkl", "rb") as f:
    split_docs = pickle.load(f)

# Load embedding model
embedding_model = OllamaEmbeddings(model="nomic-embed-text")


def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message")

        if user_message:
            # Convert query to embedding
            query_embedding = np.array([embedding_model.embed_query(user_message)], dtype=np.float32)

            # Perform FAISS search (retrieve top 3 chunks)
            k = 5  
            distances, indices = index.search(query_embedding, k)

            # Retrieve the top 3 matching chunks
            top_chunks = [split_docs[idx].page_content for idx in indices[0] if idx != -1]
            combined_context = "\n\n".join(top_chunks)

            print("Retrieved Context:\n", combined_context)

            # Generate response using Groq API
            final_prompt = f"You are a friendly and knowledgeable AI assistant for Academia International College.Use the following context to answer the user's question in a natural and conversational way.If the context does not contain enough information never say things like The context does not mention or I recommend checking their website. Always respond as if you are directly chatting with the user, not summarizing a document.Be concise, polite, and sound human — not robotic and provide short answer as much as possible.Context: {combined_context}\n\nQuestion: {user_message}\n\nAnswer:"

            llm_response = llm.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}],
                model="llama-3.3-70b-versatile",
            )

            # Extract chatbot response
            bot_response = llm_response.choices[0].message.content

            return JsonResponse({"response": bot_response})

    return render(request, "interface.html")
