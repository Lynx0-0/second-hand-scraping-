import { getRiskDisplay } from '../utils/scamDetector';
import { useState } from 'react';
import api from '../services/api';

export default function ScamModal({ listing, scamData, onClose }) {
  const [reporting, setReporting] = useState(false);
  const [reported, setReported] = useState(false);
  const [reportReason, setReportReason] = useState('');

  const { score, reasons, riskLevel } = scamData;
  const display = getRiskDisplay(riskLevel);

  const handleReport = async () => {
    if (!reportReason.trim()) {
      alert('Inserisci un motivo per la segnalazione');
      return;
    }

    setReporting(true);
    try {
      await api.reportScam({
        listing_id: listing.listing_id || 'unknown',
        listing_url: listing.link,
        reason: reportReason,
        additional_info: `Score automatico: ${score}/100. Motivi: ${reasons.join(', ')}`,
      });

      setReported(true);
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (error) {
      alert('Errore durante la segnalazione: ' + (error.response?.data?.message || error.message));
    } finally {
      setReporting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className={`${display.bgColor} ${display.borderColor} border-b-4 p-6`}>
          <div className="flex justify-between items-start">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="text-4xl">{display.icon}</span>
                <h2 className={`text-2xl font-bold ${display.textColor}`}>
                  {display.label}
                </h2>
              </div>
              <p className="text-gray-700 font-medium">
                Score di rischio: <span className="text-2xl font-bold">{score}/100</span>
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-3xl leading-none"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Annuncio Info */}
          <div className="mb-6">
            <h3 className="font-semibold text-lg mb-2">Annuncio Analizzato</h3>
            <p className="text-gray-700 line-clamp-2">{listing.title}</p>
            {listing.price && (
              <p className="text-xl font-bold text-gray-900 mt-1">€{listing.price}</p>
            )}
          </div>

          {/* Reasons */}
          {reasons.length > 0 && (
            <div className="mb-6">
              <h3 className="font-semibold text-lg mb-3">⚠️ Segnali di Allarme Rilevati</h3>
              <ul className="space-y-2">
                {reasons.map((reason, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-red-500 font-bold">•</span>
                    <span className="text-gray-700">{reason}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Safety Tips */}
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
            <h3 className="font-semibold text-lg mb-3 flex items-center gap-2">
              <span>💡</span>
              Consigli per Evitare Truffe
            </h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2">
                <span>✓</span>
                <span>Incontra il venditore di persona in luogo pubblico</span>
              </li>
              <li className="flex items-start gap-2">
                <span>✓</span>
                <span>Non pagare mai in anticipo o con metodi non tracciabili</span>
              </li>
              <li className="flex items-start gap-2">
                <span>✓</span>
                <span>Verifica l'autenticità del prodotto prima di pagare</span>
              </li>
              <li className="flex items-start gap-2">
                <span>✓</span>
                <span>Diffida di prezzi troppo bassi o offerte "troppo belle per essere vere"</span>
              </li>
              <li className="flex items-start gap-2">
                <span>✓</span>
                <span>Usa sistemi di pagamento con protezione acquirente</span>
              </li>
            </ul>
          </div>

          {/* Report Form */}
          {!reported ? (
            <div className="border-t pt-4">
              <h3 className="font-semibold text-lg mb-3">Segnala questo annuncio</h3>
              <p className="text-sm text-gray-600 mb-3">
                Aiutaci a mantenere la community sicura segnalando annunci sospetti.
              </p>
              <textarea
                value={reportReason}
                onChange={(e) => setReportReason(e.target.value)}
                placeholder="Descrivi perché ritieni questo annuncio sospetto..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
                rows="3"
                disabled={reporting}
              />
              <button
                onClick={handleReport}
                disabled={reporting || !reportReason.trim()}
                className="w-full px-4 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {reporting ? 'Invio segnalazione...' : 'Invia Segnalazione'}
              </button>
            </div>
          ) : (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
              <span className="text-3xl block mb-2">✓</span>
              <p className="font-semibold text-green-800">Segnalazione inviata con successo!</p>
              <p className="text-sm text-green-700 mt-1">Grazie per aver contribuito alla sicurezza della community.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t">
          <p className="text-xs text-gray-500 text-center">
            ⚠️ Questo è un sistema automatico di rilevamento. I risultati sono indicativi e non sostituiscono il buon senso.
            Verifica sempre personalmente prima di procedere con l'acquisto.
          </p>
        </div>
      </div>
    </div>
  );
}
