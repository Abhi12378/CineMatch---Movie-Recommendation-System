from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from recommender import MovieRecommender
import uuid

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = '2f83f6ad6f45d6a50b88a14b0232c460'
CORS(app)

# Initialize the movie recommender
recommender = MovieRecommender()

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/movies', methods=['GET'])
def get_all_movies():
    """Get all available movies"""
    try:
        movies = recommender.get_all_movies()
        return jsonify({
            'success': True,
            'movies': movies,
            'count': len(movies)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/genres', methods=['GET'])
def get_genres():
    """Get all available genres"""
    try:
        genres = recommender.get_genres()
        return jsonify({
            'success': True,
            'genres': genres
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_movies():
    """Get movie recommendations based on user preferences"""
    try:
        data = request.get_json()
        
        # Extract parameters
        movie_title = data.get('movie_title', '')
        genre = data.get('genre', '')
        min_rating = float(data.get('min_rating', 0))
        max_results = int(data.get('max_results', 10))
        
        # Get recommendations
        recommendations = recommender.get_recommendations(
            movie_title=movie_title,
            genre=genre,
            min_rating=min_rating,
            max_results=max_results
        )
        
        # Store in session for future reference
        session_id = str(uuid.uuid4())
        session[session_id] = recommendations
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'session_id': session_id,
            'count': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/movie/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    """Get detailed information about a specific movie"""
    try:
        movie = recommender.get_movie_by_id(movie_id)
        if movie:
            return jsonify({
                'success': True,
                'movie': movie
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Movie not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['GET'])
def search_movies():
    """Search movies by title"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
            
        results = recommender.search_movies(query)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/popular', methods=['GET'])
def get_popular_movies():
    """Get popular movies"""
    try:
        limit = int(request.args.get('limit', 20))
        popular_movies = recommender.get_popular_movies(limit)
        return jsonify({
            'success': True,
            'movies': popular_movies,
            'count': len(popular_movies)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)