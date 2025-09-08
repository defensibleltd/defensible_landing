// IP Fabric Decision Tree Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    const optionBubbles = document.querySelectorAll('.option-bubble');
    const connectionLines = document.querySelectorAll('.connection-line');
    const rootNode = document.querySelector('.root-node');
    
    // Initialize the decision tree
    init();
    
    function init() {
        setupOptionInteractions();
        setupKeyboardNavigation();
        setupAnimations();
    }
    
    function setupOptionInteractions() {
        optionBubbles.forEach((bubble, index) => {
            // Mouse enter - highlight connection
            bubble.addEventListener('mouseenter', function() {
                highlightConnection(bubble.dataset.option);
                addRippleEffect(bubble);
            });
            
            // Mouse leave - remove highlights
            bubble.addEventListener('mouseleave', function() {
                removeConnectionHighlights();
            });
            
            // Click handler - simulate selection
            bubble.addEventListener('click', function() {
                selectOption(bubble);
            });
            
            // Add focus support for accessibility
            bubble.setAttribute('tabindex', '0');
            bubble.setAttribute('role', 'button');
            bubble.setAttribute('aria-label', `Select ${bubble.querySelector('.option-title').textContent}`);
            
            // Keyboard support
            bubble.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    selectOption(bubble);
                }
            });
        });
    }
    
    function highlightConnection(option) {
        // Reset all connections
        removeConnectionHighlights();
        
        // Highlight the specific connection
        const lineClass = `line-${option}`;
        const targetLine = document.querySelector(`.${lineClass}`);
        
        if (targetLine) {
            targetLine.style.opacity = '1';
            targetLine.style.strokeWidth = '3';
            targetLine.style.filter = 'drop-shadow(0 0 4px currentColor)';
        }
        
        // Add subtle glow to root node
        rootNode.style.transform = 'scale(1.02)';
        rootNode.style.filter = 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))';
    }
    
    function removeConnectionHighlights() {
        connectionLines.forEach(line => {
            line.style.opacity = '0.7';
            line.style.strokeWidth = '2';
            line.style.filter = 'none';
        });
        
        // Reset root node
        rootNode.style.transform = 'scale(1)';
        rootNode.style.filter = 'none';
    }
    
    function addRippleEffect(element) {
        // Create ripple element
        const ripple = document.createElement('div');
        ripple.className = 'ripple-effect';
        
        // Style the ripple
        Object.assign(ripple.style, {
            position: 'absolute',
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.3)',
            transform: 'scale(0)',
            animation: 'ripple 0.6s linear',
            pointerEvents: 'none',
            left: '50%',
            top: '50%',
            width: '20px',
            height: '20px',
            marginLeft: '-10px',
            marginTop: '-10px'
        });
        
        // Add ripple keyframe if not exists
        if (!document.querySelector('#ripple-keyframes')) {
            const style = document.createElement('style');
            style.id = 'ripple-keyframes';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Add to element and clean up
        element.style.position = 'relative';
        element.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    function selectOption(bubble) {
        // Remove previous selections
        optionBubbles.forEach(b => {
            b.classList.remove('selected');
            b.style.transform = '';
        });
        
        // Mark as selected
        bubble.classList.add('selected');
        
        // Add selection styles
        const selection = document.createElement('style');
        if (!document.querySelector('#selection-styles')) {
            selection.id = 'selection-styles';
            selection.textContent = `
                .option-bubble.selected {
                    transform: translateY(-8px) scale(1.02);
                    border-width: 3px;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                }
                .option-bubble.selected::after {
                    content: '✓ Selected';
                    position: absolute;
                    top: -12px;
                    right: -12px;
                    background: var(--color-success);
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                    animation: selectBounce 0.5s ease-out;
                }
                @keyframes selectBounce {
                    0% { transform: scale(0) rotate(-180deg); opacity: 0; }
                    50% { transform: scale(1.2) rotate(-10deg); opacity: 1; }
                    100% { transform: scale(1) rotate(0deg); opacity: 1; }
                }
            `;
            document.head.appendChild(selection);
        }
        
        // Highlight the connection permanently
        highlightConnection(bubble.dataset.option);
        
        // Add subtle shake to other options
        optionBubbles.forEach(otherBubble => {
            if (otherBubble !== bubble) {
                otherBubble.style.animation = 'subtle-shake 0.5s ease-in-out';
                setTimeout(() => {
                    otherBubble.style.animation = '';
                }, 500);
            }
        });
        
        // Add shake animation if not exists
        if (!document.querySelector('#shake-keyframes')) {
            const shakeStyle = document.createElement('style');
            shakeStyle.id = 'shake-keyframes';
            shakeStyle.textContent = `
                @keyframes subtle-shake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
                    20%, 40%, 60%, 80% { transform: translateX(2px); }
                }
            `;
            document.head.appendChild(shakeStyle);
        }
        
        // Announce selection for screen readers
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = `Selected: ${bubble.querySelector('.option-title').textContent}`;
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            if (announcement.parentNode) {
                announcement.parentNode.removeChild(announcement);
            }
        }, 1000);
    }
    
    function setupKeyboardNavigation() {
        // Add keyboard navigation between options
        document.addEventListener('keydown', function(e) {
            const focusedElement = document.activeElement;
            const currentIndex = Array.from(optionBubbles).indexOf(focusedElement);
            
            if (currentIndex === -1) return;
            
            let newIndex;
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    newIndex = currentIndex > 0 ? currentIndex - 1 : optionBubbles.length - 1;
                    optionBubbles[newIndex].focus();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    newIndex = currentIndex < optionBubbles.length - 1 ? currentIndex + 1 : 0;
                    optionBubbles[newIndex].focus();
                    break;
                case 'Home':
                    e.preventDefault();
                    optionBubbles[0].focus();
                    break;
                case 'End':
                    e.preventDefault();
                    optionBubbles[optionBubbles.length - 1].focus();
                    break;
            }
        });
    }
    
    function setupAnimations() {
        // Intersection Observer for scroll-triggered animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, observerOptions);
        
        // Observe all animated elements
        const animatedElements = document.querySelectorAll('.root-node, .option-bubble');
        animatedElements.forEach(el => {
            observer.observe(el);
        });
        
        // Add subtle parallax effect on scroll (for desktop)
        if (window.innerWidth > 768) {
            let ticking = false;
            
            function updateParallax() {
                const scrolled = window.pageYOffset;
                const parallaxElements = document.querySelectorAll('.option-bubble');
                
                parallaxElements.forEach((el, index) => {
                    const speed = 0.02 * (index + 1);
                    const yPos = -(scrolled * speed);
                    el.style.transform = `translateY(${yPos}px)`;
                });
                
                ticking = false;
            }
            
            function requestTick() {
                if (!ticking) {
                    requestAnimationFrame(updateParallax);
                    ticking = true;
                }
            }
            
            window.addEventListener('scroll', requestTick);
        }
    }
    
    // Add smooth scrolling for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Performance optimization: Debounce resize events
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            // Recalculate any size-dependent features
            removeConnectionHighlights();
        }, 250);
    });
});