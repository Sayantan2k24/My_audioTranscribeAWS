
# First create an SNS TOPIC --> Must subscribe first to get the email notification  - and then configure this lambda function
# Triggered by Transcribe output file → extracts text → sends SNS
import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:123456789012:audio-transcript-notifications"  # give your SNS topic ARN

def lambda_handler(event, context):

    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    # Only handle Transcribe output
    if not key.endswith(".json"):
        return {"message": "Not a transcript output file"}

    # Download the output JSON
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read()

    data = json.loads(body)

    # Extract transcript text
    transcript = data["results"]["transcripts"][0]["transcript"]

    # Format SNS message
    message = {
        "file": key,
        "bucket": bucket,
        "transcript_preview": transcript[:300] + "..." if len(transcript) > 300 else transcript
    }

    # Publish to SNS
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="AWS Transcription Completed",
        Message=json.dumps(message)
    )

    return {"message": "SNS notification sent"}
