import React, { useState, useEffect } from 'react';
import type { CarouselSlide } from '../data/mockData';

interface ImageCarouselProps {
  slides: CarouselSlide[];
  onExploreClick?: () => void;
}

export const ImageCarousel: React.FC<ImageCarouselProps> = ({ slides, onExploreClick }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Auto-avance cada 5 segundos
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [slides.length]);

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev === 0 ? slides.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % slides.length);
  };

  return (
    <div className="hero-carousel" role="region" aria-label="Carrusel Institucional UPT">
      {slides.map((slide, index) => (
        <div
          key={slide.id}
          className={`carousel-slide ${index === currentIndex ? 'active' : ''}`}
        >
          <img
            src={slide.image}
            alt={slide.title}
            className="carousel-bg-image"
          />
          <div className="carousel-overlay">
            <span
              className="badge badge-gold"
              style={{
                width: 'fit-content',
                background: 'rgba(185, 148, 81, 0.3)',
                color: '#FFDF9E',
                marginBottom: '0.75rem',
                border: '1px solid rgba(217, 191, 125, 0.4)'
              }}
            >
              {slide.tag}
            </span>
            <h2 style={{ color: '#FFFFFF', fontSize: '2rem', fontWeight: 800, marginBottom: '0.6rem', maxWidth: '700px', lineHeight: 1.2 }}>
              {slide.title}
            </h2>
            <p style={{ color: 'rgba(255, 255, 255, 0.9)', fontSize: '1rem', maxWidth: '600px', marginBottom: '1.5rem' }}>
              {slide.subtitle}
            </p>
            {onExploreClick && (
              <div>
                <button className="btn-gold btn-sm" onClick={onExploreClick}>
                  Ver Mentorías Disponibles ↓
                </button>
              </div>
            )}
          </div>
        </div>
      ))}

      {/* Flechas Flotantes (docs/diseño.md - 4.4) */}
      <button
        className="carousel-arrow prev"
        onClick={handlePrev}
        aria-label="Imagen anterior"
      >
        ‹
      </button>
      <button
        className="carousel-arrow next"
        onClick={handleNext}
        aria-label="Siguiente imagen"
      >
        ›
      </button>

      {/* Puntos / Píldoras de Navegación */}
      <div className="carousel-dots">
        {slides.map((_, dotIdx) => (
          <button
            key={dotIdx}
            className={`carousel-dot ${dotIdx === currentIndex ? 'active' : ''}`}
            onClick={() => setCurrentIndex(dotIdx)}
            aria-label={`Ir a la diapositiva ${dotIdx + 1}`}
          />
        ))}
      </div>
    </div>
  );
};
