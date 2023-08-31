<div align="center">

# YouTube Dashboard

</div>

## Overview

Welcome to the YouTube Dashboard project! This dashboard provides comprehensive video analytics for YouTube comments, empowering users with valuable insights and statistics about specific videos. By simply inputting the video URL, users can access a wide range of analytics, including information about the top 100 comments associated with the video. The dashboard also features a trained machine learning model that incorporates a sentiment analysis for each comment.

## Table of Contents



| Section         | Description                   |
| --------------- | ----------------------------- |
| [Installation](#installation) | How to install and set up   |
| [Usage](#usage) | How to use the dashboard     |
| [Configuration](#configuration) | Configuration options      |
| [Features](#features) | List of key features       |
| [Screenshots](#screenshots) | Visuals of the dashboard  |
| [API Documentation](#api-documentation) | Details about APIs  |
| [Contributors](#contributors) | Project contributors      |
| [License](#license) | Licensing information      |

![example event parameter]()



## Features <a name="features"></a>

- **User-Friendly Interface:** Easily input the URL of the desired YouTube video in the intuitive interface.
- **Video Analytics:** Gain insights into the video's performance and impact with a variety of analytics.
- **Popular Comment Analysis:** Dive deep into the 100 most popular comments associated with the video to understand public sentiment.
- **Sentiment Analysis:** Utilize a trained machine learning model to determine sentiment for each comment, aiding in accurate public opinion assessment.
- **Comment Data Table:** View sentiment analysis and metadata for comments in a sortable table.
- **CSV Export:** Export the comment data table as a CSV file for further analysis.
- **Visualizations:** Explore visual representations of video comment data to enhance your understanding.
- **Helping Points:** Get guidance at each dashboard section to navigate effectively.

## Installation <a name="installation"></a>

1. Clone the repository:
```
git clone https://github.com/StamTheo28/youtube-dashboard.git
```

2. Move to the project project directory:
```
cd youtube-dashboard
```
3. Create and activate a virtual environment:
- Windows:
```
python -m venv venv
vevn/Scripts/activate
```
- Linux:
```
python3-m venv venv
source venv/bin/activate
```
4. Install the requirements.txt
```
pip install requirements.txt
```
5. Install nltk required packages
```
python3 -m nltk.downloader stopwords, sentiwordnet,
```
6. Run the dashboard:
```
cd myDashboard
python3 manage.py runserver
```
## Screenshots <a name="screenshots"></a>
Insert some screenshots of your dashboard here.

## API Documentation
Document any APIs or usage guidelines here.

## Contributors <a name="contributors"></a>
John Doe @johndoe
Jane Smith @janesmith

## License
This project is licensed under the XYZ License - see the LICENSE file for details.
