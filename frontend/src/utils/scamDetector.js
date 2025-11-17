/**
 * Sistema di rilevamento truffe
 *
 * Analizza gli annunci e assegna uno score di rischio.
 * Score > 70: Alta probabilità di truffa
 * Score 40-70: Sospetto
 * Score < 40: Probabilmente legittimo
 */

/**
 * Calcola lo score di rischio truffa per un annuncio
 * @param {Object} listing - Annuncio da analizzare
 * @returns {Object} { score, reasons, riskLevel }
 */
export function calculateScamScore(listing) {
  let score = 0;
  const reasons = [];

  // 1. Analisi prezzo (peso alto)
  if (listing.price) {
    const priceAnalysis = analyzePriceRisk(listing);
    score += priceAnalysis.score;
    if (priceAnalysis.reason) reasons.push(priceAnalysis.reason);
  }

  // 2. Analisi titolo
  const titleAnalysis = analyzeTitleRisk(listing.title);
  score += titleAnalysis.score;
  if (titleAnalysis.reason) reasons.push(titleAnalysis.reason);

  // 3. Analisi descrizione
  if (listing.description) {
    const descAnalysis = analyzeDescriptionRisk(listing.description);
    score += descAnalysis.score;
    if (descAnalysis.reason) reasons.push(descAnalysis.reason);
  }

  // 4. Analisi foto
  if (listing.photos) {
    const photoAnalysis = analyzePhotosRisk(listing.photos);
    score += photoAnalysis.score;
    if (photoAnalysis.reason) reasons.push(photoAnalysis.reason);
  }

  // 5. Analisi location
  if (listing.location) {
    const locationAnalysis = analyzeLocationRisk(listing.location);
    score += locationAnalysis.score;
    if (locationAnalysis.reason) reasons.push(locationAnalysis.reason);
  }

  // 6. Analisi venditore
  if (listing.seller_name) {
    const sellerAnalysis = analyzeSellerRisk(listing);
    score += sellerAnalysis.score;
    if (sellerAnalysis.reason) reasons.push(sellerAnalysis.reason);
  }

  // Determina livello di rischio
  let riskLevel;
  if (score >= 70) {
    riskLevel = 'high';
  } else if (score >= 40) {
    riskLevel = 'medium';
  } else {
    riskLevel = 'low';
  }

  return {
    score: Math.min(100, Math.max(0, score)),
    reasons,
    riskLevel,
  };
}

/**
 * Analizza rischio basato sul prezzo
 */
function analyzePriceRisk(listing) {
  const { price, title, price_text } = listing;

  // Prezzi sospettosamente bassi per prodotti costosi
  const expensiveKeywords = {
    iphone: { normal_min: 300, weight: 30 },
    macbook: { normal_min: 600, weight: 30 },
    'playstation 5': { normal_min: 350, weight: 30 },
    'ps5': { normal_min: 350, weight: 30 },
    'samsung s23': { normal_min: 400, weight: 25 },
    'rolex': { normal_min: 2000, weight: 40 },
    'louis vuitton': { normal_min: 500, weight: 35 },
  };

  const titleLower = title.toLowerCase();

  for (const [keyword, config] of Object.entries(expensiveKeywords)) {
    if (titleLower.includes(keyword)) {
      if (price < config.normal_min * 0.3) {
        // Prezzo < 30% del valore normale
        return {
          score: config.weight,
          reason: `Prezzo sospettosamente basso per ${keyword} (€${price})`,
        };
      } else if (price < config.normal_min * 0.5) {
        // Prezzo < 50% del valore normale
        return {
          score: config.weight * 0.6,
          reason: `Prezzo molto conveniente per ${keyword}, verifica autenticità`,
        };
      }
    }
  }

  // Prezzo = 1 euro (spesso truffa)
  if (price === 1) {
    return {
      score: 25,
      reason: 'Prezzo simbolico (€1), contatta venditore per prezzo reale',
    };
  }

  // Prezzo troppo tondo per prodotti costosi
  if (price >= 500 && price % 100 === 0) {
    return {
      score: 5,
      reason: 'Prezzo molto tondo per prodotto costoso',
    };
  }

  return { score: 0, reason: null };
}

/**
 * Analizza rischio nel titolo
 */
