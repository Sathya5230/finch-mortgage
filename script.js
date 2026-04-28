document.addEventListener('DOMContentLoaded', () => {

  // --- Active Nav State ---
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/index.html';
  document.querySelectorAll('nav a.nav-link, nav .dropdown-item').forEach(link => {
    try {
      const linkPath = new URL(link.href, window.location.href).pathname.replace(/\/$/, '');
      if (linkPath === currentPath || (currentPath.endsWith('/index.html') && linkPath.endsWith('/index.html'))) {
        link.classList.add('active');
        const parentItem = link.closest('.nav-item');
        if (parentItem) parentItem.classList.add('active');
      }
    } catch(e) {}
  });

  // --- Header Scroll Logic ---
  const header = document.querySelector('header');
  const handleScroll = () => {
    if (window.scrollY > 10) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', handleScroll);
  handleScroll(); // Initial check

  // --- Fullscreen Menu Toggle ---
  const menuBtn = document.getElementById('mobile-menu-btn');
  const closeMenuBtn = document.getElementById('close-menu-btn');
  const fullscreenMenu = document.getElementById('fullscreen-menu');

  if (menuBtn && closeMenuBtn && fullscreenMenu) {
    const openMenu = () => {
      fullscreenMenu.style.display = 'block';
      setTimeout(() => {
        fullscreenMenu.style.opacity = '1';
      }, 10);
      document.body.style.overflow = 'hidden'; 
    };

    const closeMenu = () => {
      fullscreenMenu.style.opacity = '0';
      setTimeout(() => {
        fullscreenMenu.style.display = 'none';
      }, 400); 
      document.body.style.overflow = ''; 
    };

    menuBtn.addEventListener('click', openMenu);
    closeMenuBtn.addEventListener('click', closeMenu);
  }

  // --- Scroll Reveal Animation ---
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  }, { threshold: 0.1 });

  revealElements.forEach(el => revealObserver.observe(el));

  // --- Mortgage Calculator Logic (for calculator.html) ---
  const priceInput = document.getElementById('price-range');
  const priceValue = document.getElementById('price-value');
  const downInput = document.getElementById('down-range');
  const downValue = document.getElementById('down-value');
  const rateInput = document.getElementById('rate-range');
  const rateValue = document.getElementById('rate-value');
  const termInput = document.getElementById('term-select');
  const taxInput = document.getElementById('tax-input');
  
  const totalMonthlyDisplay = document.getElementById('total-monthly');
  const piDisplay = document.getElementById('pi-payment');
  const taxDisplay = document.getElementById('tax-ins-payment');

  const formatCurrency = (val) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD', 
      maximumFractionDigits: 0 
    }).format(val);
  };

  const updateCalculator = () => {
    if (!priceInput) return;

    const price = parseFloat(priceInput.value);
    const downPercent = parseFloat(downInput.value);
    const rate = parseFloat(rateInput.value);
    const term = parseInt(termInput.value);
    const annualTax = parseFloat(taxInput.value) || 0;
    const annualIns = 1200;

    const downDollar = price * (downPercent / 100);
    const loanAmount = price - downDollar;
    
    const r = (rate / 100) / 12;
    const n = term * 12;
    
    let monthlyPI = 0;
    if (r === 0) {
      monthlyPI = loanAmount / n;
    } else {
      monthlyPI = loanAmount * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    }
      
    const monthlyTax = annualTax / 12;
    const monthlyIns = annualIns / 12;
    const totalMonthly = monthlyPI + monthlyTax + monthlyIns;

    // Update UI
    if (priceValue) priceValue.innerText = formatCurrency(price);
    if (downValue) downValue.innerText = `${downPercent}% (${formatCurrency(downDollar)})`;
    if (rateValue) rateValue.innerText = `${rate.toFixed(2)}%`;
    
    if (totalMonthlyDisplay) totalMonthlyDisplay.innerText = formatCurrency(totalMonthly);
    if (piDisplay) piDisplay.innerText = formatCurrency(monthlyPI);
    if (taxDisplay) taxDisplay.innerText = formatCurrency(monthlyTax + monthlyIns);
  };

  if (priceInput) {
    [priceInput, downInput, rateInput, termInput, taxInput].forEach(el => {
      el.addEventListener('input', updateCalculator);
    });
    updateCalculator();
  }

  // --- Multi-Step Form Logic (for apply.html) ---
  const applyForm = document.getElementById('apply-form');
  if (applyForm) {
    let currentStep = 1;
    const totalSteps = 4;
    const steps = applyForm.querySelectorAll('.form-step');
    const progressBar = document.getElementById('apply-progress');
    const stepText = document.getElementById('step-text');
    const percentText = document.getElementById('percent-text');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');

    const updateStep = (n) => {
      steps.forEach((s, idx) => {
        s.style.display = (idx + 1 === n) ? 'block' : 'none';
      });

      // Update progress
      const percent = Math.round((n / totalSteps) * 100);
      if (progressBar) progressBar.style.width = `${percent}%`;
      if (stepText) stepText.innerText = `Step ${n} of ${totalSteps}`;
      if (percentText) percentText.innerText = `${percent}%`;

      // Update buttons
      if (prevBtn) prevBtn.style.display = (n > 1) ? 'flex' : 'none';
      if (nextBtn) nextBtn.style.display = (n < totalSteps) ? 'flex' : 'none';
      if (submitBtn) submitBtn.style.display = (n === totalSteps) ? 'flex' : 'none';
    };

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (currentStep < totalSteps) {
          currentStep++;
          updateStep(currentStep);
        }
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (currentStep > 1) {
          currentStep--;
          updateStep(currentStep);
        }
      });
    }

    applyForm.addEventListener('submit', (e) => {
      e.preventDefault();
      document.getElementById('form-container').style.display = 'none';
      document.getElementById('success-message').style.display = 'block';
    });

    updateStep(currentStep);
  }

  // --- FAQ Accordion Logic ---
  const faqTriggers = document.querySelectorAll('.faq-trigger');
  faqTriggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const parent = trigger.parentElement;
      const content = parent.querySelector('.faq-content');
      const icon = trigger.querySelector('svg');
      const isOpen = parent.classList.contains('active');

      // Close all
      document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
        const c = item.querySelector('.faq-content');
        const i = item.querySelector('.faq-trigger svg');
        if (c) c.style.display = 'none';
        if (i) i.style.transform = 'rotate(0deg)';
      });

      if (!isOpen) {
        parent.classList.add('active');
        if (content) content.style.display = 'block';
        if (icon) icon.style.transform = 'rotate(180deg)';
      }
    });
  });

  // --- Mobile Dropdown Toggle ---
  // If the user taps a dropdown trigger on mobile, we'll toggle the menu
  const mobileDropdownTriggers = document.querySelectorAll('.mobile-dropdown-trigger');
  mobileDropdownTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      if (window.innerWidth < 768) {
        e.preventDefault();
        const menu = trigger.nextElementSibling;
        const isOpen = menu.style.display === 'flex';
        menu.style.display = isOpen ? 'none' : 'flex';
        // Toggle chevron rotation if needed
        const icon = trigger.querySelector('.chevron-icon');
        if (icon) icon.style.transform = isOpen ? 'rotate(0)' : 'rotate(180deg)';
      }
    });
  });

  // --- Hero Carousel: 4 slides + dots + arrows ---
  const heroSlides = document.querySelectorAll('.hero-carousel-slide');
  const carouselDots = document.querySelectorAll('.carousel-dot');

  function updateDots(index) {
    carouselDots.forEach((dot, i) => {
      dot.style.opacity = i === index ? '1' : '0.45';
      dot.style.transform = i === index ? 'scale(1.2)' : 'scale(1)';
    });
  }

  if (heroSlides.length > 0) {
    let currentHeroSlide = 0;

    function showSlide(index) {
      heroSlides.forEach((slide, i) => {
        slide.style.opacity = i === index ? '1' : '0';
        slide.style.pointerEvents = i === index ? 'all' : 'none';
        slide.style.zIndex = i === index ? '2' : '1';
      });
      updateDots(index);
    }

    function nextSlide() {
      currentHeroSlide = (currentHeroSlide + 1) % heroSlides.length;
      showSlide(currentHeroSlide);
    }

    function prevSlide() {
      currentHeroSlide = (currentHeroSlide - 1 + heroSlides.length) % heroSlides.length;
      showSlide(currentHeroSlide);
    }

    let autoPlay = setInterval(nextSlide, 6000);

    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        clearInterval(autoPlay);
        prevSlide();
        autoPlay = setInterval(nextSlide, 6000);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        clearInterval(autoPlay);
        nextSlide();
        autoPlay = setInterval(nextSlide, 6000);
      });
    }

    // Dot click navigation
    carouselDots.forEach(dot => {
      dot.addEventListener('click', () => {
        clearInterval(autoPlay);
        currentHeroSlide = parseInt(dot.dataset.index);
        showSlide(currentHeroSlide);
        autoPlay = setInterval(nextSlide, 6000);
      });
    });

    if (typeof lucide !== 'undefined') lucide.createIcons();
  }

  // --- Floating Free Consultation CTA ---
  const subdirs = ['services','lenders','guides','calculators','blog','weekly-reports','testimonials','case-studies'];
  const inSubdir = subdirs.some(d => window.location.pathname.includes('/' + d + '/'));
  const contactHref = inSubdir ? '../contact.html' : 'contact.html';
  const floatBtn = document.createElement('a');
  floatBtn.href = contactHref;
  floatBtn.className = 'floating-consult';
  floatBtn.setAttribute('aria-label', 'Book a free consultation');
  floatBtn.innerHTML =
    '<span class="fcta-dot"></span>' +
    '<span style="display:flex;flex-direction:column;line-height:1.25;"><span>Get Free</span><span>Consultation</span></span>' +
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
  document.body.appendChild(floatBtn);
});
