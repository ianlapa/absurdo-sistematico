/* -------------------------------------------------------------
   APP LOGIC - ABSVRDO / SISTEMÁTICO
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    initNavbarScroll();
    initMobileMenu();
    initScrollReveal();
    initSmoothScrollFix();
    initSubstackRSS();
    initLanguageToggle();
});

/**
 * Adds active glassmorphic styling to navbar upon scroll.
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar-container');
    if (!navbar) return;

    const handleScroll = () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    // Initial check
    handleScroll();
    
    window.addEventListener('scroll', handleScroll, { passive: true });
}

/**
 * Controls the mobile slide-down drawer menu.
 */
function initMobileMenu() {
    const toggleBtn = document.getElementById('menu-toggle-btn');
    const mobileNav = document.getElementById('mobile-navigation');
    
    if (!toggleBtn || !mobileNav) return;
    
    const icon = toggleBtn.querySelector('i');

    const toggleMenu = () => {
        const isOpen = mobileNav.classList.contains('open');
        if (isOpen) {
            mobileNav.classList.remove('open');
            icon.className = 'fas fa-bars';
            document.body.style.overflow = ''; // enable scroll
        } else {
            mobileNav.classList.add('open');
            icon.className = 'fas fa-xmark';
            document.body.style.overflow = 'hidden'; // disable scroll
        }
    };

    toggleBtn.addEventListener('click', toggleMenu);

    // Close menu when a link is clicked
    const mobileLinks = mobileNav.querySelectorAll('.mobile-nav-item');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileNav.classList.remove('open');
            icon.className = 'fas fa-bars';
            document.body.style.overflow = '';
        });
    });
}

/**
 * Dynamic fade-in scroll animation using Intersection Observer.
 */
function initScrollReveal() {
    // Inject the reveal css classes into the document dynamically to ensure it degrades gracefully if JS is disabled
    const style = document.createElement('style');
    style.innerHTML = `
        .reveal-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            will-change: opacity, transform;
        }
        .reveal-on-scroll.revealed {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);

    const elementsToReveal = [
        document.querySelector('.essays-info'),
        document.querySelector('.newsletter-card'),
        document.querySelector('.host-avatar-frame'),
        document.querySelector('.host-details')
    ].filter(el => el !== null);

    elementsToReveal.forEach(el => {
        el.classList.add('reveal-on-scroll');
    });

    const observerOptions = {
        root: null,
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries, self) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                self.unobserve(entry.target); // Stop observing once animated
            }
        });
    }, observerOptions);

    elementsToReveal.forEach(el => {
        observer.observe(el);
    });
}

/**
 * Elegant smooth scroll offset alignment for nav links.
 */
function initSmoothScrollFix() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetEl = document.querySelector(targetId);
            if (!targetEl) return;
            
            e.preventDefault();
            
            const headerOffset = 90;
            const elementPosition = targetEl.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.scrollY - headerOffset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        });
    });
}

/**
 * Dynamically fetches and renders the 3 latest Substack posts via RSS.
 * If the request fails, it preserves the static fallback posts defined in index.html.
 */
async function initSubstackRSS() {
    const container = document.getElementById('substack-feed-container');
    if (!container) return;

    const substackUrl = 'https://ianlapa.substack.com/feed';
    const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(substackUrl)}`;

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error('RSS fetch failed');
        
        const data = await response.json();
        if (data.status !== 'ok' || !data.items || data.items.length === 0) {
            throw new Error('Invalid RSS response format');
        }

        const latestItems = data.items.slice(0, 3);
        const monthsPt = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
        const monthsEn = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const currentLang = document.documentElement.lang === 'en' ? 'en' : 'pt';
        const months = currentLang === 'en' ? monthsEn : monthsPt;

        const formatRSSDate = (dateStr) => {
            // dateStr format is usually "YYYY-MM-DD HH:MM:SS" or ISO. We replace '-' with '/' for compatibility with iOS/Safari Date parsing.
            const parsedDate = new Date(dateStr.replace(/-/g, '/'));
            if (isNaN(parsedDate.getTime())) return '';
            
            const day = String(parsedDate.getDate()).padStart(2, '0');
            const month = months[parsedDate.getMonth()];
            return `${day} ${month}`;
        };

        const listHtml = latestItems.map(item => {
            const formattedDate = formatRSSDate(item.pubDate);
            return `
                <a href="${item.link}" target="_blank" rel="noopener" class="essay-item">
                    <span class="essay-date">${formattedDate}</span>
                    <span class="essay-title">${item.title} <i class="fas fa-external-link-alt"></i></span>
                </a>
            `;
        }).join('');

        container.innerHTML = listHtml;
    } catch (error) {
        console.warn('Substack RSS Feed could not load dynamically. Falling back to static content. Error:', error);
        // Do nothing else - the original static HTML links remain intact as a fallback.
    }
}

/**
 * Language toggle: switches all [data-pt] / [data-en] elements between Portuguese and English.
 */
function initLanguageToggle() {
    const toggleBtn = document.getElementById('lang-toggle');
    if (!toggleBtn) return;

    let currentLang = 'pt';

    const applyLanguage = (lang) => {
        const attr = `data-${lang}`;
        const elements = document.querySelectorAll(`[${attr}]`);
        elements.forEach(el => {
            el.textContent = el.getAttribute(attr);
        });

        // Handle placeholders
        const placeholderAttr = `data-${lang}-placeholder`;
        const placeholderEls = document.querySelectorAll(`[${placeholderAttr}]`);
        placeholderEls.forEach(el => {
            el.placeholder = el.getAttribute(placeholderAttr);
        });

        // Update html lang attribute
        document.documentElement.lang = lang === 'pt' ? 'pt-BR' : 'en';

        // Update toggle button label
        const label = toggleBtn.querySelector('.lang-label');
        if (label) label.textContent = lang === 'pt' ? 'EN' : 'PT';
    };

    toggleBtn.addEventListener('click', () => {
        currentLang = currentLang === 'pt' ? 'en' : 'pt';
        applyLanguage(currentLang);
    });
}
