from pathlib import Path
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(
    prefix="/theme",
    tags=["Theme"]
)


BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
THEME_FILE = STORAGE_DIR / "theme.json"


ALLOWED_THEMES = {
    "sky",
    "green",
    "purple",
    "orange",
    "red",
    "dark",
}


class ThemeRequest(BaseModel):
    theme: str


def ensure_theme_file():

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not THEME_FILE.exists():

        THEME_FILE.write_text(
            json.dumps(
                {
                    "theme": "sky"
                },
                indent=4
            ),
            encoding="utf-8"
        )


def read_theme():

    ensure_theme_file()

    try:

        content = THEME_FILE.read_text(
            encoding="utf-8"
        )

        data = json.loads(content)

        theme = data.get(
            "theme",
            "sky"
        )

        if theme not in ALLOWED_THEMES:
            return "sky"

        return theme

    except Exception:

        return "sky"


def write_theme(theme: str):

    ensure_theme_file()

    THEME_FILE.write_text(
        json.dumps(
            {
                "theme": theme
            },
            indent=4
        ),
        encoding="utf-8"
    )


@router.get("/")
def get_theme():

    return {
        "success": True,
        "theme": read_theme()
    }


@router.post("/")
def save_theme(payload: ThemeRequest):

    theme = payload.theme.lower().strip()

    if theme not in ALLOWED_THEMES:

        raise HTTPException(
            status_code=400,
            detail="Invalid theme"
        )

    write_theme(theme)

    return {
        "success": True,
        "theme": theme
    }

