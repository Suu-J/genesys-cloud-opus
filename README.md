# Genesys Cloud Recording Scripts

Scripts for interacting with Genesys Cloud API to download call recordings and metadata.

## Main Recording Download Scripts
- **download_recordings.py** - Current version for downloading recordings - Pushed
- **download_using_metadata.py** - Downloads recordings using metadata - Pushed
- **deprecated_download_recordings.py** - Legacy recording download script - Pushed
- **OLD_V2_download_recordings.py** - Version 2 of legacy download script
- **downloadV1.py** - Version 1 download script
- **FinalVersion1.py** - Finalized download implementation
- **testingWorking.py** - Testing version of working download script

## Recording Analysis & Counting
- **list_ids_with_multiple_recordings.py** - Identifies conversations with multiple recordings
- **tally_multi_recording_count.py** - Tallies recording counts per conversation
- **count_recordings_for_each_id.py** - Counts recordings for each conversation ID
- **Final_count_reccs.py** - Final version of recording counter
- **MultipleIDfetches.py** - Fetches data for multiple IDs
- **MultipleIDfetches_2.py** - Enhanced version of multiple ID fetcher

## Recording Invocation Scripts
- **recordingInvocation.py** - Invokes recording operations
- **recordingInvocate2.py** - Version 2 of recording invocation
- **recordingInvocate3.py** - Version 3 of recording invocation
- **check.py** - Checks recording status

## Authentication
These scripts use OAuth2 client credentials flow with Genesys Cloud API.

## Environment
Default environment: mypurecloud.com
