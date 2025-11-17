import { useState, useEffect } from 'react';

const PROGRESS_MESSAGES = [
  { text: "🔍 Connessione a Subito.it...", duration: 800 },
  { text: "📡 Caricamento della pagina di ricerca...", duration: 1200 },
  { text: "🔎 Analisi dei risultati...", duration: 1500 },
  { text: "📋 Estrazione degli annunci...", duration: 1800 },
  { text: "🛡️ Controllo sicurezza annunci...", duration: 2000 },
  { text: "🔍 Analisi testi per rilevamento truffe...", duration: 1600 },
  { text: "💰 Verifica prezzi sospetti...", duration: 1400 },
  { text: "📊 Elaborazione dati...", duration: 1200 },
  { text: "✅ Finalizzazione risultati...", duration: 1000 },
];

export default function SearchProgress({ isSearching, onComplete }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    if (!isSearching) {
      setCurrentStep(0);
      setProgress(0);
      setElapsedTime(0);
      return;
    }

    // Timer per tempo trascorso
    const timeInterval = setInterval(() => {
      setElapsedTime((prev) => prev + 100);
    }, 100);

    // Avanza attraverso i messaggi
    let stepTimeout;
    let progressInterval;

    const advanceStep = () => {
      if (currentStep < PROGRESS_MESSAGES.length - 1) {
        const nextStep = currentStep + 1;
        setCurrentStep(nextStep);

        // Animazione progress bar per questo step
        const stepProgress = ((nextStep + 1) / PROGRESS_MESSAGES.length) * 100;
        let currentProgress = progress;

        progressInterval = setInterval(() => {
          currentProgress += 2;
          if (currentProgress >= stepProgress) {
            currentProgress = stepProgress;
            clearInterval(progressInterval);
          }
          setProgress(currentProgress);
        }, 30);

        // Passa al prossimo step dopo la durata specificata
        stepTimeout = setTimeout(advanceStep, PROGRESS_MESSAGES[nextStep].duration);
      } else {
        // Completato
        setProgress(100);
        clearInterval(progressInterval);
      }
    };

    // Inizia con il primo step
    advanceStep();

    return () => {
      clearTimeout(stepTimeout);
      clearInterval(progressInterval);
      clearInterval(timeInterval);
    };
  }, [isSearching, currentStep, progress]);

  if (!isSearching) return null;

  const currentMessage = PROGRESS_MESSAGES[currentStep] || PROGRESS_MESSAGES[0];

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6 mb-6 shadow-lg animate-fade-in">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center animate-pulse">
                <svg
                  className="w-6 h-6 text-white animate-spin"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-ping" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900">
                Ricerca in corso...
              </h3>
              <p className="text-sm text-gray-600">
                Tempo trascorso: {(elapsedTime / 1000).toFixed(1)}s
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-blue-600">
              {Math.round(progress)}%
            </div>
            <div className="text-xs text-gray-500">
              Step {currentStep + 1}/{PROGRESS_MESSAGES.length}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="relative">
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-all duration-300 ease-out relative"
              style={{ width: `${progress}%` }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30 animate-shimmer" />
            </div>
          </div>
        </div>

        {/* Current Message */}
        <div className="bg-white rounded-lg p-4 shadow-sm border border-blue-100">
          <div className="flex items-center gap-3">
            <div className="text-2xl animate-bounce">
              {currentMessage.text.split(' ')[0]}
            </div>
            <div className="flex-1">
              <p className="text-base font-medium text-gray-800 animate-fade-in">
                {currentMessage.text.substring(currentMessage.text.indexOf(' ') + 1)}
              </p>
            </div>
          </div>
        </div>

        {/* Previous Steps Timeline */}
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 max-h-48 overflow-y-auto">
          <h4 className="text-xs font-semibold text-gray-500 uppercase mb-3">
            Operazioni completate
          </h4>
          <div className="space-y-2">
            {PROGRESS_MESSAGES.slice(0, currentStep).map((msg, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 text-sm text-gray-600 animate-slide-in"
              >
                <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                  <svg
                    className="w-3 h-3 text-green-600"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <span className="line-through opacity-60">{msg.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Info */}
        <div className="flex items-start gap-2 text-xs text-gray-600 bg-blue-50 rounded-lg p-3">
          <svg
            className="w-4 h-4 text-blue-500 flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
              clipRule="evenodd"
            />
          </svg>
          <p>
            Stiamo analizzando gli annunci in tempo reale per rilevare possibili truffe.
            Questo può richiedere alcuni secondi. Grazie per la pazienza!
          </p>
        </div>
      </div>

      {/* Custom CSS for animations */}
      <style jsx>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateX(-10px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        .animate-shimmer {
          animation: shimmer 2s infinite;
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-in;
        }
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
      `}</style>
    </div>
  );
}
