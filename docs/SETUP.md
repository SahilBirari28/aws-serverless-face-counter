# Setup Guide

This guide deploys the project using the AWS Management Console.

## 1. Choose one AWS Region

Use one Region for all project services.

Example:

```text
Asia Pacific (Mumbai)
ap-south-1
```

Your S3 bucket and Rekognition operation must use a compatible Region.

---

## 2. Create the S3 Bucket

1. Open **Amazon S3**.
2. Choose **Create bucket**.
3. Enter a globally unique name.
4. Keep **Block Public Access** enabled.
5. Create the bucket.

Example:

```text
sahil-face-counter-project-2026
```

### S3 CORS

Go to:

```text
S3 → Your bucket → Permissions → Cross-origin resource sharing (CORS)
```

Use:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag", "x-amz-request-id"],
        "MaxAgeSeconds": 3000
    }
]
```

For a real deployment, replace `*` in `AllowedOrigins` with your actual website origin.

---

## 3. Create FaceDetectionLambda

1. Open **AWS Lambda**.
2. Create function:
   - Name: `FaceDetectionLambda`
   - Runtime: Python 3.13
   - Architecture: x86_64
3. Paste code from:

```text
lambda/face_detection/lambda_function.py
```

4. Deploy.

### IAM Permissions

Attach an inline policy based on:

```text
iam/face_detection_policy.json
```

Replace:

```text
YOUR-BUCKET-NAME
```

with your real bucket name.

The Lambda role must also retain its normal basic CloudWatch logging permissions.

---

## 4. Create S3 Event Trigger

On `FaceDetectionLambda`:

1. Choose **Add trigger**.
2. Select **S3**.
3. Choose your bucket.
4. Event type: **All object create events**.
5. Optional but recommended:
   - Prefix: `uploads/`
6. Add the trigger.

---

## 5. Create FaceUploadApiLambda

Create a second Lambda:

```text
Name: FaceUploadApiLambda
Runtime: Python 3.13
Architecture: x86_64
```

Paste:

```text
lambda/upload_api/lambda_function.py
```

Deploy it.

### Environment Variables

Add:

```text
BUCKET_NAME = YOUR-EXACT-BUCKET-NAME
BUCKET_REGION = ap-south-1
```

Use your actual bucket Region.

### IAM Permissions

Attach:

```text
iam/upload_api_policy.json
```

after replacing `YOUR-BUCKET-NAME`.

---

## 6. Create API Gateway HTTP API

1. Open **API Gateway**.
2. Create an **HTTP API**.
3. Add Lambda integration:
   - `FaceUploadApiLambda`

Create these routes:

```text
POST /upload-url
GET  /result
```

Connect both routes to `FaceUploadApiLambda`.

---

## 7. Configure API Gateway CORS

Recommended development settings:

```text
Allow origins:
*

Allow methods:
GET
POST
OPTIONS

Allow headers:
content-type
```

For a real deployment, restrict origins to your actual frontend URL.

---

## 8. Configure the Frontend

Copy:

```text
frontend/config.example.js
```

to:

```text
frontend/config.js
```

Set:

```javascript
window.APP_CONFIG = {
    API_URL: "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com"
};
```

Do not put AWS credentials in the browser.

---

## 9. Run Locally

Use VS Code Live Server or another local web server.

Example:

```text
http://127.0.0.1:5500/frontend/index.html
```

Then:

1. Select a JPG/PNG image.
2. Click **Upload & Detect Faces**.
3. Wait for the result.

---

## 10. Verify AWS Resources

### S3

The uploaded object should appear under:

```text
uploads/
```

### CloudWatch

Open:

```text
CloudWatch → Logs → Log groups → /aws/lambda/FaceDetectionLambda
```

Expected:

```text
Image Name: uploads/<uuid>.jpg
Number of faces detected: 5
```

### S3 Object Tags

The image should eventually contain:

```text
status = completed
face-count = 5
```

---

## Production Improvements

For a production-grade version, consider:

- Restrict CORS origins.
- Add authentication.
- Add file size limits.
- Validate images more strictly.
- Store job results in DynamoDB rather than S3 tags.
- Add lifecycle rules to delete old uploaded images.
- Add throttling / rate limiting.
- Add monitoring and alarms.
