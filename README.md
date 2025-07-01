# Waitz Data Scraper (UCSD Building Occupancy Tracker)

A pipeline for collecting and visualizing real-time crowd-level data at UCSD campus locations.

📊 **Live Demo:** [https://ucsd-building-occupancy-tracker.streamlit.app](https://ucsd-building-occupancy-tracker.streamlit.app)

---

## Overview

This project:

1. **Fetches** occupancy data from the Waitz API (e.g. Geisel Library, RIMAC Gym).  
2. **Parses** out each location’s name, crowding percentage, open/closed status, and timestamp.  
3. **Stores** results in Google Sheets via a service-account.  
4. **Runs** on a schedule using AWS Lambda (no servers to manage).  
5. **Visualizes** historical trends in a Streamlit dashboard.

---

## Features

- **Automated scraping** every 30 minutes with AWS Lambda & CloudWatch (or Cron).  
- **Google Sheets integration** for free, persistent storage.  
- **Timestamped records** for trend analysis.  
- **Streamlit app** for interactive filtering and charting of past data.
