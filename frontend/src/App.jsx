import { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import ProductGrid from './components/ProductGrid';
import SearchProgress from './components/SearchProgress';
import api from './services/api';

function App() {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchInfo, setSearchInfo] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');
  const [stats, setStats] = useState({
    totalSearches: 0,
    currentSession: 0,
  });

  // Check API status on mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        await api.healthCheck();
        setApiStatus('connected');
      } catch {
        setApiStatus('disconnected');
      }
    };

    checkApiHealth();
    // Check every 30 seconds
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, []);

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

      // Update stats
      setStats((prev) => ({
        totalSearches: prev.totalSearches + 1,
        currentSession: prev.currentSession + 1,
      }));
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
      setApiStatus('disconnected');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 flex items-center gap-3">
                <span className="text-5xl">🔍</span>
                Subito Scraper
              </h1>
              <p className="text-gray-600 mt-2 text-base">
                Cerca annunci usati con rilevamento truffe automatico intelligente
              </p>
            </div>

            {/* Stats & API Status */}
            <div className="hidden md:flex flex-col gap-2">
              {/* API Status Indicator */}
              <div
                className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                  apiStatus === 'connected'
                    ? 'bg-green-50 border-green-200'
                    : apiStatus === 'disconnected'
                    ? 'bg-red-50 border-red-200'
                    : 'bg-yellow-50 border-yellow-200'
                }`}
              >
                <div
                  className={`w-2.5 h-2.5 rounded-full ${
                    apiStatus === 'connected'
                      ? 'bg-green-500 animate-pulse'
                      : apiStatus === 'disconnected'
                      ? 'bg-red-500'
                      : 'bg-yellow-500 animate-pulse'
                  }`}
                ></div>
                <span
                  className={`text-sm font-semibold ${
                    apiStatus === 'connected'
                      ? 'text-green-800'
                      : apiStatus === 'disconnected'
                      ? 'text-red-800'
                      : 'text-yellow-800'
                  }`}
                >
                  {apiStatus === 'connected'
                    ? '✓ API Connessa'
                    : apiStatus === 'disconnected'
                    ? '✗ API Offline'
                    : '⟳ Controllo...'}
                </span>
              </div>

              {/* Session Stats */}
              {stats.currentSession > 0 && (
                <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg">
                  <span className="text-2xl">📊</span>
                  <span className="text-sm text-blue-800 font-medium">
                    {stats.currentSession} ricerca{stats.currentSession > 1 ? 'he' : ''} effettuata
                    {stats.currentSession > 1 ? 'e' : ''}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Search Progress */}
        <SearchProgress isSearching={loading} />

        {/* Search Info - Enhanced */}
        {searchInfo && !loading && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-5 mb-6 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                <span className="text-2xl">✅</span>
                Ricerca Completata
              </h3>
              {searchInfo.cached && (
                <span className="px-3 py-1.5 bg-purple-100 text-purple-800 rounded-full text-xs font-bold flex items-center gap-1">
                  <span className="text-base">⚡</span>
                  RISULTATI DA CACHE
                </span>
              )}
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-lg p-3 border border-blue-100">
                <div className="text-xs text-gray-500 mb-1">Query</div>
                <div className="font-bold text-gray-900 truncate">{searchInfo.query}</div>
              </div>
              {searchInfo.categoria && (
                <div className="bg-white rounded-lg p-3 border border-blue-100">
                  <div className="text-xs text-gray-500 mb-1">Categoria</div>
                  <div className="font-bold text-gray-900 truncate">{searchInfo.categoria}</div>
                </div>
              )}
              <div className="bg-white rounded-lg p-3 border border-blue-100">
                <div className="text-xs text-gray-500 mb-1">Risultati Trovati</div>
                <div className="font-bold text-blue-600 text-xl">{searchInfo.total}</div>
              </div>
              <div className="bg-white rounded-lg p-3 border border-blue-100">
                <div className="text-xs text-gray-500 mb-1">Tempo Esecuzione</div>
                <div className="font-bold text-green-600 text-xl">
                  {(searchInfo.executionTime / 1000).toFixed(2)}s
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Product Grid */}
        <ProductGrid listings={listings} loading={loading} error={error} />

        {/* Empty State (initial) - Enhanced */}
        {!loading && !error && listings.length === 0 && !searchInfo && (
          <div className="text-center py-12">
            <div className="max-w-3xl mx-auto">
              {/* Hero Section */}
              <div className="mb-8">
                <div className="text-7xl mb-6 animate-bounce">🔍</div>
                <h2 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-4">
                  Benvenuto su Subito Scraper
                </h2>
                <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
                  Il tuo assistente intelligente per cercare annunci di prodotti usati su Subito.it
                  con un potente sistema di <span className="font-bold text-blue-600">rilevamento truffe automatico</span>.
                </p>
              </div>

              {/* Features Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
                  <div className="text-4xl mb-3">🛡️</div>
                  <h3 className="font-bold text-gray-900 mb-2">Protezione Anti-Truffa</h3>
                  <p className="text-sm text-gray-600">
                    Analisi automatica degli annunci per rilevare possibili truffe
                  </p>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
                  <div className="text-4xl mb-3">⚡</div>
                  <h3 className="font-bold text-gray-900 mb-2">Risultati Veloci</h3>
                  <p className="text-sm text-gray-600">
                    Cache intelligente per risposte istantanee
                  </p>
                </div>
                <div className="bg-white rounded-xl p-6 shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
                  <div className="text-4xl mb-3">🎯</div>
                  <h3 className="font-bold text-gray-900 mb-2">Filtri Avanzati</h3>
                  <p className="text-sm text-gray-600">
                    Categoria, prezzo e regione per risultati precisi
                  </p>
                </div>
              </div>

              {/* Tips Section */}
              <div className="bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-xl p-6 text-left shadow-md">
                <h3 className="font-bold text-yellow-900 mb-4 flex items-center gap-2 text-lg">
                  <span className="text-2xl">💡</span>
                  Come iniziare
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-yellow-800 mb-2 flex items-center gap-2">
                      <span>🔸</span>
                      Suggerimenti di Ricerca
                    </h4>
                    <ul className="text-sm text-yellow-800 space-y-1.5">
                      <li>• Prova: "iPhone 13", "MacBook Pro", "Bicicletta"</li>
                      <li>• Sii specifico per risultati migliori</li>
                      <li>• Usa i filtri per raffinare la ricerca</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-yellow-800 mb-2 flex items-center gap-2">
                      <span>🔸</span>
                      Indicatori di Sicurezza
                    </h4>
                    <ul className="text-sm text-yellow-800 space-y-1.5">
                      <li>• <span className="font-bold text-red-600">Badge Rosso</span>: Alto rischio truffa</li>
                      <li>• <span className="font-bold text-yellow-600">Badge Giallo</span>: Medio rischio</li>
                      <li>• Clicca sul badge per vedere i dettagli</li>
                    </ul>
                  </div>
                </div>
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
