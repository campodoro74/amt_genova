DOMAIN = "amt_genova"

DEFAULT_SCAN_INTERVAL = 30

AMT_XML_URL = (
    "https://www.amt.genova.it/amt/servizi/passaggi_xml.php"
)

# Stop ID to name mapping
STOP_NAMES = {
    "0731": "Prasca / Chiesa",
    "0732": "Carrara 1 / Prasca",
    "0730": "Prasca",
    "0733": "Carrara 2",
    "2386": "Piazza Principe",
    "2385": "Via Balbi",
    "2384": "Via Gramsci",
    "2563": "Via Fiume",
    "2564": "Via D'Annunzio",
    "2565": "Via XX Settembre",
    "2383": "Via Assarotti",
    "2381": "Via Doria",
    "2387": "Via del Tritone",
    "2388": "Via Carrara",
    "2395": "Piazza Caricamento",
    "2396": "Via del Molo",
    "2397": "Via del Campo",
    "0418": "Via Garibaldi",
    "2398": "Via San Lorenzo",
    "2399": "Via del Portello",
    "0399": "Via delle Fontane",
    "0400": "Via delle Grazie",
    "0401": "Via delle Vigne",
    "0402": "Via delle Palme",
}


def get_stop_name(stop_id: str) -> str:
    """Get stop name from stop ID, or return the ID if not found."""
    return STOP_NAMES.get(stop_id, stop_id)

