import { login, register } from '../services/authService.js';
import { navigate } from '../core/router.js';
import { showToast } from '../components/toast.js';

export const template = `
  <div class="flex min-h-[calc(100vh-12rem)] items-center justify-center">
    <div class="w-full flex items-center justify-center px-5 sm:px-8 py-10 sm:py-12">
      <div class="w-full max-w-sm">
        <div id="login-panel">
          <h1 class="text-2xl sm:text-3xl font-semibold mb-2">Log in to Shopify</h1>
          <p class="text-gray-500 text-sm mb-8">Enter your details below</p>
          <form id="login-form" class="space-y-7">
            <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
              <input type="email" id="login-email" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="Email" />
            </div>
            <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
              <input type="password" id="login-password" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="Password" />
            </div>
            <div class="flex items-center justify-between pt-1">
              <button type="submit" class="bg-red-500 hover:bg-red-600 text-white px-10 py-3 rounded text-sm font-medium transition-colors">Log In</button>
              <button type="button" id="forgot-link" class="text-red-500 text-sm hover:underline">Forget Password?</button>
            </div>
            <p class="text-sm text-center text-gray-500 pt-1">
              Don't have an account?
              <button type="button" id="go-register" class="font-semibold underline hover:text-black ml-1">Create Account</button>
            </p>
          </form>
        </div>
        <div id="register-panel" class="hidden">
          <h1 class="text-2xl sm:text-3xl font-semibold mb-2">Create an account</h1>
          <p class="text-gray-500 text-sm mb-8">Enter your details below</p>
          <form id="register-form" class="space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
                <input type="text" id="reg-firstname" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="First Name" />
              </div>
              <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
                <input type="text" id="reg-lastname" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="Last Name" />
              </div>
            </div>
            <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
              <input type="email" id="reg-email" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="Email" />
            </div>
            <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
              <input type="password" id="reg-password" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="Password" />
            </div>
            <div class="border-b border-gray-300 pb-1 focus-within:border-red-500 transition-colors">
              <input type="password" id="reg-confirm" class="w-full text-sm outline-none bg-transparent placeholder-gray-400 py-1" placeholder="Confirm Password" />
            </div>
            <button type="submit" class="w-full bg-red-500 hover:bg-red-600 text-white py-3.5 rounded text-sm font-medium transition-colors">Create Account</button>
            <p class="text-sm text-center text-gray-500">
              Already have an account?
              <button type="button" id="go-login" class="font-semibold underline hover:text-black ml-1">Log in</button>
            </p>
          </form>
        </div>
      </div>
    </div>
  </div>
`;

export function init() {
  const loginPanel = document.getElementById('login-panel');
  const registerPanel = document.getElementById('register-panel');
  document.getElementById('go-register').addEventListener('click', () => {
    loginPanel.classList.add('hidden');
    registerPanel.classList.remove('hidden');
  });
  document.getElementById('go-login').addEventListener('click', () => {
    registerPanel.classList.add('hidden');
    loginPanel.classList.remove('hidden');
  });
  document.getElementById('forgot-link').addEventListener('click', () => {
    showToast('Password reset not available in demo mode', 'info');
  });
  document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    if (!email) { showToast('Please enter your email', 'error'); return; }
    if (!password) { showToast('Please enter your password', 'error'); return; }
    try {
      await login(email, password);
      showToast('Welcome back!', 'success');
      navigate('/');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });
  document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const firstName = document.getElementById('reg-firstname').value.trim();
    const lastName = document.getElementById('reg-lastname').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value;
    const confirm = document.getElementById('reg-confirm').value;
    if (!firstName) { showToast('Please enter your first name', 'error'); return; }
    if (!lastName) { showToast('Please enter your last name', 'error'); return; }
    if (!email || !email.includes('@')) { showToast('Please enter a valid email', 'error'); return; }
    if (!password || password.length < 6) { showToast('Password must be at least 6 characters', 'error'); return; }
    if (password !== confirm) { showToast('Passwords do not match', 'error'); return; }
    try {
      await register({ firstName, lastName, email, password });
      showToast('Account created! Welcome!', 'success');
      navigate('/');
    } catch (err) {
      showToast(err.message, 'error');
    }
  });
}
