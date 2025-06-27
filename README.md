# 🎬 CineMatch - Movie Recommendation System

A powerful and intelligent movie recommendation system built with Flask REST API and modern web technologies. CineMatch uses advanced machine learning algorithms to provide personalized movie recommendations based on content similarity, genres, ratings, and user preferences.

![app](https://github.com/user-attachments/assets/af1c9554-bab9-48b7-ba81-303555b0ed55)

## ✨ Features

- **🤖 Smart Recommendations**: Content-based filtering using TF-IDF vectorization and cosine similarity
- **🔍 Multiple Search Options**: Search by movie title, genre, rating, year, director, and cast
- **📊 Popular Movies**: Curated list of top-rated and popular movies
- **🎯 Advanced Filtering**: Filter movies by genre, minimum rating, and year
- **📱 REST API**: Complete RESTful API for easy integration with web and mobile applications
- **🎭 Rich Movie Details**: Comprehensive movie information including cast, director, duration, and descriptions
- **⚡ Real-time Search**: Instant search functionality with fuzzy matching
- **📈 Rating-based Sorting**: Movies sorted by ratings and popularity
- **🎨 Clean Data Structure**: Well-organized movie database with 100+ classic and modern films

## 🏗️ Architecture

### Backend Components
- **Flask Application** (`app.py`): RESTful API server with CORS support
- **Recommendation Engine** (`recommender.py`): ML-powered recommendation system
- **Movie Database** (`movies.csv`): Comprehensive movie dataset with metadata

### API Endpoints
- `GET /` - Main application page
- `GET /api/movies` - Retrieve all movies
- `GET /api/genres` - Get available genres
- `POST /api/recommend` - Get personalized recommendations
- `GET /api/movie/<id>` - Get detailed movie information
- `GET /api/search?q=<query>` - Search movies by title
- `GET /api/popular?limit=<n>` - Get popular movies

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd cinematch
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

5. **Access the application:**
- Open your browser and navigate to `http://localhost:5000`
- API endpoints are available at `http://localhost:5000/api/`

## 📚 API Documentation

### Get All Movies
```http
GET /api/movies
```
**Response:**
```json
{
  "success": true,
  "movies": [...],
  "count": 100
}
```

### Get Movie Recommendations
```http
POST /api/recommend
Content-Type: application/json

{
  "movie_title": "The Dark Knight",
  "genre": "Action",
  "min_rating": 8.0,
  "max_results": 10
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": [...],
  "session_id": "unique-session-id",
  "count": 10
}
```

### Search Movies
```http
GET /api/search?q=godfather
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "id": 2,
      "title": "The Godfather",
      "genre": "Crime",
      "rating": 9.2,
      "year": 1972,
      "director": "Francis Ford Coppola",
      "description": "The aging patriarch...",
      "cast": "Marlon Brando, Al Pacino, James Caan",
      "duration": 175
    }
  ],
  "count": 1
}
```

### Get Popular Movies
```http
GET /api/popular?limit=5
```

### Get Movie Details
```http
GET /api/movie/1
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Database Configuration
The system uses a CSV file (`movies.csv`) as the data source. The file includes:
- Movie ID, Title, Genre, Rating, Year
- Director, Cast, Duration, Description
- 100+ curated movies from classics to modern hits

## 🧠 Machine Learning Features

### Content-Based Filtering
- **TF-IDF Vectorization**: Converts movie features into numerical vectors
- **Cosine Similarity**: Measures similarity between movies based on content
- **Feature Engineering**: Combines genre, director, and description for better recommendations

### Recommendation Algorithm
1. **Input Processing**: Accepts movie title, genre, and rating preferences
2. **Feature Extraction**: Creates combined feature vectors from movie metadata
3. **Similarity Calculation**: Computes cosine similarity between movies
4. **Ranking**: Sorts recommendations by similarity score and rating
5. **Filtering**: Applies user-specified filters (genre, rating, etc.)

## 📊 Dataset

The movie database includes 100 carefully selected films featuring:
- **Genres**: Drama, Crime, Action, Sci-Fi, Comedy, Animation, Biography, War, Romance, Horror, Thriller, Adventure, Western, Mystery, Musical, Fantasy
- **Rating Range**: 7.8 - 9.3 (IMDb ratings)
- **Year Range**: 1925 - 2019 (Classic to modern cinema)
- **Directors**: Legendary filmmakers like Christopher Nolan, Martin Scorsese, Steven Spielberg, Quentin Tarantino, and more

## 🛠️ Dependencies

```
Flask==2.3.3          # Web framework
Flask-CORS==4.0.0     # Cross-origin resource sharing
pandas==2.1.1         # Data manipulation
numpy==1.24.3         # Numerical computing
scikit-learn==1.3.0   # Machine learning algorithms
python-dotenv==1.0.0  # Environment variable management
requests==2.31.0      # HTTP library
```

## 🔍 Usage Examples

### Python API Client
```python
import requests

# Get recommendations based on a movie
response = requests.post('http://localhost:5000/api/recommend', json={
    'movie_title': 'Inception',
    'max_results': 5
})
recommendations = response.json()['recommendations']

# Search for movies
response = requests.get('http://localhost:5000/api/search?q=batman')
movies = response.json()['results']

# Get popular movies
response = requests.get('http://localhost:5000/api/popular?limit=10')
popular = response.json()['movies']
```

### JavaScript/AJAX
```javascript
// Get movie recommendations
fetch('/api/recommend', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        movie_title: 'The Matrix',
        genre: 'Sci-Fi',
        min_rating: 8.0,
        max_results: 10
    })
})
.then(response => response.json())
.then(data => {
    console.log('Recommendations:', data.recommendations);
});
```

## 🧪 Testing

### Manual Testing
1. Start the server: `python app.py`
2. Test endpoints using curl, Postman, or browser
3. Verify recommendations quality and API responses

### Example Tests
```bash
# Test movie search
curl "http://localhost:5000/api/search?q=dark"

# Test recommendations
curl -X POST "http://localhost:5000/api/recommend" \
     -H "Content-Type: application/json" \
     -d '{"movie_title": "Pulp Fiction", "max_results": 5}'

# Test popular movies
curl "http://localhost:5000/api/popular?limit=10"
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Set environment variables:**
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

2. **Use a production WSGI server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Docker deployment:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔮 Future Enhancements

- **User Authentication**: Personal user accounts and watch history
- **Collaborative Filtering**: User-based recommendations
- **Movie Ratings**: User rating system and feedback
- **Advanced Filters**: Language, country, budget, box office
- **Real-time Updates**: Dynamic movie database updates
- **Social Features**: Share recommendations and create watchlists
- **Mobile App**: React Native or Flutter mobile application
- **Streaming Integration**: Links to streaming platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Movie data sourced from IMDb and other film databases
- Powered by scikit-learn for machine learning capabilities
- Built with Flask for robust web API development
- Special thanks to the open-source community

## 📞 Support

For support, questions, or feature requests:
- Create an issue on GitHub
- Contact the development team
- Check the documentation and API examples

---

**CineMatch** - Discover your next favorite movie! 🍿
