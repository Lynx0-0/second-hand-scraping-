import { useState } from 'react';
import ScamBadge from './ScamBadge';
import ScamModal from './ScamModal';
import { calculateScamScore } from '../utils/scamDetector';

export default function ProductCard({ listing }) {
  const [showModal, setShowModal] = useState(false);
  const [imageError, setImageError] = useState(false);

  // Calcola score truffa
  const scamData = calculateScamScore(listing);

  // Placeholder image se non ci sono foto o errore
  const imageUrl = !imageError && listing.photos && listing.photos.length > 0
    ? listing.photos[0]
    : 'https://via.placeholder.com/300x200?text=No+Image';

  // Formatta prezzo
  const priceDisplay = listing.price
    ? `€${listing.price.toFixed(2)}`
    : listing.price_text || 'Prezzo non specificato';

  // Formatta data
  const dateDisplay = listing.posted_date || 'Data non disponibile';

  return (
    <>
      <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden">
        {/* Image */}
        <div className="relative">
          <img
            src={imageUrl}
            alt={listing.title}
            onError={() => setImageError(true)}
            className="w-full h-48 object-cover"
          />

          {/* Scam Badge Overlay */}
          {scamData.riskLevel !== 'low' && (
            <div className="absolute top-2 right-2">
              <ScamBadge
                scamData={scamData}
                onClick={(e) => {
                  e.stopPropagation();
                  setShowModal(true);
                }}
              />
            </div>
          )}

          {/* Photo Count */}
          {listing.photos && listing.photos.length > 1 && (
            <div className="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs flex items-center gap-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
              </svg>
              {listing.photos.length}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Title */}
          <h3 className="font-semibold text-lg mb-2 line-clamp-2 h-14" title={listing.title}>
            {listing.title}
          </h3>

          {/* Price */}
          <div className="mb-3">
            <p className="text-2xl font-bold text-gray-900">{priceDisplay}</p>
          </div>

          {/* Location & Date */}
          <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
            {listing.location && (
              <span className="flex items-center gap-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {listing.location}
              </span>
            )}
            <span className="text-xs">{dateDisplay}</span>
          </div>

          {/* Description Preview */}
          {listing.description && (
            <p className="text-sm text-gray-600 line-clamp-2 mb-3">
              {listing.description}
            </p>
          )}

          {/* Seller Info */}
          {listing.seller_name && (
            <div className="flex items-center gap-2 mb-3 text-sm text-gray-600">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>{listing.seller_name}</span>
              {listing.seller_type && (
                <span className="px-2 py-0.5 bg-gray-200 rounded text-xs">
                  {listing.seller_type}
                </span>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-2">
            <a
              href={listing.link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 px-4 py-2 bg-blue-600 text-white text-center font-semibold rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
            >
              <span>Vedi su Subito.it</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>

            {scamData.riskLevel !== 'low' && (
              <button
                onClick={() => setShowModal(true)}
                className="px-4 py-2 border-2 border-red-500 text-red-500 font-semibold rounded-lg hover:bg-red-50 transition-colors"
                title="Vedi dettagli sicurezza"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Scam Modal */}
      {showModal && (
        <ScamModal
          listing={listing}
          scamData={scamData}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}
