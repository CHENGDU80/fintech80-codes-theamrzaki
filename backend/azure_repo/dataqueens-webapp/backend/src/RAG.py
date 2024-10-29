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


    except Exception as e:
        print(e)

def index_documents(documents):
    # Upload documents to the index
    result = search_client.upload_documents(documents=documents)
    #print(f"Indexed documents: {result}")
    return len(result)

def read_documents():
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
    return documents


def search_with_vector(query_embedding):
    vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=1536, fields="embedding")
    
    names = [
        "auto_make",
        "auto_model",
        "vehicle_maker",
        "vehicle_model",
        "auto_year",
        "vehicle_year",
        "age",
        "sex",
        "education_level",
        "relationship",
        "previous_accidents_injuries",
        "previous_accidents_conditions",
        "previous_accidents_crash_speed",
        "liability_coverage_bodily_injury_liability_per_person",
        "liability_coverage_bodily_injury_liability_per_accident",
        "liability_coverage_property_damage_liability_per_accident",
        "comprehensive_coverage_deductible",
        "collision_coverage_included",
        "collision_coverage_deductible",
        "personal_injury_protection_medical_expenses_limit",
        "personal_injury_protection_lost_wages_limit",
        "underinsured_motorist_coverage_bodily_injury_per_person",
        "underinsured_motorist_coverage_bodily_injury_per_accident",
        "underinsured_motorist_coverage_property_damage_per_accident",
        "underinsured_motorist_coverage_deductible",
        "av_specific_coverage_deductible",
        "premium_details_annual_premium",
        "premium_details_discounts",
        "premium_details_payment_options"
    ]
    results = search_client.search(  
        search_text=None,  
        vector_queries= [vector_query],
        select=names,
        top = 1
    )  
    
    #for result in results:  
    #    print(f"Title: {result['title']}")  
    #    print(f"Score: {result['@search.score']}")  
    #    print(f"Content: {result['content']}")   
    return results



if __name__ == "__main__":
    create_index()

    documents = read_documents()

    index_documents(documents)
