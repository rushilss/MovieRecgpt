# MovieRecgpt 🎬

Welcome to the **Movie Recommendation System**, a Python-based tool that recommends movies based on user input and provides streaming availability information. This project leverages advanced natural language processing (NLP) techniques and integrates with external APIs to deliver personalized movie recommendations.

## Features ✨

- **Personalized Recommendations**: Get movie recommendations tailored to your mood or preferences.
- **Streaming Availability**: Check which streaming platforms offer the recommended movies.
- **Advanced NLP**: Utilizes OpenAI's GPT-3.5-turbo model for generating recommendations.
- **Multi-Query Retrieval**: Enhances recommendation accuracy by generating multiple queries for better context understanding.
- **Interactive CLI**: A user-friendly command-line interface for easy interaction.

## Technologies Used 🛠️

- **Python**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **OpenAI API**: For generating movie recommendations using GPT-3.5-turbo.
- **LangChain**: For building retrieval-augmented generation (RAG) pipelines.
- **FAISS**: For efficient similarity search and retrieval.
- **Utelly API**: For fetching streaming availability information.
- **Dotenv**: For managing environment variables securely.

## How It Works 🧠

1. **Data Preparation**:
   - The system uses a dataset of top 250 movies (`top250_movies_filtered.csv`).
   - Relevant movie details (title, description, genres, ratings, etc.) are combined into a single text representation for each movie.

2. **Recommendation Generation**:
   - The user provides input (e.g., "I feel like watching a comedy").
   - The system uses OpenAI's GPT-3.5-turbo model to generate recommendations based on the input.
   - A multi-query retriever enhances the recommendation process by generating additional queries for better context understanding.

3. **Streaming Availability**:
   - The system checks the availability of recommended movies on popular streaming platforms using the Utelly API.

4. **Output**:
   - The system displays detailed recommendations, including:
     - Movie title
     - Description
     - Why it was recommended
     - Genres
     - Release year
     - Rating
     - Streaming platforms

## Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- An OpenAI API key
- A Utelly API key
- A LangChain API key (optional for tracing)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/rushilss/movie_gpt.git
   cd movie_gpt
   ```

2. Install the required dependencies:
   ```bash
   git clone https://github.com/rushilss/movie_gpt.git
   cd movie_gpt
   ```

3. Create a .env file in the root directory and add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   UTELLY_API_KEY=your_utelly_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key  # Optional
   ```
   
4. Run the application:
    ```bash
   python main.py
   ```
