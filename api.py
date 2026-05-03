import minio
import minio.error
import os
import requests
import envs
import urllib.parse
import uuid
import model

NEW_DATA_ENDPOINT = "/api/perchai/sections/%s/uploaded_media"
PERCH_MOUNT_ENDPOINT = "/api/perchai/perch_mounts/%s"
MINIO_HEALTHCHECK_PROBES = "/minio/health/live"


def is_perch_mount_service_alive() -> bool:
    url = urllib.parse.urljoin(envs.PERCHMOUNT_SYSTEM, "ping")
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return True
        else:
            print(f"Perch Mount 服務狀態異常，Status Code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"無法連接到 Perch Mount 服務: {e}")
        return False


def is_minio_alive() -> bool:
    url = urllib.parse.urljoin(envs.MINIO_HOST, MINIO_HEALTHCHECK_PROBES)

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return True
        else:
            print(f"MinIO 服務狀態異常，Status Code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"無法連接到 MinIO 服務: {e}")
        return False


def post_new_data(section_id: uuid.UUID, payload: list[dict]):
    try:
        url = urllib.parse.urljoin(
            envs.PERCHMOUNT_SYSTEM, NEW_DATA_ENDPOINT % str(section_id)
        )
        response = requests.post(url, json=payload)
        response.raise_for_status()

        print("上傳成功！")
        print("伺服器回傳：", response.json())
    except requests.exceptions.RequestException as e:
        print(f"請求失敗: {e}")
        raise


def upload_media_to_minio(media: list[model.Medium], bucket_name, minio_client):

    if not minio_client.bucket_exists(bucket_name):
        print(f"建立 Bucket: {bucket_name}")
        minio_client.make_bucket(bucket_name)

    for medium in media:
        try:
            minio_client.fput_object(bucket_name, medium.s3_file_name, medium.path)
        except minio.error.S3Error as e:
            print(f"上傳 {medium.s3_file_name} 失敗: {e}")
            raise


def get_perch_mount_name(perch_mount_id: uuid.UUID) -> str:
    url = urllib.parse.urljoin(
        envs.PERCHMOUNT_SYSTEM, PERCH_MOUNT_ENDPOINT % str(perch_mount_id)
    )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()["perch_mount_name"]
        else:
            print(f"Perch Mount 服務狀態異常，Status Code: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"無法連接到 Perch Mount 服務: {e}")
        raise
