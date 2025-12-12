# Receives audio file → uploads to S3 → triggers Transcribe Lambda

import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = "your-input-bucket"  # change this # we are hardcoding this to specify to which s3 bucket the file has to be stored
                                   # First create the bucket


def lambda_handler(event, context):
    try:
        # Body from API Gateway
        body = event.get("body")
        is_base64 = event.get("isBase64Encoded", False)

        # Convert to bytes
        if is_base64:
            file_bytes = base64.b64decode(body)
        else:
            file_bytes = body.encode()

        # Generate filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.mp3"  # adjust based on actual file type

        key = f"uploads/{filename}"

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=file_bytes,
            ContentType="audio/mpeg"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "File uploaded successfully",
                "s3_key": key,
                "bucket": BUCKET_NAME
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
