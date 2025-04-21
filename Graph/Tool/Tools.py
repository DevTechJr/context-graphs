from langchain_core.tools import tool
from KG.VectorRAG import query_vector_rag

@tool
def get_vector_response(question,top_k=5):
    """Use this to get vector response from database."""
    Vector_RAG = query_vector_rag(
        question=question, 
        vector_index_name = 'Chunk',
        vector_node_label = 'Chunk',
        vector_source_property= 'text',
        vector_embedding_property = 'textEmbeddingOpenAI',
        )
    return Vector_RAG



