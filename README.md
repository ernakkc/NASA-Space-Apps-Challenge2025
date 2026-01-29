# 🚀 NASA Space Apps Challenge 2025

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NASA](https://img.shields.io/badge/NASA-API-blue?style=for-the-badge)
![Space](https://img.shields.io/badge/Space-Apps-red?style=for-the-badge)

*Near-Earth Object (NEO) data analysis project for NASA Space Apps Challenge 2025*

</div>

---

## 📖 Overview

This project was developed for the NASA Space Apps Challenge 2025, focusing on analyzing Near-Earth Objects (NEOs) using NASA's public API. The application collects, processes, and analyzes asteroid data to provide insights about potentially hazardous space objects.

## ✨ Features

- 🌌 **NASA API Integration**: Fetches real-time NEO data from NASA's API
- 📊 **Data Collection**: Automated pagination through all available NEO records
- 💾 **Multiple Formats**: Exports data to JSON and CSV
- 🔍 **Data Analysis**: Process and analyze asteroid characteristics
- 📈 **Statistics**: Calculate key metrics about NEOs
- 🎯 **Hazard Assessment**: Identify potentially hazardous asteroids
- 🌐 **Comprehensive Dataset**: Collects orbital data, size estimates, and close approach information

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **requests**: HTTP library for API calls
- **json**: JSON data processing
- **csv**: CSV file generation
- **NASA NEO API**: Official NASA Near-Earth Object API

## 📁 Project Structure

```
NASA-Space-Apps-Challenge2025/
├── nasaDataSet.py          # Main data collection script
├── data2.py                # Additional data processing
├── asteroid_data.json      # Complete asteroid dataset
├── asteroid_sample.json    # Sample data for testing
├── nasa4/                  # Additional modules
├── nasaData3/              # Data analysis scripts
└── NASA_son/               # Final submission version
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- NASA API key (free from [NASA API Portal](https://api.nasa.gov/))
- Internet connection

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ernakkc/NASA-Space-Apps-Challenge2025.git
   cd NASA-Space-Apps-Challenge2025
   ```

2. **Install dependencies**:
   ```bash
   pip install requests
   ```

3. **Set up NASA API key**:
   - Get your free API key from [NASA API Portal](https://api.nasa.gov/)
   - Replace the API key in `nasaDataSet.py`:
     ```python
     API_KEY = "your_api_key_here"
     ```

4. **Run the data collector**:
   ```bash
   python nasaDataSet.py
   ```

## 📊 NASA NEO API

### API Endpoint
```
https://api.nasa.gov/neo/rest/v1/neo/browse
```

### Data Retrieved
For each Near-Earth Object:
- **Identification**
  - NEO Reference ID
  - Name
  - NASA JPL URL

- **Physical Characteristics**
  - Estimated diameter (min/max)
  - Absolute magnitude
  - Hazardous classification

- **Orbital Data**
  - Orbital period
  - Orbital class
  - Close approach dates
  - Relative velocity
  - Miss distance

## 💻 Usage Examples

### Basic Data Collection
```python
from nasaDataSet import fetch_all_neos

# Fetch all NEO data
all_asteroids = fetch_all_neos()
print(f"Total asteroids collected: {len(all_asteroids)}")
```

### Filtering Hazardous Objects
```python
hazardous = [neo for neo in all_asteroids 
             if neo.get('is_potentially_hazardous_asteroid')]
print(f"Potentially hazardous: {len(hazardous)}")
```

### Size Analysis
```python
large_asteroids = [neo for neo in all_asteroids 
                   if neo['estimated_diameter']['kilometers']['estimated_diameter_max'] > 1]
```

## 📈 Data Analysis Features

### Statistical Analysis
- Total number of discovered NEOs
- Size distribution analysis
- Hazard classification breakdown
- Orbital period statistics

### Visualizations (Planned)
- Size vs. hazard level scatter plots
- Orbital distribution charts
- Close approach timeline
- Discovery trends over time

## 🔍 API Features

### Pagination Handling
```python
page = 0
while page < total_pages:
    params = {
        "page": page,
        "size": 20,
        "api_key": API_KEY
    }
    response = requests.get(BROWSE_URL, params=params)
    # Process data...
    page += 1
```

### Rate Limiting
The script respects NASA API rate limits:
- Default: 1000 requests per hour
- With API key: Higher limits available

### Error Handling
```python
try:
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

## 📦 Output Formats

### JSON Output
```json
{
  "id": "2000433",
  "name": "433 Eros",
  "is_potentially_hazardous_asteroid": false,
  "estimated_diameter": {
    "kilometers": {
      "estimated_diameter_min": 22.1,
      "estimated_diameter_max": 49.4
    }
  }
}
```

### CSV Output
```csv
id,name,diameter_km,hazardous,orbital_period_days
2000433,433 Eros,34.4,false,642.93
```

## 🎯 Challenge Goals

### Primary Objectives
- ✅ Collect comprehensive NEO dataset
- ✅ Analyze asteroid characteristics
- ✅ Identify potentially hazardous objects
- ✅ Create visualization tools

### Secondary Objectives
- 📊 Statistical analysis dashboard
- 🗺️ Interactive asteroid map
- ⚠️ Risk assessment model
- 📱 Public awareness application

## 🚀 Future Enhancements

### Planned Features
- [ ] Real-time data updates
- [ ] Machine learning hazard prediction
- [ ] 3D orbital visualization
- [ ] Mobile application
- [ ] Public API for processed data
- [ ] Integration with other space data sources

### Advanced Analysis
- Trajectory prediction modeling
- Impact probability calculations
- Size evolution tracking
- Discovery trend analysis

## 🐛 Troubleshooting

### API Key Issues
```python
# Check if API key is valid
response = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?api_key={API_KEY}")
if response.status_code == 403:
    print("Invalid API key")
```

### Rate Limit Exceeded
```python
import time
# Add delay between requests
time.sleep(0.5)
```

### Connection Errors
```python
# Implement retry logic
import time
for attempt in range(3):
    try:
        response = requests.get(url)
        break
    except requests.exceptions.ConnectionError:
        time.sleep(5)
```

## 📚 Resources

### NASA APIs
- [NASA API Portal](https://api.nasa.gov/)
- [NEO API Documentation](https://api.nasa.gov/api.html#NeoWS)
- [NEO Earth Close Approaches](https://cneos.jpl.nasa.gov/ca/)

### Space Data
- [JPL Small-Body Database](https://ssd.jpl.nasa.gov/sbdb.cgi)
- [Minor Planet Center](https://minorplanetcenter.net/)
- [NEO Data Viewer](https://cneos.jpl.nasa.gov/stats/totals.html)

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- 📊 Data visualization improvements
- 🧪 New analysis algorithms
- 🐛 Bug fixes and optimizations
- 📝 Documentation enhancements
- 🌍 Translation support

## 📝 License

This project is open source and available under the MIT License.

## 👤 Team

**Developer**: Eren Akkoç
- GitHub: [@ernakkc](https://github.com/ernakkc)
- Email: ern.akkc@gmail.com

**Event**: NASA Space Apps Challenge 2025
**Category**: Near-Earth Objects Analysis
**Location**: Trabzon, Turkey

## 🏆 Competition Information

- **Event**: [NASA Space Apps Challenge](https://www.spaceappschallenge.org/)
- **Year**: 2025
- **Challenge**: Near-Earth Object Data Analysis
- **Team**: [Team Name]
- **Location**: [City, Country]

## 🌟 Acknowledgments

- NASA for providing open API access
- Space Apps Challenge organizers
- JPL Small-Body Database team
- Open source community

---

<div align="center">

**🌌 Exploring the Universe, One Asteroid at a Time! 🚀**

*Built for NASA Space Apps Challenge 2025*

⭐ Star this repo to support space exploration!

</div>
