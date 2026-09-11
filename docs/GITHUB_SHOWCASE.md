# GitHub Showcase Guide

## Recommended Repository Name

```text
aws-serverless-face-counter
```

## Repository Description

```text
Serverless face detection web application using Amazon S3, Lambda, API Gateway, Rekognition and CloudWatch.
```

## Recommended GitHub Topics

```text
aws
serverless
amazon-s3
aws-lambda
amazon-rekognition
api-gateway
cloudwatch
python
javascript
computer-vision
cloud-computing
```

## Screenshots to Add

Place screenshots inside:

```text
screenshots/
```

Recommended files:

```text
01-web-ui.png
02-image-selected.png
03-face-count-result.png
04-s3-object.png
05-lambda-trigger.png
06-cloudwatch-log.png
```

Then add them to the main README.

## Demo Video

A 30–60 second recording is enough:

1. Open the webpage.
2. Select a group photo.
3. Click upload.
4. Show face count.
5. Briefly show S3 / CloudWatch.

Upload the video to a suitable platform and link it in the README.

## Before Publishing

Check that you did NOT commit:

- AWS access keys
- AWS secret keys
- Session tokens
- `.env`
- Private keys
- Sensitive screenshots
- Active temporary presigned URLs
- Personal/private images

## Suggested Interview Explanation

> I built a serverless image-processing pipeline on AWS. The browser first requests a presigned upload URL through API Gateway and Lambda. The image is uploaded directly to a private S3 bucket. An S3 ObjectCreated event triggers another Lambda function, which sends the image to Amazon Rekognition. The function counts the detected faces, stores the result as S3 object tags, and logs the result in CloudWatch. The frontend polls a result endpoint and displays the detected face count.

## Cost-Safe Portfolio Strategy

After testing:

1. Capture screenshots/video.
2. Push the source code to GitHub.
3. Delete the AWS resources.
4. Keep the repository online as the portfolio artifact.

This allows the project to remain visible without keeping paid cloud infrastructure running.
