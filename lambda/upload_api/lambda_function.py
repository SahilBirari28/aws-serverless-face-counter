import boto3
import json
import os
import uuid
from botocore.config import Config

BUCKET_NAME = os.environ["BUCKET_NAME"]
BUCKET_REGION = os.environ.get("BUCKET_REGION", "ap-south-1")

s3 = boto3.client(
    "s3",
    region_name=BUCKET_REGION,
    config=Config(signature_version="s3v4")
)


def api_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    print(json.dumps(event))

    route = event.get("routeKey", "")

    if route == "POST /upload-url":
        return create_upload_url(event)

    if route == "GET /result":
        return get_result(event)

    return api_response(404, {"error": "Route not found"})


def create_upload_url(event):
    try:
        body = json.loads(event.get("body") or "{}")

        filename = body.get("filename", "")
        content_type = body.get("contentType", "")

        if not filename:
            return api_response(400, {"error": "Filename is required"})

        allowed_content_types = {
            "image/jpeg": {"jpg", "jpeg"},
            "image/png": {"png"}
        }

        if content_type not in allowed_content_types:
            return api_response(
                400,
                {"error": "Only JPEG and PNG files are supported"}
            )

        if "." not in filename:
            return api_response(400, {"error": "File extension is required"})

        extension = filename.rsplit(".", 1)[1].lower()

        if extension not in allowed_content_types[content_type]:
            return api_response(
                400,
                {"error": "File extension and content type do not match"}
            )

        key = f"uploads/{uuid.uuid4()}.{extension}"

        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": key,
                "ContentType": content_type
            },
            ExpiresIn=300,
            HttpMethod="PUT"
        )

        return api_response(
            200,
            {
                "uploadUrl": upload_url,
                "key": key
            }
        )

    except Exception as exc:
        print(f"Upload URL error: {exc}")
        return api_response(500, {"error": "Unable to create upload URL"})


def get_result(event):
    query = event.get("queryStringParameters") or {}
    key = query.get("key")

    if not key:
        return api_response(400, {"error": "Image key is required"})

    if not key.startswith("uploads/"):
        return api_response(400, {"error": "Invalid image key"})

    try:
        result = s3.get_object_tagging(
            Bucket=BUCKET_NAME,
            Key=key
        )

        tags = {
            item["Key"]: item["Value"]
            for item in result.get("TagSet", [])
        }

        status = tags.get("status", "processing")

        if status == "completed":
            return api_response(
                200,
                {
                    "status": "completed",
                    "faceCount": int(tags.get("face-count", "0"))
                }
            )

        if status == "failed":
            return api_response(
                200,
                {
                    "status": "failed",
                    "error": "Image processing failed"
                }
            )

        return api_response(200, {"status": "processing"})

    except Exception as exc:
        print(f"Result error: {exc}")

        # The image may exist before FaceDetectionLambda writes tags.
        return api_response(200, {"status": "processing"})
