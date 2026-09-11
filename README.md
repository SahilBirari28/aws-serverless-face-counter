# AWS Serverless Face Counter

A serverless face-detection web application built using **Amazon S3, AWS Lambda, API Gateway, Amazon Rekognition, IAM, and CloudWatch**.

Users select an image from the browser, the image is uploaded securely to Amazon S3 using a presigned URL, an S3 event triggers a Lambda function, Amazon Rekognition detects faces, and the detected face count is displayed back on the web page.

> **Portfolio deployment note:** The AWS resources used for testing can be deleted after the demo to avoid ongoing cloud costs. This repository keeps the complete source code, setup instructions, IAM examples, and architecture for portfolio use.

---

## Features

- Browser-based image upload
- Secure S3 upload using presigned URLs
- Event-driven S3 → Lambda architecture
- Amazon Rekognition face detection
- Face count displayed on the webpage
- CloudWatch logging
- Private S3 bucket
- No AWS credentials stored in the frontend
- Cleanup guide for zero ongoing maintenance cost after demo

---

## Architecture

```text
User
  |
  v
HTML / JavaScript Frontend
  |
  | POST /upload-url
  v
Amazon API Gateway
  |
  v
FaceUploadApiLambda
  |
  | Generates presigned S3 PUT URL
  v
Browser ----------------------> Amazon S3
                                   |
                                   | ObjectCreated event
                                   v
                            FaceDetectionLambda
                                   |
                                   v
                            Amazon Rekognition
                                   |
                                   | FaceDetails[]
                                   v
                              Face Count
                                   |
                                   +--> S3 object tags
                                   |
                                   +--> CloudWatch Logs
                                   |
                                   v
Frontend polls GET /result through API Gateway
                                   |
                                   v
                         Faces Detected: N
```

See also: [`architecture/architecture.svg`](architecture/architecture.svg)

---

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores uploaded images |
| AWS Lambda | Generates upload URLs and processes images |
| API Gateway | Connects the frontend to the upload/result Lambda |
| Amazon Rekognition | Detects faces in uploaded images |
| IAM | Controls permissions between AWS services |
| CloudWatch | Stores Lambda logs |

---

## Repository Structure

```text
aws-serverless-face-counter/
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── config.example.js
├── lambda/
│   ├── face_detection/
│   │   └── lambda_function.py
│   └── upload_api/
│       └── lambda_function.py
├── iam/
│   ├── face_detection_policy.json
│   └── upload_api_policy.json
├── docs/
│   ├── SETUP.md
│   ├── CLEANUP.md
│   ├── TROUBLESHOOTING.md
│   └── GITHUB_SHOWCASE.md
├── architecture/
│   └── architecture.svg
├── screenshots/
│   └── README.md
├── sample-images/
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quick Start

1. Create a private S3 bucket.
2. Create `FaceDetectionLambda`.
3. Attach the required S3 + Rekognition IAM permissions.
4. Configure the S3 `ObjectCreated` event to trigger `FaceDetectionLambda`.
5. Create `FaceUploadApiLambda`.
6. Add `BUCKET_NAME` and `BUCKET_REGION` environment variables.
7. Create API Gateway HTTP API routes:
   - `POST /upload-url`
   - `GET /result`
8. Configure API Gateway CORS.
9. Configure S3 CORS for browser `PUT` requests.
10. Copy `frontend/config.example.js` to `frontend/config.js`.
11. Add your API Gateway invoke URL to `frontend/config.js`.
12. Open `frontend/index.html` using VS Code Live Server.

Full instructions: [`docs/SETUP.md`](docs/SETUP.md)

---

## Frontend Configuration

Create:

```text
frontend/config.js
```

from:

```text
frontend/config.example.js
```

Example:

```javascript
window.APP_CONFIG = {
    API_URL: "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com"
};
```

`config.js` is ignored by Git so your live endpoint is not accidentally committed.

---

## Expected Result

After selecting and uploading an image:

```text
Uploading image to Amazon S3...
Image uploaded. Detecting faces...
Amazon Rekognition is analysing the image...
Face detection completed!

Faces Detected: 5
```

CloudWatch should also contain:

```text
Image Name: uploads/<uuid>.jpg
Number of faces detected: 5
```

---

## Security Notes

- Never commit AWS Access Key IDs or Secret Access Keys.
- Never put AWS credentials directly in JavaScript.
- Keep the S3 bucket private.
- Use presigned URLs for temporary uploads.
- Restrict CORS origins to your real website before production use.
- Use least-privilege IAM policies.
- Do not commit `frontend/config.js` if it contains a live endpoint.
- Remove AWS resources after the demo if you do not want ongoing costs.

---

## Cost Strategy

This project uses serverless pay-as-you-go AWS services. If you do not have AWS Free Tier benefits, testing can generate small charges, especially from Amazon Rekognition.

For a portfolio with no ongoing AWS maintenance cost:

1. Build and test the project.
2. Capture screenshots / a short demo video.
3. Push this repository to GitHub.
4. Delete the AWS infrastructure.
5. Keep the frontend and documentation as a portfolio showcase.

See [`docs/CLEANUP.md`](docs/CLEANUP.md).

---

## Suggested Resume Entry

**Serverless Face Detection Web Application — AWS**  
Built an event-driven image-processing application using Amazon S3, AWS Lambda, API Gateway, Amazon Rekognition, IAM, and CloudWatch. Implemented secure browser-to-S3 uploads using presigned URLs and displayed detected face counts through a web interface.

---

## License

MIT License. See [`LICENSE`](LICENSE).
