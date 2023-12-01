from datetime import UTC, datetime, timedelta
from typing import Any

from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, HTTPException, status

from src.secret import utils
from src.secret.repository import SecretRepository
from src.secret.schemas import (
    SecretGenerateIn,
    SecretGenerateOut,
    SecretGetIn,
    SecretGetOut,
)

router = APIRouter()


@router.post(
    "/generate", status_code=status.HTTP_201_CREATED, response_model=SecretGenerateOut
)
async def generate_secret(secret: SecretGenerateIn) -> Any:
    secret_key = utils.generate_secret_key()
    hash_passphrase = utils.get_hash(password=secret.passphrase)
    encrypted_message = utils.encrypt(secret.secret_message, secret.passphrase)

    expire = secret.ttl or 3600

    await SecretRepository.add(
        secret_key=secret_key,
        secret_message=encrypted_message,
        passphrase=hash_passphrase,
        expires_at=datetime.now(tz=UTC) + timedelta(seconds=expire),
    )
    return {"secret_key": secret_key}


@router.post("/secrets/{secret_key}", response_model=SecretGetOut)
async def get_secret(secret_key: str, passphrase: SecretGetIn) -> Any:
    secret = await SecretRepository.get_one_or_none(secret_key=secret_key)
    if not secret:
        raise HTTPException(
            status_code=404,
            detail="It either never existed or has already been viewed.",
        )

    try:
        utils.check_hash(password=passphrase.passphrase, known_hash=secret.passphrase)
    except VerifyMismatchError as e:
        raise HTTPException(
            status_code=404,
            detail=f"It either never existed or has already been viewed: {e}.",
        ) from e

    if secret.expires_at < datetime.now(tz=UTC):
        await SecretRepository.delete(id=secret.id)
        raise HTTPException(
            status_code=410,
            detail="The secret retention time has expired.",
        )

    decrypted_message = utils.decrypt(secret.secret_message, passphrase.passphrase)

    await SecretRepository.delete(id=secret.id)

    return {"secret_message": decrypted_message}
