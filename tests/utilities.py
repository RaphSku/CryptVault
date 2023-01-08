import os


def cleanup_base_path():
    base_path = os.path.expanduser("~/cryptvault")
    os.remove(f"{base_path}/test_secrets.parquet")
    os.remove(f"{base_path}/test.txt")
    os.rmdir(f"{base_path}")