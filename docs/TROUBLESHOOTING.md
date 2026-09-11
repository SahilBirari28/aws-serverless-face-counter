# Troubleshooting

## `S3 upload failed`

Open browser DevTools:

```text
F12 → Network
```

Inspect the failed S3 `PUT` request.

### `403 AccessDenied`

Check:

- `FaceUploadApiLambda` execution role has `s3:PutObject`.
- Resource ARN ends with `/*`.
- Bucket policy does not explicitly deny the request.

### `SignatureDoesNotMatch`

Check:

- Bucket Region matches `BUCKET_REGION`.
- The presigned URL has not expired.
- Browser sends the same `Content-Type` used when generating the URL.
- Do not modify the generated presigned URL.

### CORS error

Verify S3 CORS includes:

```text
PUT
```

and allows the frontend origin.

---

## Upload works but page stays on "analysing"

Check CloudWatch logs for:

```text
/aws/lambda/FaceDetectionLambda
```

Then verify:

- S3 trigger exists.
- S3 trigger is listening for `uploads/` if a prefix is configured.
- Lambda has `rekognition:DetectFaces`.
- Lambda has `s3:GetObject`.
- Lambda has `s3:PutObjectTagging`.
- S3 bucket and Rekognition are in a compatible Region.

---

## `AccessDeniedException` from Rekognition

Add:

```text
rekognition:DetectFaces
```

to the `FaceDetectionLambda` execution role.

---

## `NoSuchKey` or result stays processing

The upload API may query object tags before processing is finished.

The frontend intentionally polls `/result` for up to 30 seconds.

If the problem persists, check CloudWatch for Lambda errors.

---

## API returns CORS error

Configure API Gateway CORS:

```text
Origins: *
Methods: GET, POST, OPTIONS
Headers: content-type
```

Restrict the origin later for production.

---

## Frontend says API URL is not configured

Create:

```text
frontend/config.js
```

and set your API Gateway invoke URL.
