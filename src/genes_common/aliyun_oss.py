"""Aliyun OSS helper utilities.

This module provides CRUD operations for Aliyun Object Storage Service (OSS)
using the official `oss2` SDK.

Environment variables required:
    ALIYUN_OSS_ENDPOINT
    ALIYUN_OSS_BUCKET
    ALIYUN_ACCESS_KEY_ID
    ALIYUN_ACCESS_KEY_SECRET

Example:
    from genes_common.aliyun_oss import OSSClient
    client = OSSClient()
    client.upload_file('local.jpg', 'images/local.jpg')
"""
from __future__ import annotations

import os
import logging
from typing import List, Optional

import oss2  # type: ignore

logger = logging.getLogger(__name__)

__all__ = ["OSSClient"]


class OSSClient:
    """Simple wrapper around Aliyun OSS Bucket providing basic CRUD."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        bucket_name: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
    ) -> None:
        self.endpoint = endpoint or os.getenv("ALIYUN_OSS_ENDPOINT")
        self.bucket_name = bucket_name or os.getenv("ALIYUN_OSS_BUCKET")
        self.access_key_id = access_key_id or os.getenv("ALIYUN_ACCESS_KEY_ID")
        self.access_key_secret = access_key_secret or os.getenv("ALIYUN_ACCESS_KEY_SECRET")

        if not all(
            [self.endpoint, self.bucket_name, self.access_key_id, self.access_key_secret]
        ):
            raise ValueError("Missing Aliyun OSS credentials (endpoint/bucket/access keys).")

        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        logger.info("OSS client ready for bucket '%s'", self.bucket_name)

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------
    def upload_file(self, local_path: str, object_name: str) -> bool:
        logger.debug("Uploading %s to OSS as %s", local_path, object_name)
        res = self.bucket.put_object_from_file(object_name, local_path)
        return res.status == 200

    def download_file(self, object_name: str, local_path: str) -> bool:
        logger.debug("Downloading %s to %s", object_name, local_path)
        res = self.bucket.get_object_to_file(object_name, local_path)
        return res.status == 200

    def delete_object(self, object_name: str) -> bool:
        logger.debug("Deleting OSS object %s", object_name)
        res = self.bucket.delete_object(object_name)
        return res.status == 204

    def list_objects(self, prefix: str = "", max_keys: int = 1000) -> List[str]:
        logger.debug("Listing objects under prefix '%s'", prefix)
        keys: List[str] = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix, max_keys=max_keys):
            keys.append(obj.key)
        return keys 