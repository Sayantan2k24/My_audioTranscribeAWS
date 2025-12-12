1️⃣ API Gateway
→ invokes
→ Lambda 1 (upload_to_s3.py)
→ Uploads file to S3 /uploads/

2️⃣ S3 Event (prefix: uploads/)
→ invokes
→ Lambda 2 (start_transcription.py)
→ Starts AWS Transcribe
→ Output goes to S3 /transcribe-output/

3️⃣ S3 Event (prefix: transcribe-output/)
→ invokes
→ Lambda 3 (notify_transcript.py)
→ Reads transcript
→ Sends SNS notification