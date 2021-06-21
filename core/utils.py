from core.coretypes import COUNTRY_EMOJI


def get_country_emoji(country: str) -> str:
    return COUNTRY_EMOJI.get(country.lower(), "🏳️‍🌈")
