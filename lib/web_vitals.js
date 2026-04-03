/**
 * Core Web Vitals Tracking
 * Lightweight performance monitoring
 */

(function() {
    'use strict';
    
    // Check if PerformanceObserver is supported
    if (!('PerformanceObserver' in window)) {
        console.warn('PerformanceObserver not supported');
        return;
    }
    
    const vitals = {
        lcp: null,  // Largest Contentful Paint
        fid: null,  // First Input Delay
        cls: null   // Cumulative Layout Shift
    };
    
    // Largest Contentful Paint (LCP)
    function observeLCP() {
        try {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                vitals.lcp = lastEntry.renderTime || lastEntry.loadTime;
                logMetric('LCP', vitals.lcp);
            });
            observer.observe({ type: 'largest-contentful-paint', buffered: true });
        } catch (e) {
            console.warn('LCP observation failed:', e);
        }
    }
    
    // First Input Delay (FID)
    function observeFID() {
        try {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach((entry) => {
                    vitals.fid = entry.processingStart - entry.startTime;
                    logMetric('FID', vitals.fid);
                });
            });
            observer.observe({ type: 'first-input', buffered: true });
        } catch (e) {
            console.warn('FID observation failed:', e);
        }
    }
    
    // Cumulative Layout Shift (CLS)
    function observeCLS() {
        try {
            let clsValue = 0;
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                        vitals.cls = clsValue;
                    }
                }
                logMetric('CLS', vitals.cls);
            });
            observer.observe({ type: 'layout-shift', buffered: true });
        } catch (e) {
            console.warn('CLS observation failed:', e);
        }
    }
    
    // Log metric to console (can be extended to send to analytics)
    function logMetric(name, value) {
        const rating = getMetricRating(name, value);
        console.log(`[Web Vitals] ${name}: ${value.toFixed(2)}ms - ${rating}`);
        
        // Optional: Send to analytics endpoint
        // sendToAnalytics(name, value, rating);
    }
    
    // Rate metric performance
    function getMetricRating(name, value) {
        const thresholds = {
            'LCP': { good: 2500, needsImprovement: 4000 },
            'FID': { good: 100, needsImprovement: 300 },
            'CLS': { good: 0.1, needsImprovement: 0.25 }
        };
        
        const threshold = thresholds[name];
        if (!threshold) return 'unknown';
        
        if (value <= threshold.good) return 'good';
        if (value <= threshold.needsImprovement) return 'needs improvement';
        return 'poor';
    }
    
    // Basic page load performance
    function trackPageLoad() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    const loadTime = perfData.loadEventEnd - perfData.fetchStart;
                    console.log(`[Web Vitals] Page Load Time: ${loadTime.toFixed(2)}ms`);
                    
                    // Log detailed timing
                    const timing = {
                        'DNS Lookup': perfData.domainLookupEnd - perfData.domainLookupStart,
                        'TCP Connection': perfData.connectEnd - perfData.connectStart,
                        'Server Response': perfData.responseStart - perfData.requestStart,
                        'DOM Processing': perfData.domComplete - perfData.domLoading,
                        'Total Load': loadTime
                    };
                    
                    console.table(timing);
                }
            }, 0);
        });
    }
    
    // Initialize all observers
    observeLCP();
    observeFID();
    observeCLS();
    trackPageLoad();
    
    // Expose vitals globally (optional)
    window.webVitals = vitals;
    
})();
