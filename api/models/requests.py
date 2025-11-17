"""Modelli Pydantic per le richieste API."""

from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional
from enum import Enum


class PlatformEnum(str, Enum):
    """Piattaforme supportate."""
    SUBITO = "subito"
    EBAY = "ebay"
    ALL = "all"  # Cerca su entrambe


class CategoryEnum(str, Enum):
    """Categorie supportate da Subito.it."""
    ELETTRONICA = "elettronica"
    TELEFONIA = "telefonia"
    INFORMATICA = "informatica"
    ARREDAMENTO = "arredamento-casalinghi"
    CONSOLE_VIDEOGIOCHI = "console-videogiochi"
    FOTOGRAFIA = "fotografia"
    LIBRI_RIVISTE = "libri-riviste"
    STRUMENTI_MUSICALI = "strumenti-musicali"
    ABBIGLIAMENTO = "abbigliamento-accessori"
    TUTTO = "tutto"
    BICICLETTE = "biciclette"
    SPORT = "sport"
    AUTO = "auto"
    MOTO = "moto"


class SearchRequest(BaseModel):
    """Modello per richiesta di ricerca annunci."""

    query: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Query di ricerca",
        example="iphone 13"
    )

    platform: PlatformEnum = Field(
        PlatformEnum.SUBITO,
        description="Piattaforma di ricerca (subito/ebay/all)",
        example="subito"
    )

    categoria: Optional[CategoryEnum] = Field(
        None,
        description="Categoria di ricerca",
        example="telefonia"
    )

    prezzo_max: Optional[float] = Field(
        None,
        gt=0,
        le=1000000,
        description="Prezzo massimo in euro",
        example=500.0
    )

    regione: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Regione di ricerca (solo per Subito.it)",
        example="lazio"
    )

    max_pages: int = Field(
        1,
        ge=1,
        le=5,
        description="Numero massimo di pagine da scansionare (max 5)",
        example=2
    )

    @validator('query')
    def validate_query(cls, v):
        """Valida che la query non contenga caratteri speciali pericolosi."""
        if not v or not v.strip():
            raise ValueError("La query non può essere vuota")

        # Rimuovi spazi multipli
        v = ' '.join(v.split())

        # Blocca caratteri potenzialmente pericolosi
        dangerous_chars = ['<', '>', ';', '&', '|', '$', '`']
        if any(char in v for char in dangerous_chars):
            raise ValueError("La query contiene caratteri non validi")

        return v.strip()

    @validator('regione')
    def validate_regione(cls, v):
        """Normalizza il nome della regione."""
        if v:
            return v.lower().strip()
        return v

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "query": "iphone 13",
                "categoria": "telefonia",
                "prezzo_max": 500.0,
                "regione": "lazio",
                "max_pages": 2
            }
        }


class ReportScamRequest(BaseModel):
    """Modello per segnalazione di annunci sospetti."""

    listing_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="ID univoco dell'annuncio",
        example="12345678"
    )

    listing_url: HttpUrl = Field(
        ...,
        description="URL completo dell'annuncio",
        example="https://www.subito.it/annunci/12345678.htm"
    )

    reason: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Motivo della segnalazione",
        example="Prezzo troppo basso, probabilmente truffa"
    )

    reporter_email: Optional[str] = Field(
        None,
        max_length=100,
        description="Email del segnalante (opzionale)",
        example="user@example.com"
    )

    additional_info: Optional[str] = Field(
        None,
        max_length=2000,
        description="Informazioni aggiuntive",
    )

    @validator('listing_url')
    def validate_listing_url(cls, v):
        """Valida che l'URL sia di una piattaforma supportata."""
        url_str = str(v).lower()
        supported_platforms = ['subito.it', 'ebay.it', 'ebay.com']
        if not any(platform in url_str for platform in supported_platforms):
            raise ValueError("L'URL deve essere di una piattaforma supportata (Subito.it o eBay)")
        return v

    @validator('reporter_email')
    def validate_email(cls, v):
        """Validazione base dell'email."""
        if v and '@' not in v:
            raise ValueError("Email non valida")
        return v

    @validator('reason')
    def validate_reason(cls, v):
        """Valida il motivo della segnalazione."""
        if not v or not v.strip():
            raise ValueError("Il motivo non può essere vuoto")

        # Blocca spam/test
        spam_words = ['test', 'spam', 'prova']
        if v.lower().strip() in spam_words:
            raise ValueError("Motivo non valido")

        return v.strip()

    class Config:
        """Configurazione Pydantic."""
        schema_extra = {
            "example": {
                "listing_id": "12345678",
                "listing_url": "https://www.subito.it/telefonia/iphone-13-roma-12345678.htm",
                "reason": "Il venditore chiede pagamento anticipato su carta prepagata, sospetto truffa",
                "reporter_email": "user@example.com",
                "additional_info": "L'annuncio ha foto rubate da altri siti"
            }
        }
