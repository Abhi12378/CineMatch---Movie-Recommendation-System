import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import os
import random

class MovieRecommender:
    def __init__(self, csv_file='movies.csv'):
        """Initialize the movie recommender"""
        self.csv_file = csv_file
        self.movies_df = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.load_data()
        
    def load_data(self):
        """Load movie data from CSV file"""
        try:
            if os.path.exists(self.csv_file):
                self.movies_df = pd.read_csv(self.csv_file)
            else:
                # Create sample data if CSV doesn't exist
                self.create_sample_data()
            
            # Prepare data for recommendations
            self.prepare_recommendation_data()
            
        except Exception as e:
            print(f"Error loading data: {e}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample movie data"""
        sample_movies = [
            {
                'id': 1, 'title': 'The Shawshank Redemption', 'genre': 'Drama', 
                'rating': 9.3, 'year': 1994, 'director': 'Frank Darabont',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'cast': 'Tim Robbins, Morgan Freeman', 'duration': 142
            },
            {
                'id': 2, 'title': 'The Godfather', 'genre': 'Crime', 
                'rating': 9.2, 'year': 1972, 'director': 'Francis Ford Coppola',
                'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'cast': 'Marlon Brando, Al Pacino', 'duration': 175
            },
            {
                'id': 3, 'title': 'The Dark Knight', 'genre': 'Action', 
                'rating': 9.0, 'year': 2008, 'director': 'Christopher Nolan',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.',
                'cast': 'Christian Bale, Heath Ledger', 'duration': 152
            },
            {
                'id': 4, 'title': 'Pulp Fiction', 'genre': 'Crime', 
                'rating': 8.9, 'year': 1994, 'director': 'Quentin Tarantino',
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
                'cast': 'John Travolta, Uma Thurman', 'duration': 154
            },
            {
                'id': 5, 'title': 'Forrest Gump', 'genre': 'Drama', 
                'rating': 8.8, 'year': 1994, 'director': 'Robert Zemeckis',
                'description': 'The presidencies of Kennedy and Johnson, Vietnam, Watergate, and other history unfold through the perspective of an Alabama man.',
                'cast': 'Tom Hanks, Robin Wright', 'duration': 142
            },
            {
                'id': 6, 'title': 'Inception', 'genre': 'Sci-Fi', 
                'rating': 8.8, 'year': 2010, 'director': 'Christopher Nolan',
                'description': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.',
                'cast': 'Leonardo DiCaprio, Marion Cotillard', 'duration': 148
            },
            {
                'id': 7, 'title': 'The Matrix', 'genre': 'Sci-Fi', 
                'rating': 8.7, 'year': 1999, 'director': 'Lana Wachowski',
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'cast': 'Keanu Reeves, Laurence Fishburne', 'duration': 136
            },
            {
                'id': 8, 'title': 'Goodfellas', 'genre': 'Crime', 
                'rating': 8.7, 'year': 1990, 'director': 'Martin Scorsese',
                'description': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.',
                'cast': 'Robert De Niro, Ray Liotta', 'duration': 146
            },
            {
                'id': 9, 'title': 'Interstellar', 'genre': 'Sci-Fi', 
                'rating': 8.6, 'year': 2014, 'director': 'Christopher Nolan',
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'cast': 'Matthew McConaughey, Anne Hathaway', 'duration': 169
            },
            {
                'id': 10, 'title': 'The Lion King', 'genre': 'Animation', 
                'rating': 8.5, 'year': 1994, 'director': 'Roger Allers',
                'description': 'Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.',
                'cast': 'Matthew Broderick, Jeremy Irons', 'duration': 88
            },
            {
                'id': 11, 'title': 'Titanic', 'genre': 'Romance', 
                'rating': 7.8, 'year': 1997, 'director': 'James Cameron',
                'description': 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
                'cast': 'Leonardo DiCaprio, Kate Winslet', 'duration': 194
            },
            {
                'id': 12, 'title': 'Avatar', 'genre': 'Sci-Fi', 
                'rating': 7.8, 'year': 2009, 'director': 'James Cameron',
                'description': 'A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.',
                'cast': 'Sam Worthington, Zoe Saldana', 'duration': 162
            },
            {
                'id': 13, 'title': 'The Avengers', 'genre': 'Action', 
                'rating': 8.0, 'year': 2012, 'director': 'Joss Whedon',
                'description': 'Earth\'s mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.',
                'cast': 'Robert Downey Jr., Chris Evans', 'duration': 143
            },
            {
                'id': 14, 'title': 'Jurassic Park', 'genre': 'Adventure', 
                'rating': 8.1, 'year': 1993, 'director': 'Steven Spielberg',
                'description': 'A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park\'s cloned dinosaurs to run loose.',
                'cast': 'Sam Neill, Laura Dern', 'duration': 127
            },
            {
                'id': 15, 'title': 'Toy Story', 'genre': 'Animation', 
                'rating': 8.3, 'year': 1995, 'director': 'John Lasseter',
                'description': 'A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy\'s room.',
                'cast': 'Tom Hanks, Tim Allen', 'duration': 81
            }
        ]
        
        self.movies_df = pd.DataFrame(sample_movies)
        # Save to CSV
        self.movies_df.to_csv(self.csv_file, index=False)
    
    def prepare_recommendation_data(self):
        """Prepare data for content-based recommendations"""
        # Combine features for content-based filtering
        self.movies_df['combined_features'] = (
            self.movies_df['genre'] + ' ' + 
            self.movies_df['director'] + ' ' + 
            self.movies_df['description']
        )
        
        # Create TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.movies_df['combined_features'])
    
    def get_all_movies(self):
        """Return all movies"""
        return self.movies_df.to_dict('records')
    
    def get_genres(self):
        """Return all unique genres"""
        return sorted(self.movies_df['genre'].unique().tolist())
    
    def get_movie_by_id(self, movie_id):
        """Get movie by ID"""
        movie = self.movies_df[self.movies_df['id'] == movie_id]
        if not movie.empty:
            return movie.iloc[0].to_dict()
        return None
    
    def search_movies(self, query):
        """Search movies by title"""
        query = query.lower()
        results = self.movies_df[
            self.movies_df['title'].str.lower().str.contains(query, na=False)
        ]
        return results.to_dict('records')
    
    def get_popular_movies(self, limit=10):
        """Get popular movies sorted by rating"""
        popular = self.movies_df.nlargest(limit, 'rating')
        return popular.to_dict('records')
    
    def get_recommendations(self, movie_title='', genre='', min_rating=0, max_results=10):
        """Get movie recommendations based on various criteria"""
        recommendations = []
        
        if movie_title:
            # Content-based recommendations
            recommendations = self._get_content_based_recommendations(movie_title, max_results)
        else:
            # Filter-based recommendations
            filtered_movies = self.movies_df.copy()
            
            if genre:
                filtered_movies = filtered_movies[filtered_movies['genre'] == genre]
            
            if min_rating > 0:
                filtered_movies = filtered_movies[filtered_movies['rating'] >= min_rating]
            
            # Sort by rating and get top results
            recommendations = filtered_movies.nlargest(max_results, 'rating').to_dict('records')
        
        return recommendations
    
    def _get_content_based_recommendations(self, movie_title, max_results):
        """Get content-based recommendations for a given movie"""
        # Find the movie
        movie_indices = self.movies_df[
            self.movies_df['title'].str.lower().str.contains(movie_title.lower(), na=False)
        ].index
        
        if len(movie_indices) == 0:
            return []
        
        movie_idx = movie_indices[0]
        
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(self.tfidf_matrix[movie_idx], self.tfidf_matrix).flatten()
        
        # Get similarity scores for all movies
        sim_scores = list(enumerate(cosine_sim))
        
        # Sort movies by similarity score
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top similar movies (excluding the input movie itself)
        sim_scores = sim_scores[1:max_results+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return the recommended movies
        return self.movies_df.iloc[movie_indices].to_dict('records')