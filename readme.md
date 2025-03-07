# Movie Recommendation System

## Project Overview
This content-based recommendation system suggests movies similar to a user's selection by analyzing textual metadata. The system leverages natural language processing techniques to understand movie attributes and deliver personalized recommendations.

## Key Features
- **Content-Based Filtering**: Analyzes movie attributes including plot summaries, genres, keywords, cast, and crew
- **Advanced Text Processing**: Implements stemming, stop word removal, and feature vectorization
- **Similarity Calculation**: Uses cosine similarity to find movies with similar content profiles
- **Interactive UI**: Built with Streamlit for seamless user experience
- **Dynamic Poster Display**: Integrates with TMDB API to fetch and display movie posters
- **Responsive Design**: Optimized for both desktop and mobile viewing


## Technical Implementation
- **Data Processing**: Cleaned and preprocessed data from TMDB dataset (5000+ movies)
- **NLP Techniques**: Applied Porter Stemming and Count Vectorization to convert text data to numerical features
- **Similarity Matrix**: Calculated cosine similarity between all movie vectors
- **Model Persistence**: Implemented pickle serialization for efficient model deployment
- **Web Application**: Developed with Streamlit featuring custom CSS for enhanced visual appeal

## Dataset
The project uses the TMDB 5000 Movie Dataset, which includes:
- Basic information like title, genre, and release year
- Cast and crew details
- Plot summaries and keywords
- Production metadata

## How It Works
1. **Data Preprocessing**:
   - Combines multiple features (overview, genres, keywords, cast, crew)
   - Converts text to lowercase
   - Applies stemming to reduce words to their root form
   - Removes English stop words

2. **Feature Extraction**:
   - Uses CountVectorizer to convert text to numerical vectors
   - Creates a feature space of 5000 most frequent terms

3. **Similarity Computation**:
   - Calculates cosine similarity between movie vectors
   - Stores results in a similarity matrix

4. **Recommendation Generation**:
   - When a user selects a movie, identifies the 5 most similar titles
   - Retrieves movie posters and details via TMDB API
   - Displays recommendations in an intuitive card-based UI

## Technologies Used
- Python 3.8+
- pandas & numpy
- scikit-learn
- NLTK
- Streamlit
- TMDB API
- Pickle (for model serialization)

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/jain-atishay/Recommender-System--Movie-Recommendation-Cosine-Similarity
   cd movie-recommender
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up TMDB API:
   - Create an account on [TMDB](https://www.themoviedb.org/)
   - Generate an API key
   - Create a `.env` file in the project root and add: `TMDB_API_KEY=your_api_key_here`

4. Run the application:
   ```
   streamlit run app.py
   ```

5. Access the application in your browser at `http://localhost:8501`

## Future Enhancements
- Implement collaborative filtering to complement content-based recommendations
- Add user authentication and personalized recommendation history
- Incorporate sentiment analysis from user reviews for improved recommendation relevance
- Optimize performance for larger datasets with dimensionality reduction techniques

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License

## Acknowledgments
- TMDB for providing the dataset
- Streamlit for the excellent web application framework
- The open-source community for various libraries used in this project

---
*Created by [Atishay Jain](https://github.com/jain-atishay) - 2025*
