<div align="center">

# YouTube Dashboard

[![Django CI](https://github.com/StamTheo28/youtube-dashboard/actions/workflows/django.yml/badge.svg)](https://github.com/StamTheo28/youtube-dashboard/actions/workflows/django.yml)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/StamTheo28/youtube-dashboard)
![GitHub issues](https://img.shields.io/github/issues/StamTheo28/youtube-dashboard)


</div>

## Overview

Welcome to the YouTube Dashboard project! This dashboard provides comprehensive video analytics for YouTube comments, empowering users with valuable insights and statistics about specific videos. By simply inputting the video URL, users can access a wide range of analytics, including information about the top 100 most famous comments associated with the video (according to YouTube). The dashboard also features a trained machine learning model that incorporates a sentiment analysis for each comment. This is not a commercialised dashboard, however if you want to try it for yourself message me on [Linkedin](https://www.linkedin.com/in/stamatistheocharous/) or [email](StamaitsTheocharous@gmail.com) me.

## Table of Contents



| Section         | Description                   |
| --------------- | ----------------------------- |
| [Features](#features) | List of key features       |
| [Installation](#installation) | How to install and set up   |
| [Production](#production) | Production and Server Configurations used   |
| [Demo](#demo) | A demonstration and visuals of the dashboard  |
| [Contributors](#contributors) | Project contributors      |
| [License](#license) | Licensing information      |





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
4. In the project directory create a file for the environment variables and name it '.env'. Add the following code inside the file, and add your [youtube data v3 api key](https://console.cloud.google.com/apis)
```
DJANGO-KEY=django-insecure-tx%-r7q1vzgsn75$sk67uu@m(^x0-so_eavv%0$!k#*h0gh=-j
YOUTUBE-API-KEY=ADD YOUR YOUTUBE DATA V3 KEY HERE
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

## Production  <a name="server"></a>
- The django production mode uses whitenoise API to create and use static files.
- The project was deployed on an AWS Ubuntu 22.04 server using the AWS free tier.
- In order to run the current project on AWS you have to modify the default volume of the server as the default size is not enough to use all the required dependencies (8Gb+ Disk Space)


## Demo <a name="demo"></a>
Insert some screenshots of your dashboard here.


## Contributors <a name="contributors"></a>

| Section | Role | Email  | LinkedIn |
|---|---|---|---|
| Stamatis Theocharous | Dashboard Developer | StamatisTheocharous@gmail.com | [Stamatis](https://www.linkedin.com/in/stamatistheocharous/) |
| Andreas Argyrou | Semantic Analysis Developer | AndreasArgyrou999@gmail.com | [Andreas](https://www.linkedin.com/in/andreas-arghyrou-2260151b4/) |

## Extras
To ensure that the project is of high quality we implemented:
- Flake8 with a pre-commit yaml file to ensure that my code follows industry level Python Standards (Pep8).
- Used a django.yml to build and test the django app in CI/CD pipeline using git.
- Created a number of Django Tests to make sure that the app works as intended.

#### Back-end
 - YouTube comment and video metada are extracted through the use of YouTubes data v3 API.
 -- The API comments extraction is a time consuming process, thus in our dashboard we use only the top most famous comments (according to YouTube) if they exist.
 - We have added our semantic analysis model that during comment extraction we predict the semantic value of each comment (Positive, Negative & Neutral).
 - Also, we created a number of functions to determine the most used words, emojis & other to create, clean and transform our data into a readable form.
 - Heavy secutiry and data flows checks are done in the backend to ensure the correct operation and prevent any potential disruptions.

 #### Front-end
- All graphs, tables and paginators are created using js in order to not overload the server.
- Visual effects such loading effect is created using js.
- Input validations to ensure that tainted data do not negatively effect the web-app.


## License
This project is licensed under the [MIT License](LICENSE).
