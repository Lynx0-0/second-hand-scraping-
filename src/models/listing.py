"""Modello dati per rappresentare un annuncio."""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime
import json


@dataclass
class Listing:
    """Rappresenta un annuncio di un articolo usato."""

    title: str
    price: Optional[float] = None
    price_text: Optional[str] = None  # Prezzo come testo (es. "Gratis", "Contattami")
    description: Optional[str] = None
    link: Optional[str] = None
    photos: List[str] = field(default_factory=list)
    location: Optional[str] = None
    category: Optional[str] = None
    posted_date: Optional[str] = None
    seller_name: Optional[str] = None
    seller_type: Optional[str] = None  # "privato" o "professionale"
    listing_id: Optional[str] = None
    scraped_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Converte l'annuncio in dizionario."""
        data = asdict(self)
        data['scraped_at'] = self.scraped_at.isoformat()
        return data

    def to_json(self, indent: int = 2) -> str:
        """Converte l'annuncio in JSON."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Listing':
        """Crea un Listing da un dizionario."""
        if 'scraped_at' in data and isinstance(data['scraped_at'], str):
            data['scraped_at'] = datetime.fromisoformat(data['scraped_at'])
        return cls(**data)

    def __str__(self) -> str:
        """Rappresentazione stringa dell'annuncio."""
        price_str = f"€{self.price}" if self.price else self.price_text or "N/A"
        return f"Listing(title='{self.title[:50]}...', price={price_str}, link={self.link})"

    def is_valid(self) -> bool:
        """Verifica se l'annuncio ha i dati minimi necessari."""
        return bool(self.title and (self.link or self.listing_id))
