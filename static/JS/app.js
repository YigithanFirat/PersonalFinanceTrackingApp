// === Elemanlar ===
const loginTab = document.getElementById('loginTab');
const registerTab = document.getElementById('registerTab');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const authStatus = document.getElementById('authStatus');
const financeSection = document.getElementById('financeSection');
const goToGraphBtn = document.getElementById('goToGraph');
const financeForm = document.getElementById('financeForm');
const tableBody = document.querySelector('#transactionsTable tbody');
const statusDiv = document.getElementById('status');
const logoutBtn = document.getElementById('logoutBtn');

// === Kullanıcı Durumu ===
let currentUser = localStorage.getItem('loggedInUser');
let editId = null;

// === Sayfa Yüklendiğinde ===
document.addEventListener('DOMContentLoaded', () => {
  if (currentUser) {
    authStatus.style.color = 'green';
    authStatus.textContent = `${currentUser} olarak giriş yapıldı.`;
    showFinanceSection();
    fetchTransactions();
  }
});

// === Sekme Geçişleri ===
loginTab.addEventListener('click', () => switchTab('login'));
registerTab.addEventListener('click', () => switchTab('register'));

function switchTab(tab) {
  const isLogin = tab === 'login';
  loginTab.classList.toggle('active', isLogin);
  registerTab.classList.toggle('active', !isLogin);
  loginForm.classList.toggle('hidden', !isLogin);
  registerForm.classList.toggle('hidden', isLogin);
  authStatus.textContent = '';
}

// === Kayıt İşlemi ===
registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('registerUsername').value.trim();
  const email = document.getElementById('registerEmail').value.trim();
  const password = document.getElementById('registerPassword').value.trim();

  if (!username || !email || !password) {
    return showAuthError('Lütfen tüm alanları doldurun.');
  }

  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });

    const result = await response.json();
    if (response.ok) {
      showAuthSuccess(result.message || 'Kayıt başarılı! Giriş yapabilirsiniz.');
      registerForm.reset();
      switchTab('login');
    } else {
      showAuthError(result.message || 'Kayıt başarısız.');
    }
  } catch (err) {
    console.error('Sunucu hatası:', err);
    showAuthError('Sunucu hatası!');
  }
});

// === Giriş İşlemi ===
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('loginUsername').value.trim();
  const password = document.getElementById('loginPassword').value.trim();

  if (!username || !password) {
    return showAuthError('Lütfen kullanıcı adı ve şifreyi doldurun.');
  }

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    if (response.ok) {
      currentUser = username;
      localStorage.setItem('loggedInUser', currentUser);

      await fetch('/update_login_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, status: 1 }),
      });

      showAuthSuccess(`${currentUser} olarak giriş yapıldı.`);
      showFinanceSection();
      fetchTransactions();
      loginForm.reset();
    } else {
      showAuthError(result.message || 'Giriş başarısız.');
    }
  } catch (err) {
    console.error(err);
    showAuthError('Sunucu hatası!');
  }
});

// === UI Yardımcıları ===
function showFinanceSection() {
  loginForm.classList.add('hidden');
  registerForm.classList.add('hidden');
  financeSection.classList.remove('hidden');
  loginTab.classList.remove('active');
  registerTab.classList.remove('active');
}

function showAuthError(msg) {
  authStatus.style.color = 'red';
  authStatus.textContent = msg;
}

function showAuthSuccess(msg) {
  authStatus.style.color = 'green';
  authStatus.textContent = msg;
}

// === Transaction İşlemleri ===
function getTransactions() {
  return JSON.parse(localStorage.getItem(`transactions_${currentUser}`) || '[]');
}

function saveTransactions(transactions) {
  localStorage.setItem(`transactions_${currentUser}`, JSON.stringify(transactions));
}

