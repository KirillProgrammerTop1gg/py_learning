/**
 * contact-map.js
 * Handles additional interactive features or logging for the Google Maps iframe container
 */
document.addEventListener('DOMContentLoaded', () => {
    const mapContainer = document.querySelector('.map-container-premium');
    
    if (mapContainer) {
        console.log('⚡ Contact Map initialized using static files successfully.');
        
        // Example interactive interaction: click on map container reveals full location details
        mapContainer.addEventListener('mouseenter', () => {
            const badge = document.querySelector('.map-overlay-badge');
            if (badge) {
                badge.style.borderColor = 'var(--border-hover)';
                badge.style.boxShadow = '0 0 15px var(--accent-glow)';
            }
        });
        
        mapContainer.addEventListener('mouseleave', () => {
            const badge = document.querySelector('.map-overlay-badge');
            if (badge) {
                badge.style.borderColor = 'var(--border-color)';
                badge.style.boxShadow = '0 5px 15px rgba(0,0,0,0.5)';
            }
        });
    }
});
