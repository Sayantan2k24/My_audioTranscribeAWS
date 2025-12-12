
---

# 🟩 **LAMBDA 1 — Upload Handler (API Gateway → S3)**

### **Services used:**

* S3 (upload audio)

### **Required actions:**

```
s3:PutObject
s3:PutObjectAcl   (optional if public, usually not needed)
```

---

## ✅ **IAM Policy for Lambda 1 (Upload Handler)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::your-input-bucket/uploads/*"
    }
  ]
}
```

⚠️ Replace `your-input-bucket` with real bucket name.

---

# 🟦 **LAMBDA 2 — Start Transcribe (Triggered by S3)**

### **Services used:**

* S3 (read metadata of uploaded file)
* Transcribe (start transcription job)
* CloudWatch Logs (default)

### **Required actions:**

```
s3:GetObject
s3:GetObjectVersion
s3:ListBucket
transcribe:StartTranscriptionJob
iam:PassRole            (ONLY if Transcribe uses a custom service role)
```

⚠️ **In your case, Transcribe does NOT need PassRole**, because you are writing output to S3 using:

```python
OutputBucketName=...
```

So no special service role needed.

---

## ✅ **IAM Policy for Lambda 2 (Start Transcribe)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::your-input-bucket",
        "arn:aws:s3:::your-input-bucket/uploads/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob"
      ],
      "Resource": "*"
    }
  ]
}
```

---

# 🟪 **LAMBDA 3 — Notify (Reads Transcribe Output → Sends SNS)**

### **Services used:**

* S3 (read transcribe output JSON)
* SNS (publish notification)

### **Required actions:**

```
s3:GetObject
sns:Publish
```

---

## ✅ **IAM Policy for Lambda 3 (Notify)**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::your-input-bucket/transcribe-output/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:ap-south-1:123456789012:audio-transcript-notifications"
    }
  ]
}
```

---

# 🔥 **BONUS: ALL Lambdas Need CloudWatch Logging**

AWS automatically adds this, but mentioning it for clarity:

```
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

These are handled by **AWSLambdaBasicExecutionRole**.

---

# 🎯 **Summary Table (Very Clear)**

| Lambda Function                 | Uses                      | Required IAM Actions                                                |
| ------------------------------- | ------------------------- | ------------------------------------------------------------------- |
| **Lambda 1 – Upload**           | S3 Put                    | `s3:PutObject`                                                      |
| **Lambda 2 – Start Transcribe** | S3 Read, Transcribe Start | `s3:GetObject`, `s3:ListBucket`, `transcribe:StartTranscriptionJob` |
| **Lambda 3 – Notify**           | S3 Read, SNS Publish      | `s3:GetObject`, `sns:Publish`                                       |

---
