import { useState } from 'react';

const CATEGORIES = [
  { value: '', label: 'Tutte le categorie' },
  { value: 'elettronica', label: 'Elettronica' },
  { value: 'telefonia', label: 'Telefonia' },
  { value: 'informatica', label: 'Informatica' },
  { value: 'arredamento-casalinghi', label: 'Arredamento' },
  { value: 'console-videogiochi', label: 'Console & Videogiochi' },
  { value: 'fotografia', label: 'Fotografia' },
  { value: 'libri-riviste', label: 'Libri & Riviste' },
  { value: 'strumenti-musicali', label: 'Strumenti Musicali' },
  { value: 'abbigliamento-accessori', label: 'Abbigliamento' },
  { value: 'biciclette', label: 'Biciclette' },
  { value: 'sport', label: 'Sport' },
  { value: 'auto', label: 'Auto' },
  { value: 'moto', label: 'Moto' },
];

const REGIONS = [
  'Abruzzo', 'Basilicata', 'Calabria', 'Campania', 'Emilia-Romagna',
  'Friuli-Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche',
  'Molise', 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana',
  'Trentino-Alto Adige', 'Umbria', 'Valle d\'Aosta', 'Veneto'
];

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');
  const [categoria, setCategoria] = useState('');
  const [prezzoMax, setPrezzoMax] = useState('');
  const [regione, setRegione] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!query.trim()) {
      alert('Inserisci una query di ricerca');
      return;
    }

    const searchParams = {
      query: query.trim(),
      max_pages: 2, // Default 2 pages
    };

    if (categoria) searchParams.categoria = categoria;
    if (prezzoMax) searchParams.prezzo_max = parseFloat(prezzoMax);
    if (regione) searchParams.regione = regione.toLowerCase();

    onSearch(searchParams);
  };

  const handleReset = () => {
    setQuery('');
    setCategoria('');
    setPrezzoMax('');
    setRegione('');
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6">
      <form onSubmit={handleSubmit}>
        {/* Search Input */}
        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Cerca prodotti usati (es. iPhone 13, bicicletta, PS5...)"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Cerco...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Cerca
              </span>
            )}
          </button>

          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
          </button>
        </div>

        {/* Filters */}
        {showFilters && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Categoria
              </label>
              <select
                value={categoria}
                onChange={(e) => setCategoria(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat.value} value={cat.value}>
                    {cat.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Prezzo massimo (€)
              </label>
              <input
                type="number"
                value={prezzoMax}
                onChange={(e) => setPrezzoMax(e.target.value)}
                placeholder="es. 500"
                min="0"
                step="10"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Regione
              </label>
              <select
                value={regione}
                onChange={(e) => setRegione(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              >
                <option value="">Tutta Italia</option>
                {REGIONS.map((reg) => (
                  <option key={reg} value={reg}>
                    {reg}
                  </option>
                ))}
              </select>
            </div>

            <div className="md:col-span-3 flex justify-end gap-2">
              <button
                type="button"
                onClick={handleReset}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                disabled={loading}
              >
                Reset filtri
              </button>
            </div>
          </div>
        )}
      </form>

      {/* Active Filters Display */}
      {(categoria || prezzoMax || regione) && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600">Filtri attivi:</span>
            {categoria && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                {CATEGORIES.find(c => c.value === categoria)?.label}
                <button
                  onClick={() => setCategoria('')}
                  className="ml-2 hover:text-blue-900"
                >
                  ×
                </button>
              </span>
            )}
            {prezzoMax && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                Max €{prezzoMax}
                <button
                  onClick={() => setPrezzoMax('')}
                  className="ml-2 hover:text-blue-900"
                >
                  ×
                </button>
              </span>
            )}
            {regione && (
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                {regione}
                <button
                  onClick={() => setRegione('')}
                  className="ml-2 hover:text-blue-900"
                >
                  ×
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
