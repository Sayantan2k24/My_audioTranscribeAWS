```bash
API Gateway → Lambda Upload → S3 (input)
                                          \
                                           S3 Event Trigger
                                               ↓
                                   Lambda Start-Transcribe
                                               ↓
                                   Transcribe Generates JSON
                                               ↓
                          S3 (output bucket) Event Trigger
                                               ↓
                    Lambda Process-Output → Publish SNS Notification
                                               ↓
                                           Email / SMS

```