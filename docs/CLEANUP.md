# Cleanup Guide

Use this after completing your demo if you want to avoid ongoing AWS maintenance cost.

## Recommended deletion order

1. Delete the API Gateway API.
2. Delete `FaceUploadApiLambda`.
3. Delete `FaceDetectionLambda`.
4. Empty the S3 bucket.
5. Delete the S3 bucket.
6. Delete project-specific IAM roles and inline policies.
7. Delete project CloudWatch log groups if you no longer need them.
8. Check AWS Billing / Cost Explorer for remaining resources.

## Important

Deleting the GitHub repository is **not required**.

The GitHub repository is your portfolio evidence and can remain online after the AWS infrastructure is removed.

Before deleting AWS resources, capture:

- Frontend screenshot showing face count
- S3 upload screenshot
- Lambda trigger screenshot
- CloudWatch result screenshot
- Architecture diagram
- Optional short demo video

Never publish AWS credentials in screenshots.
