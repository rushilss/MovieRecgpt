# Movie Reccommedation gpt 🎬

Welcome to **MovieRecgpt**, a movie recommendation system powered by **Retrieval-Augmented Generation (RAG)**. This Python-based tool combines the strengths of OpenAI's GPT-3.5-turbo model with efficient retrieval techniques to deliver highly personalized movie recommendations. Whether you're in the mood for a romantic comedy, a thrilling sci-fi adventure, or a classic drama, MovieRecgpt tailors its suggestions to your preferences and even tells you where to stream them. By leveraging RAG, the system enhances recommendation accuracy by retrieving relevant movie data and generating context-aware responses, ensuring you get the perfect movie match every time. Lights, camera, action—let’s find your next favorite film! 🍿

## Example Output 🖥️

Here’s an example of how the system works and what the output looks like:

### User Input:
```plaintext
How are you feeling today? (Type 'exit' to quit): I feel like taking a romantic vacation throughout Europe

🎬 Recommendation 1
   - Title: Before Sunrise
   - Description: A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. Unfortunately, both know that this will probably be their only night together.
   - Why Recommended: This movie captures a romantic encounter between two strangers in Europe, specifically in Vienna, which aligns with your desire for a romantic vacation throughout Europe.
   - Genres: Drama, Romance
   - Release Year: 1995
   - Rating: 8.1
   - Streaming Services: Amazon Instant Video, iTunes, Google Play
--------------------------------------------------
🎬 Recommendation 2
   - Title: Before Sunset
   - Description: Nine years after Jesse and Celine first met, they encounter each other again on the French leg of Jesse's book tour.
   - Why Recommended: Continuing the romantic journey, this film reunites the characters in Paris, France, providing a romantic setting in Europe for your movie choice.
   - Genres: Drama, Romance
   - Release Year: 2004
   - Rating: 8.1
   - Streaming Services: Amazon Instant Video, iTunes, Google Play
--------------------------------------------------
🎬 Recommendation 3
   - Title: Casablanca
   - Description: A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco.
   - Why Recommended: While not set in Europe, the romantic and dramatic elements of this classic film set in French Morocco might still appeal to your desire for a romantic movie experience.
   - Genres: Drama, Romance, War
   - Release Year: 1942
   - Rating: 8.5
   - Streaming Services: Amazon Instant Video, iTunes, Google Play
--------------------------------------------------
```
## Features ✨

- **Personalized Recommendations**: Get movie recommendations tailored to your mood or preferences.
- **Streaming Availability**: Check which streaming platforms offer the recommended movies.
- **Advanced NLP**: Utilizes OpenAI's GPT-3.5-turbo model for generating recommendations.
- **Retrieval-Augmented Generation (RAG)**: Combines retrieval of relevant movie data with generative AI to provide highly accurate and context-aware recommendations.
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
