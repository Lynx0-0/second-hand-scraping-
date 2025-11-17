/**
 * API Service per comunicare con il backend FastAPI
 */

import axios from 'axios';

// Base URL dell'API - modificare in produzione
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Crea istanza axios con configurazione
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor per logging (opzionale)
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor per gestione errori
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Errore dal server
      console.error('[API Error]', error.response.data);

      // Gestione rate limiting
      if (error.response.status === 429) {
        const retryAfter = error.response.headers['retry-after'] || 60;
        error.message = `Troppo richieste. Riprova tra ${retryAfter} secondi.`;
      }
    } else if (error.request) {
      // Nessuna risposta dal server
      error.message = 'Impossibile connettersi al server. Verifica la connessione.';
    }
    return Promise.reject(error);
  }
);

/**
 * API Service
 */
const api = {
  /**
   * Cerca annunci
   * @param {Object} params - Parametri ricerca
   * @param {string} params.query - Query di ricerca
   * @param {string} [params.categoria] - Categoria
   * @param {number} [params.prezzo_max] - Prezzo massimo
   * @param {string} [params.regione] - Regione
   * @param {number} [params.max_pages] - Numero pagine (default: 1)
   * @returns {Promise} Risultati ricerca
   */
  search: async (params) => {
    const response = await apiClient.post('/api/v1/search', params);
    return response.data;
  },

  /**
   * Recupera risultati per search_id
   * @param {string} searchId - ID della ricerca
   * @returns {Promise} Risultati
   */
  getSearchResults: async (searchId) => {
    const response = await apiClient.get(`/api/v1/results/${searchId}`);
    return response.data;
  },

  /**
   * Recupera dettagli listing
   * @param {string} listingId - ID dell'annuncio
   * @returns {Promise} Dettagli annuncio
   */
  getListing: async (listingId) => {
    const response = await apiClient.get(`/api/v1/listing/${listingId}`);
    return response.data;
  },

  /**
   * Segnala annuncio sospetto
   * @param {Object} report - Dati segnalazione
   * @param {string} report.listing_id - ID annuncio
   * @param {string} report.listing_url - URL annuncio
   * @param {string} report.reason - Motivo
   * @param {string} [report.reporter_email] - Email
   * @param {string} [report.additional_info] - Info aggiuntive
   * @returns {Promise} Conferma segnalazione
   */
  reportScam: async (report) => {
    const response = await apiClient.post('/api/v1/report-scam', report);
    return response.data;
  },

  /**
   * Health check
   * @returns {Promise} Status API
   */
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default api;
