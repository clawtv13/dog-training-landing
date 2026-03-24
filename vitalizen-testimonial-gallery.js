/* ============================================
   VITALIZEN — TESTIMONIAL GALLERY JS
   Lightbox functionality for review images
   ============================================ */

(function() {
  'use strict';
  
  // Create lightbox overlay on page load
  function createLightbox() {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
      <button class="lightbox-close" aria-label="Close lightbox">×</button>
      <button class="lightbox-nav lightbox-prev" aria-label="Previous image">‹</button>
      <div class="lightbox-content">
        <img class="lightbox-image" src="" alt="">
        <div class="lightbox-caption"></div>
      </div>
      <button class="lightbox-nav lightbox-next" aria-label="Next image">›</button>
    `;
    document.body.appendChild(lightbox);
    return lightbox;
  }
  
  // Initialize on DOM ready
  function init() {
    const lightbox = createLightbox();
    const lightboxImg = lightbox.querySelector('.lightbox-image');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');
    
    let currentImages = [];
    let currentIndex = 0;
    
    // Find all clickable review images
    const reviewImages = document.querySelectorAll('.review-image-wrapper, .before-after-wrapper, .instagram-item');
    
    // Convert NodeList to Array and store image data
    reviewImages.forEach((wrapper, index) => {
      const img = wrapper.querySelector('img');
      if (!img) return;
      
      const imageData = {
        src: img.src,
        alt: img.alt || '',
        caption: wrapper.dataset.caption || img.alt || ''
      };
      
      currentImages.push(imageData);
      
      // Add click event
      wrapper.addEventListener('click', function(e) {
        e.preventDefault();
        openLightbox(index);
      });
      
      // Add keyboard support
      wrapper.setAttribute('tabindex', '0');
      wrapper.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLightbox(index);
        }
      });
    });
    
    // Open lightbox
    function openLightbox(index) {
      currentIndex = index;
      updateLightboxImage();
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
      
      // Focus close button for accessibility
      setTimeout(() => closeBtn.focus(), 100);
    }
    
    // Close lightbox
    function closeLightbox() {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }
    
    // Update image in lightbox
    function updateLightboxImage() {
      if (currentImages.length === 0) return;
      
      const imageData = currentImages[currentIndex];
      lightboxImg.src = imageData.src;
      lightboxImg.alt = imageData.alt;
      lightboxCaption.textContent = imageData.caption;
      
      // Show/hide navigation arrows
      prevBtn.style.display = currentImages.length > 1 ? 'flex' : 'none';
      nextBtn.style.display = currentImages.length > 1 ? 'flex' : 'none';
    }
    
    // Navigate to previous image
    function prevImage() {
      currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
      updateLightboxImage();
    }
    
    // Navigate to next image
    function nextImage() {
      currentIndex = (currentIndex + 1) % currentImages.length;
      updateLightboxImage();
    }
    
    // Event listeners
    closeBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      closeLightbox();
    });
    
    lightbox.addEventListener('click', function(e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });
    
    prevBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      prevImage();
    });
    
    nextBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      nextImage();
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
      if (!lightbox.classList.contains('active')) return;
      
      if (e.key === 'Escape') {
        closeLightbox();
      } else if (e.key === 'ArrowLeft') {
        prevImage();
      } else if (e.key === 'ArrowRight') {
        nextImage();
      }
    });
    
    // Touch swipe support (mobile)
    let touchStartX = 0;
    let touchEndX = 0;
    
    lightbox.addEventListener('touchstart', function(e) {
      touchStartX = e.changedTouches[0].screenX;
    });
    
    lightbox.addEventListener('touchend', function(e) {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    });
    
    function handleSwipe() {
      const swipeThreshold = 50;
      const diff = touchStartX - touchEndX;
      
      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          // Swipe left (next)
          nextImage();
        } else {
          // Swipe right (prev)
          prevImage();
        }
      }
    }
  }
  
  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