function fetchTransactions() {
  const transactions = getTransactions();
  tableBody.innerHTML = '';

  transactions.forEach(t => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${t.id}</td>
      <td>${t.type}</td>
      <td>${t.amount.toFixed(2)}</td>
      <td>${escapeHtml(t.category)}</td>
      <td>${t.date}</td>
      <td>
        <button class="edit" data-id="${t.id}">Düzenle</button>
        <button class="delete" data-id="${t.id}">Sil</button>
      </td>
    `;
    tableBody.appendChild(tr);
  });
}

    const loginDurumu = "{{ login_durumu }}";

    document.addEventListener("DOMContentLoaded", function () {
      if (loginDurumu === "bil") {
        // Giriş yapılmışsa giriş ve kayıt sekmelerini/formlarını gizle
        document.getElementById("authTabs").classList.add("hidden");
        document.getElementById("loginForm").classList.add("hidden");
        document.getElementById("registerForm").classList.add("hidden");
        document.getElementById("financeSection").classList.remove("hidden");
      }
    });

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[m]));
}

// === Yeni veya Güncelleme İşlemi ===
financeForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const type = document.getElementById('type').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const category = document.getElementById('category').value.trim();
  const date = document.getElementById('date').value;

  if (!type || isNaN(amount) || !category || !date) {
    return showStatus('Lütfen tüm alanları doğru doldurun.', 'red');
  }

  let transactions = getTransactions();

  if (editId !== null) {
    const idx = transactions.findIndex(t => t.id === editId);
    if (idx !== -1) {
      transactions[idx] = { id: editId, type, amount, category, date };
      showStatus('İşlem başarıyla güncellendi.', 'green');
    }
    editId = null;
  } else {
    const newId = transactions.length > 0 ? Math.max(...transactions.map(t => t.id)) + 1 : 1;
    transactions.push({ id: newId, type, amount, category, date });
    showStatus('Yeni işlem eklendi.', 'green');
  }

  saveTransactions(transactions);
  fetchTransactions();
  financeForm.reset();
  financeForm.querySelector('button[type=submit]').textContent = 'Ekle';
});

function showStatus(msg, color) {
  statusDiv.textContent = msg;
  statusDiv.style.color = color;
}

// === Düzenle/Sil Butonları ===
tableBody.addEventListener('click', (e) => {
  const id = parseInt(e.target.dataset.id);
  if (e.target.classList.contains('edit')) editTransaction(id);
  if (e.target.classList.contains('delete')) deleteTransaction(id);
});

function editTransaction(id) {
  const t = getTransactions().find(tr => tr.id === id);
  if (!t) return;

  document.getElementById('type').value = t.type;
  document.getElementById('amount').value = t.amount;
  document.getElementById('category').value = t.category;
  document.getElementById('date').value = t.date;

  editId = id;
  financeForm.querySelector('button[type=submit]').textContent = 'Güncelle';
  showStatus('Düzenleme modunda...', '#333');
}

function deleteTransaction(id) {
  let transactions = getTransactions().filter(t => t.id !== id);
  saveTransactions(transactions);
  fetchTransactions();
  showStatus('İşlem silindi.', 'green');

  if (editId === id) {
    editId = null;
    financeForm.reset();
    financeForm.querySelector('button[type=submit]').textContent = 'Ekle';
  }
}

// === Çıkış İşlemi ===
logoutBtn.addEventListener('click', async () => {
  try {
    const response = await fetch('/logout', { method: 'POST' });
    const result = await response.json();

    if (currentUser) {
      await fetch('/update_login_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: currentUser, status: 0 }),
      });
    }

    localStorage.removeItem('loggedInUser');
    currentUser = null;

    financeSection.classList.add('hidden');
    loginForm.classList.remove('hidden');
    loginTab.classList.add('active');
    showAuthSuccess(result.message || 'Çıkış yapıldı.');
  } catch (err) {
    console.error(err);
    showAuthError('Çıkış işlemi sırasında hata oluştu.');
  }
});

// === Grafik Sayfasına Geçiş ===
goToGraphBtn.addEventListener('click', () => {
  window.location.href = '/grafik';
});