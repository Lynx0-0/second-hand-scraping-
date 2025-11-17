import { getRiskDisplay } from '../utils/scamDetector';

export default function ScamBadge({ scamData, onClick }) {
  const { score, riskLevel } = scamData;
  const display = getRiskDisplay(riskLevel);

  // Mostra badge solo per rischio medio/alto
  if (riskLevel === 'low') {
    return null;
  }

  return (
    <button
      onClick={onClick}
      className={`
        inline-flex items-center gap-2 px-3 py-1.5 rounded-md font-semibold text-sm
        ${display.bgColor} ${display.textColor} ${display.borderColor}
        border-2 hover:opacity-80 transition-opacity cursor-pointer
        animate-pulse
      `}
      title={`Score: ${score}/100 - Clicca per dettagli`}
    >
      <span className="text-lg">{display.icon}</span>
      <span>{display.label}</span>
      <span className="font-mono text-xs">({score}/100)</span>
    </button>
  );
}
