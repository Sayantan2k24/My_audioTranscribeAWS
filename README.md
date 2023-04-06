# My_audioTranscribeAWS

See my article on medium to understand how I used this code:
https://medium.com/@sayantansamanta12102001/speech-to-text-using-aws-transcribe-s3-and-lambda-7e8854d0f21f


This is a Python script that uses the Amazon Web Services (AWS) SDK for Python (Boto3) and AWS Lambda service to trigger the Amazon Transcribe service to transcribe an audio file that has been uploaded to an S3 bucket.

Here is a step-by-step explanation of the code:

The first line imports the required libraries: boto3, uuid, and json.

lambda_handler() is a function that is executed when AWS Lambda is triggered. It takes two arguments: event and context.

json.dumps(event) converts the event argument into a JSON string and prints it to the console for debugging purposes.

The record variable extracts the first record from the event argument.

The s3bucket and s3object variables extract the name of the S3 bucket and the key of the uploaded audio file from the record variable.

The s3Path, jobName, and outputKey variables are created. s3Path contains the S3 bucket name and audio file key as a string. jobName is a unique name for the transcription job, which is created using the uuid module. outputKey is the path and name of the output file that will contain the transcription results.

A Boto3 client object is created for the Amazon Transcribe service.

The client.start_transcription_job() method is called with the required parameters to start a new transcription job. The method takes the job name, language code, the location of the audio file, and the location where the transcription output will be saved.

The json.dumps(response, default=str) method converts the response from Amazon Transcribe into a JSON string and prints it to the console for debugging purposes.

The function returns a dictionary with the TranscriptionJobName key, which contains the name of the transcription job that was just started.

Overall, this script automates the process of starting a new transcription job in Amazon Transcribe when a new audio file is uploaded to an S3 bucket. It also prints out debug information to the console to help with troubleshooting and monitoring the process.
