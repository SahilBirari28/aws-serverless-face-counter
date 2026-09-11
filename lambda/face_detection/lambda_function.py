import boto3
import urllib.parse

rekognition = boto3.client("rekognition")
s3 = boto3.client("s3")


def lambda_handler(event, context):
    print("S3 event received")

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        print(f"Bucket: {bucket}")
        print(f"Image: {key}")

        if not key.lower().endswith((".jpg", ".jpeg", ".png")):
            print("Unsupported file type. Skipping.")
            continue

        try:
            result = rekognition.detect_faces(
                Image={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": key
                    }
                },
                Attributes=["DEFAULT"]
            )

            face_count = len(result.get("FaceDetails", []))

            print("--------------------------------")
            print(f"Image Name: {key}")
            print(f"Number of faces detected: {face_count}")
            print("--------------------------------")

            s3.put_object_tagging(
                Bucket=bucket,
                Key=key,
                Tagging={
                    "TagSet": [
                        {"Key": "status", "Value": "completed"},
                        {"Key": "face-count", "Value": str(face_count)}
                    ]
                }
            )

        except Exception as exc:
            print(f"Error processing {key}: {exc}")

            # Best effort: store failed state so the frontend can stop polling.
            try:
                s3.put_object_tagging(
                    Bucket=bucket,
                    Key=key,
                    Tagging={
                        "TagSet": [
                            {"Key": "status", "Value": "failed"},
                            {"Key": "error", "Value": "processing-error"}
                        ]
                    }
                )
            except Exception as tag_exc:
                print(f"Unable to write failure tags: {tag_exc}")

            raise

    return {
        "statusCode": 200,
        "message": "S3 event processed"
    }
