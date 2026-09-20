/**
 * COMPUTING MACHINERY AND INTELLIGENCE — Alan M. Turing (1950)
 * Interactive Reader Application
 */

(function () {
    'use strict';

    // --------------------------------------------------------------------------
    // Theme Management
    // --------------------------------------------------------------------------
    const htmlElement = document.documentElement;
    const themeButtons = document.querySelectorAll('.theme-btn');
    const THEME_STORAGE_KEY = 'turing-reader-theme';

    function setTheme(theme) {
        if (!['light', 'parchment', 'dark'].includes(theme)) theme = 'light';
        htmlElement.setAttribute('data-theme', theme);
        try {
            localStorage.setItem(THEME_STORAGE_KEY, theme);
        } catch (e) {
            // LocalStorage might be restricted
        }
        themeButtons.forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-theme') === theme);
        });

        // Sync theme-color meta tag for PWA / mobile browser chrome
        const themeMeta = document.querySelector('meta[name="theme-color"]');
        if (themeMeta) {
            const colors = { light: '#fcfbf9', parchment: '#f5eedb', dark: '#121214' };
            themeMeta.setAttribute('content', colors[theme] || '#fcfbf9');
        }
    }

    function initTheme() {
        let saved = null;
        try {
            saved = localStorage.getItem(THEME_STORAGE_KEY);
        } catch (e) {}

        if (saved) {
            setTheme(saved);
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
        } else {
            setTheme('light');
        }

        themeButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                setTheme(btn.getAttribute('data-theme'));
            });
        });
    }

    // --------------------------------------------------------------------------
    // Font Scaling
    // --------------------------------------------------------------------------
    const FONT_STORAGE_KEY = 'turing-reader-font-scale';
    const fontDecBtn = document.getElementById('font-dec');
    const fontIncBtn = document.getElementById('font-inc');
    const FONT_MIN = 0.85;
    const FONT_MAX = 1.35;
    const FONT_STEP = 0.05;
    let currentFontScale = 1.05;

    function setFontScale(scale) {
        scale = Math.max(FONT_MIN, Math.min(FONT_MAX, scale));
        currentFontScale = Math.round(scale * 100) / 100;
        htmlElement.style.setProperty('--font-scale', `${currentFontScale}rem`);
        try {
            localStorage.setItem(FONT_STORAGE_KEY, currentFontScale);
        } catch (e) {}
    }

    function initFontScaling() {
        try {
            const saved = localStorage.getItem(FONT_STORAGE_KEY);
            if (saved) currentFontScale = parseFloat(saved) || 1.05;
        } catch (e) {}
        setFontScale(currentFontScale);

        if (fontDecBtn) {
            fontDecBtn.addEventListener('click', () => {
                setFontScale(currentFontScale - FONT_STEP);
            });
        }
        if (fontIncBtn) {
            fontIncBtn.addEventListener('click', () => {
                setFontScale(currentFontScale + FONT_STEP);
            });
        }
    }

    // --------------------------------------------------------------------------
    // Reading Progress Bar
    // --------------------------------------------------------------------------
    const progressBar = document.getElementById('progress-bar');

    function updateProgress() {
        if (!progressBar) return;
        const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (totalHeight <= 0) {
            progressBar.style.width = '0%';
            return;
        }
        const progress = Math.min(100, Math.max(0, (window.scrollY / totalHeight) * 100));
        progressBar.style.width = `${progress}%`;
    }

    // --------------------------------------------------------------------------
    // Table of Contents & Scrollspy
    // --------------------------------------------------------------------------
    const tocItems = document.querySelectorAll('.toc-item');
    const tocSubitems = document.querySelectorAll('.toc-subitem');
    const sec6Item = document.getElementById('toc-item-sec-6');

    function initScrollspy() {
        const sections = document.querySelectorAll('.paper-section');
        const objections = document.querySelectorAll('.objection-header');

        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    tocItems.forEach(item => {
                        const link = item.querySelector('.toc-link');
                        if (link && link.getAttribute('href') === `#${id}`) {
                            item.classList.add('active');
                        } else {
                            item.classList.remove('active');
                        }
                    });

                    // Expand or collapse Section 6 sublist
                    if (sec6Item) {
                        if (id === 'sec-6') {
                            sec6Item.classList.add('expanded');
                        } else {
                            sec6Item.classList.remove('expanded');
                        }
                    }
                }
            });
        }, {
            rootMargin: '-10% 0px -65% 0px',
            threshold: 0
        });

        sections.forEach(sec => sectionObserver.observe(sec));

        // Sub-objections observer
        const objectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    tocSubitems.forEach(sub => {
                        const sublink = sub.querySelector('.toc-sublink');
                        if (sublink && sublink.getAttribute('href') === `#${id}`) {
                            sub.classList.add('active');
                        } else {
                            sub.classList.remove('active');
                        }
                    });
                }
            });
        }, {
            rootMargin: '-15% 0px -60% 0px',
            threshold: 0
        });

        objections.forEach(obj => objectionObserver.observe(obj));
    }

    // --------------------------------------------------------------------------
    // Mobile Drawer Navigation
    // --------------------------------------------------------------------------
    const tocToggleBtn = document.getElementById('toc-toggle');
    const tocCloseBtn = document.getElementById('toc-close-btn');
    const sidebar = document.getElementById('sidebar');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');

    function toggleSidebar(open) {
        if (!sidebar) return;
        const shouldOpen = open !== undefined ? open : !sidebar.classList.contains('open');
        sidebar.classList.toggle('open', shouldOpen);
        if (sidebarBackdrop) {
            sidebarBackdrop.classList.toggle('active', shouldOpen);
        }
    }

    function initMobileNav() {
        if (tocToggleBtn) {
            tocToggleBtn.addEventListener('click', () => toggleSidebar(true));
        }
        if (tocCloseBtn) {
            tocCloseBtn.addEventListener('click', () => toggleSidebar(false));
        }
        if (sidebarBackdrop) {
            sidebarBackdrop.addEventListener('click', () => toggleSidebar(false));
        }

        // Close drawer when clicking any link in sidebar on mobile
        document.querySelectorAll('.toc-link, .toc-sublink').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 900) {
                    toggleSidebar(false);
                }
            });
        });
    }

    // --------------------------------------------------------------------------
    // Interactive Footnote Popover
    // --------------------------------------------------------------------------
    const fnPopover = document.getElementById('fn-popover');
    const popoverBody = document.getElementById('popover-body');
    const popoverClose = document.getElementById('popover-close');
    const popoverJumpBtn = document.getElementById('popover-jump-btn');
    let popoverTimeout = null;

    function showFootnotePopover(targetLink) {
        if (!fnPopover || !popoverBody) return;
        const fnId = targetLink.getAttribute('data-footnote-id');
        const fnElement = document.getElementById(fnId);
        if (!fnElement) return;

        const fnContent = fnElement.querySelector('.fn-content');
        if (!fnContent) return;

        // Clone content without return link
        const clone = fnContent.cloneNode(true);
        const backlink = clone.querySelector('.fn-backlink');
        if (backlink) backlink.remove();

        popoverBody.innerHTML = clone.innerHTML;
        if (popoverJumpBtn) {
            popoverJumpBtn.href = `#${fnId}`;
        }

        fnPopover.classList.add('visible');
        fnPopover.setAttribute('aria-hidden', 'false');

        // Position popover
        const rect = targetLink.getBoundingClientRect();
        const popoverWidth = Math.min(380, window.innerWidth * 0.9);
        let left = rect.left + window.scrollX - (popoverWidth / 2) + (rect.width / 2);
        let top = rect.bottom + window.scrollY + 8;

        // Viewport boundaries
        if (left < 10) left = 10;
        if (left + popoverWidth > window.innerWidth - 10) {
            left = window.innerWidth - popoverWidth - 10;
        }

        fnPopover.style.left = `${left}px`;
        fnPopover.style.top = `${top}px`;
    }

    function hideFootnotePopover() {
        if (!fnPopover) return;
        fnPopover.classList.remove('visible');
        fnPopover.setAttribute('aria-hidden', 'true');
    }

    function initFootnotePopovers() {
        const fnLinks = document.querySelectorAll('.fn-link');
        fnLinks.forEach(link => {
            // Hover events
            link.addEventListener('mouseenter', () => {
                clearTimeout(popoverTimeout);
                showFootnotePopover(link);
            });
            link.addEventListener('mouseleave', () => {
                popoverTimeout = setTimeout(hideFootnotePopover, 400);
            });

            // Click event (for mobile or click to toggle)
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    showFootnotePopover(link);
                }
            });
        });

        if (fnPopover) {
            fnPopover.addEventListener('mouseenter', () => {
                clearTimeout(popoverTimeout);
            });
            fnPopover.addEventListener('mouseleave', () => {
                popoverTimeout = setTimeout(hideFootnotePopover, 300);
            });
        }

        if (popoverClose) {
            popoverClose.addEventListener('click', hideFootnotePopover);
        }

        if (popoverJumpBtn) {
            popoverJumpBtn.addEventListener('click', hideFootnotePopover);
        }

        document.addEventListener('click', (e) => {
            if (fnPopover && fnPopover.classList.contains('visible') && !fnPopover.contains(e.target) && !e.target.classList.contains('fn-link')) {
                hideFootnotePopover();
            }
        });
    }

    // --------------------------------------------------------------------------
    // Citation Modal
    // --------------------------------------------------------------------------
    const citeBtn = document.getElementById('cite-btn');
    const citeModal = document.getElementById('cite-modal');
    const modalCloseBtn = document.getElementById('modal-close');
    const citeTabs = document.querySelectorAll('.cite-tab-btn');
    const copyCiteBtns = document.querySelectorAll('.copy-cite-btn');

    function openCiteModal() {
        if (!citeModal) return;
        citeModal.classList.add('active');
        citeModal.setAttribute('aria-hidden', 'false');
    }

    function closeCiteModal() {
        if (!citeModal) return;
        citeModal.classList.remove('active');
        citeModal.setAttribute('aria-hidden', 'true');
    }

    function initCiteModal() {
        if (citeBtn) citeBtn.addEventListener('click', openCiteModal);
        if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeCiteModal);

        if (citeModal) {
            const backdrop = citeModal.querySelector('.modal-backdrop');
            if (backdrop) backdrop.addEventListener('click', closeCiteModal);
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && citeModal && citeModal.classList.contains('active')) {
                closeCiteModal();
            }
        });

        // Tab switching
        citeTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                citeTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const targetId = `cite-${tab.getAttribute('data-tab')}`;
                document.querySelectorAll('.cite-panel').forEach(p => {
                    p.classList.toggle('active', p.id === targetId);
                });
            });
        });

        // Copy button
        copyCiteBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetId = btn.getAttribute('data-target');
                const codeEl = document.getElementById(targetId);
                if (codeEl) {
                    const text = codeEl.innerText.trim();
                    navigator.clipboard.writeText(text).then(() => {
                        const originalText = btn.textContent;
                        btn.textContent = 'Copied to Clipboard!';
                        btn.style.backgroundColor = 'var(--speaker-candidate)';
                        setTimeout(() => {
                            btn.textContent = originalText;
                            btn.style.backgroundColor = '';
                        }, 2000);
                    }).catch(err => {
                        console.error('Failed to copy: ', err);
                    });
                }
            });
        });
    }

    // --------------------------------------------------------------------------
    // Initialization
    // --------------------------------------------------------------------------
    function initApp() {
        initTheme();
        initFontScaling();
        initScrollspy();
        initMobileNav();
        initFootnotePopovers();
        initCiteModal();

        // Passive scroll listener for progress bar
        window.addEventListener('scroll', updateProgress, { passive: true });
        updateProgress();

        // Register Service Worker for offline PWA reading
        if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('sw.js').catch(() => {});
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initApp);
    } else {
        initApp();
    }
})();
