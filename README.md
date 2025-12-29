# Genesys Cloud Recording Scripts

Scripts for interacting with Genesys Cloud API to download call recordings and metadata.

## Main Recording Download Scripts
- **download_recordings.py** - Current version for downloading recordings - Pushed
- **download_using_metadata.py** - Downloads recordings using metadata - Pushed
- **deprecated_download_recordings.py** - Legacy recording download script - Pushed

## Recording Analysis & Counting
- **tally_multi_recording_count.py** - recording counts per conversation - Pushed
- **count_recordings_for_each_id.py** - Counts recordings for each conversation ID - Pushed
- **Final_count_reccs.py** - Final version of recording counter - Pushed
- **MultipleIDfetches.py** - Fetches data for multiple IDs - Pushed
- **MultipleIDfetches_2.py** - Enhanced version of multiple ID fetcher - Pushed

## Recording Invocation Scripts, due to the API taking time to process opus files
- **recordingInvocation.py** - Invokes recording operations - Pushed
- **recordingInvocate2.py** - Version 2 of recording invocation
- **recordingInvocate3.py** - Version 3 of recording invocation
- **check.py** - Checks recording status

## Authentication
These scripts use OAuth2 client credentials flow with Genesys Cloud API.

## Environment
Default environment: mypurecloud.com
