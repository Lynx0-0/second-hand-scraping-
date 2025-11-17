import { useState } from 'react';
import SearchBar from './components/SearchBar';
import ProductGrid from './components/ProductGrid';
import api from './services/api';

function App() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchInfo, setSearchInfo] = useState(null);

  const handleSearch = async (searchParams) => {
    setLoading(true);
    setError(null);
    setListings([]);

    try {
      console.log('Ricerca con parametri:', searchParams);
      const response = await api.search(searchParams);

      console.log('Risultati ricevuti:', response);

      setListings(response.results || []);
      setSearchInfo({
        query: response.query,
        categoria: response.categoria,
        total: response.total_results,
        cached: response.cached,
        executionTime: response.execution_time_ms,
      });
    } catch (err) {
      console.error('Errore ricerca:', err);

      let errorMessage = 'Errore durante la ricerca. Riprova.';

      if (err.response) {
        // Errore dal server
        errorMessage = err.response.data?.message || err.response.data?.detail || errorMessage;
      } else if (err.request) {
        // Nessuna risposta dal server
        errorMessage = 'Impossibile connettersi al server. Verifica che l\'API sia attiva su http://localhost:8000';
      } else {
        errorMessage = err.message;
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                <span className="text-4xl">🔍</span>
                Subito Scraper
              </h1>
              <p className="text-gray-600 mt-1">
                Cerca annunci usati con rilevamento truffe automatico
              </p>
            </div>

            {/* API Status Indicator */}
            <div className="hidden md:block">
              <div className="flex items-center gap-2 px-4 py-2 bg-green-50 border border-green-200 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-800 font-medium">API Connessa</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Search Info */}
        {searchInfo && !loading && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex flex-wrap items-center gap-4 text-sm">
              <div>
                <span className="text-gray-600">Query:</span>
                <span className="font-semibold text-gray-900 ml-2">{searchInfo.query}</span>
              </div>
              {searchInfo.categoria && (
                <div>
                  <span className="text-gray-600">Categoria:</span>
                  <span className="font-semibold text-gray-900 ml-2">{searchInfo.categoria}</span>
                </div>
              )}
              <div>
                <span className="text-gray-600">Risultati:</span>
                <span className="font-semibold text-gray-900 ml-2">{searchInfo.total}</span>
              </div>
              <div>
                <span className="text-gray-600">Tempo:</span>
                <span className="font-semibold text-gray-900 ml-2">
                  {(searchInfo.executionTime / 1000).toFixed(2)}s
                </span>
              </div>
              {searchInfo.cached && (
                <div className="ml-auto">
                  <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-semibold">
                    ⚡ Da cache
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Product Grid */}
        <ProductGrid listings={listings} loading={loading} error={error} />

        {/* Empty State (initial) */}
        {!loading && !error && listings.length === 0 && !searchInfo && (
          <div className="text-center py-16">
            <div className="max-w-md mx-auto">
              <div className="text-6xl mb-6">🔍</div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                Inizia una ricerca
              </h2>
              <p className="text-gray-600 mb-6">
                Cerca annunci di prodotti usati su Subito.it. Il nostro sistema
                analizzerà automaticamente ogni annuncio per rilevare possibili truffe.
              </p>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-left">
                <h3 className="font-semibold text-yellow-900 mb-2 flex items-center gap-2">
                  <span>💡</span>
                  Suggerimenti
                </h3>
                <ul className="text-sm text-yellow-800 space-y-1">
                  <li>• Prova ricerche come "iPhone 13", "MacBook Pro", "Bicicletta"</li>
                  <li>• Usa i filtri per raffinare la ricerca</li>
                  <li>• Il badge rosso indica annunci ad alto rischio truffa</li>
                  <li>• Clicca sul badge per vedere i dettagli di sicurezza</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-600">
            <div>
              <p>
                ⚠️ Questo è un progetto educativo. Non affiliato con Subito.it.
              </p>
            </div>
            <div className="flex gap-6">
              <a href="/docs" className="hover:text-gray-900">API Docs</a>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-gray-900"
              >
                API Backend
              </a>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-gray-900"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
