import boto3
import time
import json
import google.generativeai as genai
import os

job_name = "callanalyticsHindi"
language_code = "hi-IN"  # Change language code to Hindi
media_format = "mp3"
media_uri = "s3://intern-training-test-bucket/demo/_Train Kharidne Ke Liye Loan_ HDFC Bank Funny Call Recording in India.mp3"
output_bucket = "intern-training-test-bucket"

# # Create a Transcribe client
transcribe_client = boto3.client('transcribe')
s3_client = boto3.client('s3')
# Define the transcription job parameters
transcribe_job_params = {
    "TranscriptionJobName": job_name,
    "LanguageCode": language_code,
    "MediaFormat": media_format,
    "Media": {"MediaFileUri": media_uri},
    "OutputBucketName": output_bucket  # Add this line for the output bucket
}

# Start the transcription job
response = transcribe_client.start_transcription_job(**transcribe_job_params)

# Print the response
print(response)

# Polling interval in seconds
polling_interval = 20  # Adjust as needed

# Check the status of the transcription job in a loop
while True:
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']
    
    print(f"Transcription Job Status: {job_status}")

    if job_status in ['COMPLETED', 'FAILED']:
        break  # Break out of the loop if the job is completed or failed

    time.sleep(polling_interval)  # Wait for the specified interval before checking again

# Specify the filename of the transcription results JSON file
transcription_result_key = f"{job_name}.json"

# Retrieve the transcription results JSON file from the S3 bucket
try:
    response = s3_client.get_object(Bucket=output_bucket, Key=transcription_result_key)
    # Load the JSON file
    transcript_text = json.loads(response['Body'].read().decode('utf-8'))
    # Extract the transcript text
    transcript_text = transcript_text['results']['transcripts'][0]['transcript']
    # Print the extracted text
    # print(transcript_text)
except s3_client.exceptions.NoSuchKey:
    print(f"Transcription results file '{transcription_result_key}' not found in bucket '{output_bucket}'.")
    
 
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 

 
 
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt= """Ingested from a transcription of a recent call recording:

---

**Transcribed Text:**

[Insert transcribed text here]

---

**Task:**

Based on the transcribed text from the call recording, please provide:

1. A summary of the key points discussed during the conversation.
2. Any important decisions made or actions planned during the call.
3. Insights or observations regarding the tone, sentiment, or overall theme of the conversation.
4. Recommendations or follow-up actions based on the discussion.

---

**Note to Model:**

Please elaborate on each point with as much detail as possible. Ensure that the summary is accurate and comprehensive, considering the context of the conversation and any relevant background information.

---

**Output:**

[The model's elaboration on the transcribed text will be displayed here.]"""




def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

# Pass the transcribed text to the LM
generated_content = generate_gemini_content(transcript_text, prompt)
# print(generated_content)
with open("callanalyticsHindi.txt", "w") as file:
    file.write(generated_content)