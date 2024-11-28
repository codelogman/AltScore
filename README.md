## Overview

This challenge is about as close as you can get to a day at AltScore - immersed in data, writing code, and focused on hitting a goal.

You’ll face plenty of uncertainty, and the options aren’t endless, so you have to be resourceful. It’s about making sense of raw information, turning complexity into something useful, and finding that balance between creativity and accuracy. Every choice matters as you adjust your models, fine-tune your features, and learn as you go. It’s a chance to show how you handle real-world problems where the path to the answer isn’t always clear.

Objective

Participants are challenged to estimate the cost of living (a value between 0 and 1) in different regions of LATAM based on mobility data. You will be provided with a dataset that contains anonymized device-level information, including geographic coordinates and timestamps. Your task is to transform this data into meaningful features that can accurately predict the cost of living.

Dataset Provided

Columns:
device_id: An anonymized identifier for each mobile device.
lat: Latitude of the recorded location.
lon: Longitude of the recorded location.
timestamp: The time of the record.
Participants are encouraged to utilize external datasets and variables to enrich their predictions. You have complete freedom to incorporate any additional sources of information you think could improve your model's performance.

Submission Format

Your submission should be a CSV file with the following columns:

hex_id: The H3 hexagon index that represents a specific geographic area.
cost_of_living: Your predicted value for the cost of living in that hexagon, ranging between 0 and 1.
Guidelines
Feature Engineering Focus: We are particularly interested in the creativity and quality of your feature engineering. How well you transform and enrich the data will be a key factor in evaluation.
Predictive Power: In addition to feature engineering, we also care about the predictive power of the features you create. The features should have a strong relationship with the target variable and demonstrate clear predictive capabilities.
Use of External Variables: Feel free to use additional data sources you believe could be relevant to determining cost of living.
Model Flexibility: We are less concerned with the specific model you use. Whether it's a simple linear regression or a complex ensemble method, what matters most is how well you utilize and engineer features from the provided dataset and any external variables you choose to include.
Evaluation Metrics
Feature Engineering and research: The emphasis will be on the quality of feature engineering, including the predictive power of the features and how participants derive insights from the raw data and external sources.
Root Mean Squared Error (RMSE): Predictions will be evaluated using RMSE to measure the accuracy of cost-of-living predictions.
Code Quality: If called to an interview, candidates must show a GitHub repository with all the code used for the competition, written in Python. This repo will be reviewed for code quality, organization, reproducibility, and understanding of the problem.
Resources
Participants will be provided with:

A dataset containing device-level location information.
A dataset with examples of hex_id and it's cost_of_living to be used as a train dataset.
A dataset with only hex_id that should be completed with the cost_of_living for submission.
Documentation and sample scripts to get started with H3 hexagon aggregation.
Submission Example
Below is an example of the expected CSV format for your submission:

hex_id,cost_of_living
8a2a1072b59ffff,0.45
8a2a1072a7bffff,0.60
8a2a1072959ffff,0.33
8a2a1072b0fffff,0.75
8a2a107282bffff,0.25


Frequently Asked Questions
What is the H3 Methodology?
H3 is a geospatial indexing system that divides the world into a grid of hexagonal cells. Each cell is identified by a unique index, which allows for consistent spatial aggregation and analysis. The H3 system is particularly useful for geographic data, as hexagons provide a uniform way to represent areas with minimal distortion compared to square grids.

For a detailed explanation of the H3 methodology, you can refer to the official H3 documentation.

How Do I Convert Latitude and Longitude to an H3 Index in Python?
Below is a Python snippet using the h3 library to convert latitude and longitude coordinates to an H3 index:

## First, make sure to install the h3-py library:
## pip install h3


import h3

## Example coordinates
latitude = 37.7749 
longitude = -122.4194 
resolution = 9  # H3 resolution level (higher means smaller hexagons)

//Convert lat/lon to an H3 index
h3_index = h3.latlng_to_cell(latitude, longitude, resolution)

print(f"H3 Index: {h3_index}")
