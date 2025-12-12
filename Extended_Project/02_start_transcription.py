# S3 → event → start Transcribe job

import boto3
import uuid
import json

def lambda_handler(event, context):

    print(json.dumps(event))

    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']

    # Skip if output file triggers the same lambda
    if "transcripts/" in s3object:
        return {"message": "Skipping transcript output file"}

    s3Path = f's3://{s3bucket}/{s3object}'
    jobName = f'{s3object.replace("/", "_")}--{uuid.uuid4()}'

    outputKey = f'transcribe-output/{s3object}-output.json'

    client = boto3.client('transcribe')

    response = client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode='en-US',
        Media={
            'MediaFileUri': s3Path
        },
        OutputBucketName=s3bucket,
        OutputKey=outputKey
    )

    print(json.dumps(response, default=str))

    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }
