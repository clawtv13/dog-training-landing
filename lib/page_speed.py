#!/usr/bin/env python3
"""
Page Speed Optimization Utilities
HTML minification, lazy loading, CSS/JS optimization
"""

import re
from typing import Optional


def minify_html(html: str) -> str:
    """
    Minify HTML by removing unnecessary whitespace
    
    Args:
        html: HTML content to minify
    
    Returns:
        Minified HTML
    """
    # Collapse multiple spaces/newlines to single space
    html = re.sub(r'\s+', ' ', html)
    
    # Remove spaces between tags
    html = re.sub(r'>\s+<', '><', html)
    
    # Remove spaces around attributes
    html = re.sub(r'\s+([=])\s+', r'\1', html)
    
    return html.strip()


def add_lazy_loading(html: str) -> str:
    """
    Add lazy loading to all images
    
    Args:
        html: HTML content
    
    Returns:
        HTML with lazy loading added to images
    """
    # Add loading="lazy" to img tags that don't already have it
    html = re.sub(
        r'<img\s+(?![^>]*loading=)',
        r'<img loading="lazy" ',
        html,
        flags=re.IGNORECASE
    )
    
    return html


def inline_critical_css(html: str, critical_css: str) -> str:
    """
    Inline critical CSS in <head>
    
    Args:
        html: HTML content
        critical_css: Critical CSS to inline
    
    Returns:
        HTML with inlined critical CSS
    """
    style_tag = f"<style>{critical_css}</style>"
    
    # Insert before closing </head>
    html = html.replace('</head>', f'{style_tag}\n</head>')
    
    return html


def defer_non_critical_js(html: str) -> str:
    """
    Add defer attribute to non-critical JavaScript
    
    Args:
        html: HTML content
    
    Returns:
        HTML with deferred JavaScript
    """
    # Skip inline scripts and already deferred/async scripts
    html = re.sub(
        r'<script\s+(?![^>]*(defer|async|type="module"))[^>]*src=',
        r'<script defer src=',
        html,
        flags=re.IGNORECASE
    )
    
    return html


def optimize_html(html: str, minify: bool = True, lazy_images: bool = True, 
                  defer_js: bool = True) -> str:
    """
    Apply all page speed optimizations
    
    Args:
        html: HTML content to optimize
        minify: Enable HTML minification
        lazy_images: Enable lazy loading for images
        defer_js: Enable JS deferring
    
    Returns:
        Optimized HTML
    """
    if lazy_images:
        html = add_lazy_loading(html)
    
    if defer_js:
        html = defer_non_critical_js(html)
    
    if minify:
        html = minify_html(html)
    
    return html


# Critical CSS template for above-the-fold content
CRITICAL_CSS_TEMPLATE = """
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.6;
}

nav, header {
    background: #333;
    color: white;
    padding: 1rem;
}

main {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

h1, h2, h3 {
    line-height: 1.2;
    margin-top: 1.5em;
}

a {
    color: #0066cc;
    text-decoration: none;
}

img {
    max-width: 100%;
    height: auto;
}
"""


def get_critical_css() -> str:
    """Get minimal critical CSS for above-the-fold content"""
    return CRITICAL_CSS_TEMPLATE.strip()
