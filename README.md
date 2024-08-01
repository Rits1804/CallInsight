This project is designed to transcribe call recordings and generate detailed summaries, insights, and recommendations based on the transcribed text using Google's Gemini Pro model. It also utilizes AWS Transcribe service and an S3 bucket to handle the transcription and storage of audio files efficiently.


## Features

- Transcribe Hindi call recordings using AWS Transcribe.
  
- Generate comprehensive summaries and insights from the transcribed text using Google's Gemini Pro model.
  
- Save the generated content to a text file.

## Requirements

- Python 3.10

- AWS CLI configured with the appropriate permissions
  
- Boto3
  
- Google Generative AI (Gemini Pro) API key
  
- An S3 bucket for storing audio files and transcription results

  ## Installation
  1.Clone the repository

  2.Install dependencies

  3.Set up environment variables(GOOGLE_API_KEY) https://aistudio.google.com/app/apikey


  ## Usage
   python transcribe.py
  
