// PWA Install Prompt
let deferredPrompt;
const installButton = document.getElementById('installApp');
const installBanner = document.getElementById('installBanner');

// Регистрация на Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/js/service-worker.js')
      .then(registration => {
        console.log('ServiceWorker registration successful:', registration.scope);
      })
      .catch(err => {
        console.log('ServiceWorker registration failed:', err);
      });
  });
}

// Слушане за beforeinstallprompt евент
window.addEventListener('beforeinstallprompt', (e) => {
  // Предотвратяваме автоматичното показване на prompt
  e.preventDefault();
  deferredPrompt = e;
  
  // Проверка дали потребителят вече е затворил banner-а
  const dismissed = localStorage.getItem('pwa_install_dismissed');
  
  // Показваме нашия custom install banner само ако не е dismiss-нат
  if (installBanner && dismissed !== 'true') {
    installBanner.style.display = 'block';
  }
});

// При клик на install бутона
if (installButton) {
  installButton.addEventListener('click', async () => {
    if (!deferredPrompt) {
      return;
    }
    
    // Показваме install prompt
    deferredPrompt.prompt();
    
    // Чакаме потребителят да избере
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response to install prompt: ${outcome}`);
    
    // Изчистваме prompt
    deferredPrompt = null;
    
    // Скриваме banner и запазваме в localStorage
    if (installBanner) {
      installBanner.style.display = 'none';
      localStorage.setItem('pwa_install_dismissed', 'true');
    }
  });
}

// Затваряне на banner
const closeBanner = document.getElementById('closeBanner');
if (closeBanner) {
  closeBanner.addEventListener('click', () => {
    if (installBanner) {
      installBanner.style.display = 'none';
      // Запазваме в localStorage, че потребителят е затворил banner-а
      localStorage.setItem('pwa_install_dismissed', 'true');
    }
  });
}

// Слушане за успешна инсталация
window.addEventListener('appinstalled', () => {
  console.log('PWA was installed');
  if (installBanner) {
    installBanner.style.display = 'none';
  }
  // Запазваме, че приложението е инсталирано
  localStorage.setItem('pwa_install_dismissed', 'true');
});

// Проверка дали приложението вече е инсталирано (standalone mode)
function isPWAInstalled() {
  return window.matchMedia('(display-mode: standalone)').matches || 
         window.navigator.standalone === true;
}

// Ако е вече инсталирано, не показваме banner
if (isPWAInstalled() && installBanner) {
  installBanner.style.display = 'none';
  localStorage.setItem('pwa_install_dismissed', 'true');
}
