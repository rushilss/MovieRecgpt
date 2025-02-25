import pandas as pd
import ast  # For safely evaluating strings as Python objects
import requests  # For making API calls
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
openai_api_key = os.getenv("OPENAI_API_KEY")
utelly_api_key = os.getenv("UTELLY_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# Load the CSV file
df = pd.read_csv("top250_movies_filtered.csv")

# Combine relevant columns into a single text representation for each movie
df["combined_text"] = (
    "Title: " + df["primaryTitle"] + "\n" +
    "Original Title: " + df["originalTitle"] + "\n" +
    "Description: " + df["description"] + "\n" +
    "Content Rating: " + df["contentRating"] + "\n" +
    "Release Year: " + df["startYear"].astype(str) + "\n" +
    "Genres: " + df["genres"].apply(lambda x: ", ".join(ast.literal_eval(x)) if pd.notna(x) else "") + "\n" +
    "Production Companies: " + df["productionCompanies"].apply(
        lambda x: ", ".join([comp["name"] for comp in ast.literal_eval(x)]) if pd.notna(x) else "") + "\n" +
    "Countries of Origin: " + df["countriesOfOrigin"].apply(lambda x: ", ".join(ast.literal_eval(x)) if pd.notna(x) else "") + "\n" +
    "Languages: " + df["spokenLanguages"].apply(lambda x: ", ".join(ast.literal_eval(x)) if pd.notna(x) else "") + "\n" +
    "Filming Locations: " + df["filmingLocations"].fillna("") + "\n" +
    "Budget: $" + df["budget"].astype(str) + "\n" +
    "Gross Worldwide: $" + df["grossWorldwide"].astype(str) + "\n" +
    "Runtime: " + df["runtimeMinutes"].astype(str) + " minutes\n" +
    "Average Rating: " + df["averageRating"].astype(str) + "\n" +
    "Number of Votes: " + df["numVotes"].astype(str)
)

# Convert the combined text column to a list of strings
texts = df["combined_text"].tolist()

# Ensure all items in `texts` are strings
texts = [str(text) if text is not None else "" for text in texts]

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = langchain_api_key
os.environ['USER_AGENT'] = 'myagent'

# Initialize OpenAI embeddings and LLM
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create embeddings for the combined text
vector_store = FAISS.from_texts(texts, embeddings)  # Use the list of combined texts

# Create the base retriever
base_retriever = vector_store.as_retriever()

# Create the MultiQueryRetriever
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,  # Base retriever
    llm=llm,  # LLM for generating additional queries
)

# Create the RetrievalQA chain with the multi-query retriever
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # You can also use "map_reduce", "refine", or "map_rerank"
    retriever=multi_query_retriever,  # Use the multi-query retriever
)

# Function to fetch streaming services from RapidAPI
def get_streaming_services(title):
    api_key = utelly_api_key  # Use the environment variable
    url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
    }
    params = {
        "term": title,  # The movie title to search for
        "country": "us",  # Assume the US as the default country
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract streaming services from the response
            results = data.get("results", [])
            if results:
                services = set()  # Use a set to avoid duplicate service names
                for result in results:
                    locations = result.get("locations", [])
                    for location in locations:
                        service_name = location.get("display_name", "")
                        if service_name:
                            services.add(service_name)
                return ", ".join(services) if services else "No streaming information available"
            else:
                return "No streaming information available"
        else:
            return "No streaming information available"
    except Exception as e:
        return "No streaming information available"

def generate_recommendation(query):
    # Add a detailed movie-specific prompt to guide the model
    movie_prompt = (
        "You are a movie recommendation assistant. Based on the user's input, recommend 3-5 movies from the provided dataset. "
        "For each movie, provide the following details in JSON-like format (without markdown):\n"
        "- Title: The name of the movie.\n"
        "- Description: A brief summary of the plot.\n"
        "- Why Recommended: Explain why this movie matches the user's preferences.\n"
        "- Genres: List the genres of the movie.\n"
        "- Release Year: When the movie was released.\n"
        "- Rating: The average rating of the movie.\n"
        "User input: " + query
    )

    # Use the RetrievalQA chain to get recommendations
    result = qa_chain.invoke(movie_prompt)
    response_text = result.get("result", "")

    # Clean up the response text
    response_text = response_text.strip()

    # Parse the JSON-like response
    try:
        # Split the response into individual JSON objects
        json_blocks = response_text.strip().split("\n\n")
        movie_blocks = []
        for block in json_blocks:
            block = block.strip().strip("{}")
            movie = {}
            for line in block.split("\n"):
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().strip('"')
                    value = value.strip().strip('"').strip(",").strip('"')
                    if key == "Genres":
                        value = value.strip("[]").replace('"', "").split(", ")
                    movie[key] = value
            movie_blocks.append(movie)
    except Exception as e:
        print(f"Error parsing JSON-like response: {e}")
        movie_blocks = []

    # Format the recommendations
    if not movie_blocks:
        return "No recommendations found. Please try again with a different query."
    else:
        formatted_recommendations = []
        for i, movie in enumerate(movie_blocks, start=1):
            title = movie.get("Title", "N/A")
            streaming_services = get_streaming_services(title)
            formatted_recommendations.append(
                f"🎬 Recommendation {i}\n"
                f"   - Title: {title}\n"
                f"   - Description: {movie.get('Description', 'N/A')}\n"
                f"   - Why Recommended: {movie.get('Why Recommended', 'N/A')}\n"
                f"   - Genres: {', '.join(movie.get('Genres', ['N/A']))}\n"
                f"   - Release Year: {movie.get('Release Year', 'N/A')}\n"
                f"   - Rating: {movie.get('Rating', 'N/A')}\n"
                f"   - Streaming Services: {streaming_services}\n"
                f"{'-' * 50}"
            )
        return "\n".join(formatted_recommendations)
        
# Main function
def main():
    print("Welcome to the Movie Recommendation Tool!")
    while True:
        user_input = input("How are you feeling today? (Type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        recommendation = generate_recommendation(user_input)
        print("Recommendation:", recommendation)

if __name__ == "__main__":
    main()