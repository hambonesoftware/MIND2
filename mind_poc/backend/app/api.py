import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.conflict_resolver import resolve_conflicts
from app.profiles import get_profile, list_profiles
from app.validators import SchemaValidationError, validate_schema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    logger.info("health_check")
    return {"status": "ok"}


@router.get("/profiles")
def profiles():
    logger.info("profiles_list")
    return {"profiles": list_profiles()}


def error_response(status_code, error_code, message, hint):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "error_code": error_code,
                "message": message,
                "hint": hint,
                "span": None
            }
        }
    )


@router.post("/resolve-conflict")
def resolve_conflict(payload: dict):
    logger.info(
        "resolve_conflict request style_profile=%s inputs=%d",
        payload.get("style_profile"),
        len(payload.get("inputs", [])),
    )
    if payload.get("schema_version") != "resolve.v0":
        return error_response(
            400,
            "SCHEMA_VERSION_UNSUPPORTED",
            "Unsupported schema version",
            "Use resolve.v0"
        )

    profile = get_profile(payload.get("style_profile"))
    if not profile:
        return error_response(
            400,
            "PROFILE_NOT_FOUND",
            "Profile not found",
            "Select a valid style profile"
        )

    for item in payload.get("inputs", []):
        thought = item.get("thought")
        try:
            validate_schema(thought, "thought.v0.schema.json")
        except SchemaValidationError as error:
            logger.warning("resolve_conflict schema validation failed: %s", error.message)
            return error_response(
                400,
                "SCHEMA_VALIDATION_ERROR",
                error.message,
                "Fix thought payload"
            )

    response = resolve_conflicts(payload, profile)
    try:
        validate_schema(response, "resolve.v0.schema.json")
    except SchemaValidationError as error:
        logger.error("resolve_conflict output invalid: %s", error.message)
        return error_response(
            500,
            "SCHEMA_VALIDATION_ERROR",
            error.message,
            "Resolve output invalid"
        )

    logger.info(
        "resolve_conflict complete clashes=%d actions=%d",
        response["meta"]["clashes_detected"],
        len(response["meta"]["actions"]),
    )
    return response
