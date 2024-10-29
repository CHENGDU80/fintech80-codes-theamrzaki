from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex,SearchableField, SimpleField,SearchField, SearchFieldDataType
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from azure.search.documents.indexes.models import (
    SimpleField,
    SearchFieldDataType,
    SearchableField,
    SearchField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch,
    SearchIndex,
    AzureOpenAIVectorizer
)
from backend.imports import SEARCH_SERVICE_NAME, SEARCH_INDEX_NAME, SEARCH_ADMIN_KEY, SEARCH_ENDPOINT



# Initialize the SearchIndexClient
index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT,
                                  credential=AzureKeyCredential(SEARCH_ADMIN_KEY))
# Initialize Search Client
search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=SEARCH_INDEX_NAME, credential=AzureKeyCredential(SEARCH_ADMIN_KEY))

def create_index():
    try:
        # Configure the vector search configuration  
        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="myHnsw"
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name="myHnswProfile",
                    algorithm_configuration_name="myHnsw",
                    vectorizer="myVectorizer"
                )
            ]
        )

        # Define the index schema
        index = SearchIndex(
            name=SEARCH_INDEX_NAME,
            fields=[
                SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
                SearchableField(name="title", type=SearchFieldDataType.String),
                SearchableField(name="content", type=SearchFieldDataType.String, searchable=True),
                SearchField(name="embedding", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True, vector_search_dimensions=3, vector_search_profile_name="myHnswProfile")           ],
            vector_search=vector_search,
        )
        
      
        result = index_client.create_or_update_index(index)
        print(f' {result.name} created')

        # Create the index
        index_client.delete_index(index)
        print(f"Index Deleted successfully!")
        index_client.create_index(index)
        print(f"Index created successfully!")

        # Fetch documents to ensure they're indexed correctly
        #results = search_client.search(search_text="*", select="id, title, content")
        #for result in results:
        #    print("simple search result:",result)
    except Exception as e:
        print(e)

def index_documents(documents):
    # Upload documents to the index
    result = search_client.upload_documents(documents=documents)
    print(f"Indexed documents: {result}")

def search_documents(search_text):
    try:
        # Perform a search query
        results = search_client.search(search_text)
        
        # Print the number of results found
        print("Processing search results...")

        # Iterate over the results directly
        for result in results:
            # Assuming result is a dictionary, print desired fields
            print(f"ID: {result['id']}, Title: {result['title']}, Content: {result['content']}")

    except Exception as e:
        print(f"An error occurred: {e}")



def search_with_vector(query_embedding):
    vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=3, fields="embedding")
  
    results = search_client.search(  
        search_text="sample",  
        vector_queries= [vector_query],
        select=["title", "content"],
    )  
    
    for result in results:  
        print(f"Title: {result['title']}")  
        print(f"Score: {result['@search.score']}")  
        print(f"Content: {result['content']}")   


if __name__ == "__main__":
    # Create index
    #create_index()
    
    documents = [
        {
            "id": "1",
            "content": "This is a sample document.",
            "title": "Sample Title",
            "embedding": [0.1, 0.2, 0.3]  # Assuming 'embedding' is a Collection field
        },
        {
            "id": "2",
            "content": "Another sample document.",
            "title": "Another Title",
            "embedding": [0.4, 0.5, 0.6]
        }
    ]

    # Index documents
    #index_documents(documents)

    # Example search query
    ##print("Performing search for 'sample':")
    #search_documents("sample")

    # Example vector for searching (replace with actual embedding)
    query_embedding = [0.1, 0.2, 0.3]
    print("Performing vector search:")
    search_with_vector(query_embedding)