function analyzeTitleRisk(title) {
  const suspiciousKeywords = [
    { words: ['nuovo', 'sigillato', 'scontato'], score: 10, reason: 'Promesse troppo allettanti' },
    { words: ['urgente', 'affare'], score: 8, reason: 'Senso di urgenza sospetto' },
    { words: ['originale', '100% originale'], score: 5, reason: 'Enfasi eccessiva su originalità' },
    { words: ['garanzia', 'scontrino'], score: -5, reason: null }, // Positivo
  ];

  const titleLower = title.toLowerCase();
  let maxScore = 0;
  let reason = null;

  for (const { words, score: keywordScore, reason: keywordReason } of suspiciousKeywords) {
    for (const word of words) {
      if (titleLower.includes(word)) {
        if (Math.abs(keywordScore) > Math.abs(maxScore)) {
          maxScore = keywordScore;
          reason = keywordReason;
        }
      }
    }
  }

  return { score: maxScore, reason };
}

/**
 * Analizza rischio nella descrizione
 */
function analyzeDescriptionRisk(description) {
  if (!description || description.length < 20) {
    return {
      score: 15,
      reason: 'Descrizione molto breve o assente',
    };
  }

  const descLower = description.toLowerCase();

  // Red flags nella descrizione
  const redFlags = [
    { pattern: /pagament[oi] antic/i, score: 35, reason: 'Richiesta pagamento anticipato' },
    { pattern: /western union|moneygram|ricarica/i, score: 40, reason: 'Metodo di pagamento non tracciabile' },
    { pattern: /spedizion[ei] grat/i, score: 10, reason: 'Spedizione gratuita per oggetto costoso' },
    { pattern: /whatsapp|telegram/i, score: 15, reason: 'Richiesta di contatto esterno alla piattaforma' },
    { pattern: /no perditempo|solo interessat/i, score: 8, reason: 'Tono aggressivo' },
  ];

  for (const { pattern, score, reason } of redFlags) {
    if (pattern.test(descLower)) {
      return { score, reason };
    }
  }

  return { score: 0, reason: null };
}

/**
 * Analizza rischio dalle foto
 */
function analyzePhotosRisk(photos) {
  if (!photos || photos.length === 0) {
    return {
      score: 20,
      reason: 'Nessuna foto disponibile',
    };
  }

  if (photos.length === 1) {
    return {
      score: 10,
      reason: 'Solo una foto disponibile',
    };
  }

  // Photo URLs che sembrano stock/scaricate
  const stockPhotoIndicators = ['placeholder', 'stock', 'default'];
  for (const photo of photos) {
    for (const indicator of stockPhotoIndicators) {
      if (photo.toLowerCase().includes(indicator)) {
        return {
          score: 15,
          reason: 'Foto potrebbero essere stock/scaricate',
        };
      }
    }
  }

  return { score: 0, reason: null };
}

/**
 * Analizza rischio dalla location
 */
function analyzeLocationRisk(location) {
  // Location generica o sospetta
  if (!location || location.length < 3) {
    return {
      score: 10,
      reason: 'Località non specificata',
    };
  }

  const suspiciousLocations = ['italia', 'tutta italia', 'everywhere'];
  const locationLower = location.toLowerCase();

  for (const suspicious of suspiciousLocations) {
    if (locationLower.includes(suspicious)) {
      return {
        score: 12,
        reason: 'Località troppo generica',
      };
    }
  }

  return { score: 0, reason: null };
}

/**
 * Analizza rischio dal venditore
 */
function analyzeSellerRisk(listing) {
  const { seller_name, seller_type } = listing;

  // Nome venditore sospetto
  if (!seller_name || seller_name.length < 3) {
    return {
      score: 8,
      reason: 'Nome venditore non specificato',
    };
  }

  // Pattern sospetti nel nome
  const suspiciousPatterns = [
    /^user\d+$/i,
    /^account\d+$/i,
    /^[a-z]{20,}$/i, // Stringhe casuali lunghe
  ];

  for (const pattern of suspiciousPatterns) {
    if (pattern.test(seller_name)) {
      return {
        score: 12,
        reason: 'Nome venditore sospetto',
      };
    }
  }

  return { score: 0, reason: null };
}

/**
 * Ottiene colore e icona basati sul livello di rischio
 */
export function getRiskDisplay(riskLevel) {
  const displays = {
    high: {
      color: 'red',
      bgColor: 'bg-red-100',
      textColor: 'text-red-800',
      borderColor: 'border-red-300',
      label: 'ATTENZIONE TRUFFA',
      icon: '⚠️',
    },
    medium: {
      color: 'yellow',
      bgColor: 'bg-yellow-100',
      textColor: 'text-yellow-800',
      borderColor: 'border-yellow-300',
      label: 'SOSPETTO',
      icon: '⚡',
    },
    low: {
      color: 'green',
      bgColor: 'bg-green-100',
      textColor: 'text-green-800',
      borderColor: 'border-green-300',
      label: 'Verificato',
      icon: '✓',
    },
  };

  return displays[riskLevel] || displays.low;
}
