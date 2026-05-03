import api
import envs
import read
import minio
import os

BUCKET_NAME = "perchmount"
NEW_DATA_DIR = "./new-data"
TMP_DIR = "./tmp"

minio_client = minio.Minio(
    envs.MINIO_URL,
    access_key=envs.MINIO_ACCESS_KEY,
    secret_key=envs.MINIO_SECRET_KEY,
    secure=False,
)


def upload():
    section = read.read_json_from_tmp()
    perch_mount_name = api.get_perch_mount_name(section["perch_mount_id"])
    media = read.get_media_from_tmp(perch_mount_name)

    json_media = [m.json() for m in media]
    api.upload_media_to_minio(media, BUCKET_NAME, minio_client)
    api.post_new_data(section["id"], json_media)


def main():

    os.makedirs(NEW_DATA_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)

    perch_mount_alive = api.is_perch_mount_service_alive()
    minio_alive = api.is_minio_alive()

    if not perch_mount_alive or not minio_alive:
        print("Is perch mount service alive?: %s" % perch_mount_alive)
        print("Is MinIO service alive?: %s" % minio_alive)
        return

    for section_tar in os.listdir(NEW_DATA_DIR):
        if os.path.isfile(
            os.path.join(NEW_DATA_DIR, section_tar)
        ) and section_tar.lower().endswith(".tar"):

            try:
                section_tar_path = os.path.join(NEW_DATA_DIR, section_tar)
                read.clear_tmp_directory()
                read.extract_tar_simple(section_tar_path)
                upload()
                os.remove(section_tar_path)
            except:
                os.replace(
                    section_tar_path,
                    os.path.join("./failed", os.path.basename(section_tar_path)),
                )


if __name__ == "__main__":
    main()
