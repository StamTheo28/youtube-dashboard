<div align="center">

# YouTube Dashboard

</div>

## Overview

Welcome to the YouTube Dashboard project! This dashboard provides comprehensive video analytics for YouTube comments, empowering users with valuable insights and statistics about specific videos. By simply inputting the video URL, users can access a wide range of analytics, including information about the top 100 comments associated with the video. The dashboard also features a trained machine learning model that incorporates a sentiment analysis for each comment.

## Table of Contents



| Section         | Description                   |
| --------------- | ----------------------------- |
| [Features](#features) | List of key features       |
| [Installation](#installation) | How to install and set up   |
| [Server Configurations](#server) | Server Configurations and features used   |
| [Screenshots](#screenshots) | Visuals of the dashboard  |
| [API Documentation](#api-documentation) | Details about APIs  |
| [Contributors](#contributors) | Project contributors      |
| [License](#license) | Licensing information      |

[![Django CI](https://github.com/StamTheo28/youtube-dashboard/actions/workflows/django.yml/badge.svg)](https://github.com/StamTheo28/youtube-dashboard/actions/workflows/django.yml)




## Features <a name="features"></a>

- **User-Friendly Interface:** Easily input the URL of the desired YouTube video in the intuitive interface.
- **Video Analytics:** Gain insights into the video's performance and impact with a variety of analytics.
- **Popular Comment Analysis:** Dive deep into the 100 most popular comments associated with the video to understand public sentiment.
- **Sentiment Analysis:** Utilize a trained machine learning model to determine sentiment for each comment, aiding in accurate public opinion assessment.
- **Comment Data Table:** View sentiment analysis and metadata for comments in a sortable table.
- **CSV Export:** Export the comment data table as a CSV file for further analysis.
- **Visualizations:** Explore visual representations of video comment data to enhance your understanding.
- **Error Catching:** Improve your experience through the implementation of extensive error catching.
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
4. Run the setup.py file, that installs all necessery dependencies.
```
python3 setup.py
```
5. Run the dashboard:
```
cd myDashboard
python3 manage.py runserver
```

## Server Configurations  <a name="server"></a>
- The project was deployed on an AWS Ubuntu 22.04 server using the AWS free tier.
- In order to run the current project on AWS you have to modify the default volume of the server as the default size is not enough to use all the required dependencies (8Gb+ Disk Space)


## Screenshots <a name="screenshots"></a>
Insert some screenshots of your dashboard here.

## API Documentation
Document any APIs or usage guidelines here.

## Contributors <a name="contributors"></a>

| Section | Role | Email  | LinkedIn |
|---|---|---|---|
| Stamatis Theocharous | Dashboard Developer | StamatisTheocharous@gmail.com | [Stamatis](https://www.linkedin.com/in/stamatistheocharous/) |
| Andreas Argyrou | Semantic Analysis Developer | AndreasArgyrou999@gmail.com | [Andreas](https://www.linkedin.com/in/andreas-arghyrou-2260151b4/) |

## Extras
To ensure that the project is of high quality i have used:
- Flake8 with a pre-commit yaml file to ensure that my code follows industry level Python Standards (Pep8).
- Used a django.yml to build and test the django app in CI/CD pipeline using git.
- Created a number of Django Tests to make sure that the app works as intended.


## License
This project is licensed under the XYZ License - see the LICENSE file for details.
