import './style.css';
import { initRouter } from './core/router.js';
import { renderNavbar } from './components/navbar.js';
import { renderFooter } from './components/footer.js';

renderNavbar();
renderFooter();
initRouter();
