# 📝 Overview
This project aims to analyze the presence of alt-right language in gaming-related content on YouTube, exploring potential connections in the content and recommendation patterns. The primary function of the scripts in this repository is to request a mass volume of gaming videos and compare the content of the collected video transcripts to that of political videos and keywords. 

# 🔧 Set-Up
## 🛠️ Environment Setup
1. Begin by creating a `.env` file within your repository clone.
2. Add the required environment variables, including `YT_API` and `OAUTH_SECRET`.

## 📦 Package Installation
1. **Create a Virtual Environment:**
   - Open your terminal and navigate to your project directory.
   - Create a new virtual environment by running `python -m venv env`. Replace `env` with your desired virtual environment name if needed.
   - Activate the virtual environment:
     - On Windows: `.\env\Scripts\activate`
     - On Mac/Linux: `source env/bin/activate`
2. **Install Necessary Packages:**
   - With the virtual environment activated, install all required packages using the command: `pip install -r requirements.txt`.

## 🗂️ Temporary File Storage
- **Raw (Unprocessed) Datasets:** `collected_data`
- **Files used to test small scripts:** `testing`
- **Transcript output format observation:** `transcriptions`
- **Figures (PNGs):** `viz`
- **Final Outputted Dataset:** `classified_video_titles.csv`

## 📂 Permanent Files
- **Word Bank (alt-right, gaming, skip_words):** `keywords`
- **Mass Data Collection:** `collection.py`
- **Data Categorization/Cleaning:** `processing.py`
- **Extraction and Similarity Scoring:** `extraction.py`
- **Data Visualization Generation:** `visualization.py`

# 🚀 Usage Instructions
1. **Data Collection:**
   - Run `collection.py` to collect gaming-related videos and political videos from YouTube.
2. **Data Processing:**
   - Execute `processing.py` to clean and categorize the collected data.
3. **Data Extraction and Similarity Scoring:**
   - Use `extraction.py` to extract relevant information and perform similarity scoring.
4. **Data Visualization:**
   - Generate visualizations using `visualization.py` to observe patterns and insights.

# 🤝 Contributing
Contributions are welcome! Please create a pull request or open an issue to discuss any changes.

# 📜 License
This project is licensed under the MIT License.

# 📧 Contact
For questions or further information, please contact Elizabeth Huang.
