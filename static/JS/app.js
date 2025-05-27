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
const authTabs = document.getElementById('authTabs'); // Sekmeler div'i

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

  const loginDurumu = "{{ login_durumu }}";
  if (loginDurumu === "bil") {
    authTabs.classList.add("hidden");        // Sekmeleri gizle
    loginForm.classList.add("hidden");
    registerForm.classList.add("hidden");
    financeSection.classList.remove("hidden");
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

      authTabs.classList.add('hidden'); // Giriş yapıldıktan sonra sekmeleri gizle
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

  authTabs.classList.add('hidden'); // Sekmeleri gizle
}

function showAuthError(msg) {
  authStatus.style.color = 'red';
  authStatus.textContent = msg;
}

function showAuthSuccess(msg) {
  authStatus.style.color = 'green';
  authStatus.textContent = msg;
}

function showStatus(msg, color) {
  statusDiv.textContent = msg;
  statusDiv.style.color = color;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[m]));
}

// === İşlemleri Getir ===
async function fetchTransactions() {
  if (!currentUser) return;

  try {
    const response = await fetch('/api/transactions', { method: 'GET', credentials: 'include' });
    if (!response.ok) throw new Error('Veri alınamadı.');

    const transactions = await response.json();

    tableBody.innerHTML = '';
    transactions.forEach(t => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${t.id}</td>
        <td>${t.type}</td>
        <td>${parseFloat(t.amount).toFixed(2)}</td>
        <td>${escapeHtml(t.category)}</td>
        <td>${t.date}</td>
        <td>
          <button class="edit" data-id="${t.id}">Düzenle</button>
          <button class="delete" data-id="${t.id}">Sil</button>
        </td>
      `;
      tableBody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
    showStatus('İşlemler yüklenemedi.', 'red');
  }
}

// === Form Gönderimi ===
financeForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const type = document.getElementById('type').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const category = document.getElementById('category').value.trim();
  const date = document.getElementById('date').value;

  if (!type || isNaN(amount) || !category || !date) {
    return showStatus('Lütfen tüm alanları doğru doldurun.', 'red');
  }

  const payload = {
    miktar: amount,
    kategori: category,
    tarih: date
  };

  if (type === 'Gider') payload.aciklama = ''; // Gider için gerekli olabilir

  try {
    // === GÜNCELLEME Mİ EKLEME Mİ? ===
    if (editId !== null) {
      const endpoint = type === 'Gelir' ? `/api/gelir/guncelle/${editId}` : `/api/gider/guncelle/${editId}`;
      const response = await fetch(endpoint, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showStatus('İşlem güncellendi.', 'green');
      } else {
        showStatus(result.message || 'Güncelleme başarısız.', 'red');
      }
    } else {
      const endpoint = type === 'Gelir' ? '/api/gelir/ekle' : '/api/gider/ekle';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showStatus('Yeni işlem eklendi.', 'green');
      } else {
        showStatus(result.message || 'Ekleme başarısız.', 'red');
      }
    }

    fetchTransactions(); // tabloyu yenile
    financeForm.reset();
    financeForm.querySelector('button[type=submit]').textContent = 'Ekle';
    editId = null; // bu önemli
  } catch (err) {
    console.error(err);
    showStatus('Sunucu hatası!', 'red');
  }
});

// === Düzenle/Sil Butonları ===
tableBody.addEventListener('click', async (e) => {
  const id = parseInt(e.target.dataset.id);
  if (e.target.classList.contains('edit')) await editTransaction(id);
  if (e.target.classList.contains('delete')) await deleteTransaction(id);
});

async function editTransaction(id) {
  try {
    const response = await fetch('/api/transactions');
    if (!response.ok) throw new Error('İşlem bulunamadı.');

    const transactions = await response.json();
    const t = transactions.find(tr => tr.id === id);
    if (!t) return;

    document.getElementById('type').value = t.type;  // "Gelir" veya "Gider"
    document.getElementById('amount').value = t.miktar || t.amount;  // önemli!
    document.getElementById('category').value = t.kategori || t.category;
    document.getElementById('date').value = t.tarih || t.date;

    editId = id;
    financeForm.querySelector('button[type=submit]').textContent = 'Güncelle';
    showStatus('Düzenleme modunda...', '#333');
  } catch (err) {
    console.error(err);
    showStatus('İşlem bulunamadı.', 'red');
  }
}

async function deleteTransaction(id) {
  try {
    const response = await fetch('/api/transactions');
    if (!response.ok) throw new Error('İşlem bulunamadı.');

    const transactions = await response.json();
    const t = transactions.find(tr => tr.id === id);
    if (!t) return;

    const endpoint = t.type === 'Gelir' ? `/api/gelir/sil/${id}` : `/api/gider/sil/${id}`;
    const deleteResponse = await fetch(endpoint, { method: 'DELETE' });
    const deleteResult = await deleteResponse.json();

    if (deleteResponse.ok && deleteResult.success) {
      showStatus('İşlem silindi.', 'green');
      fetchTransactions();

      if (editId === id) {
        editId = null;
        financeForm.reset();
        financeForm.querySelector('button[type=submit]').textContent = 'Ekle';
      }
    } else {
      showStatus(deleteResult.message || 'İşlem silinemedi.', 'red');
    }
  } catch (err) {
    console.error(err);
    showStatus('İşlem silinemedi.', 'red');
  }
}

// === Çıkış İşlemi ===
logoutBtn.addEventListener('click', async () => {
  try {
    await fetch('/logout', { method: 'POST' });

    if (currentUser) {
      await fetch('/update_login_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username: currentUser, status: 0 }),
      });
    }

    localStorage.removeItem('loggedInUser');
    currentUser = null;

    financeSection.classList.add('hidden');
    loginForm.classList.remove('hidden');
    loginTab.classList.add('active');
    showAuthSuccess('Çıkış yapıldı.');
  } catch (err) {
    console.error(err);
    showAuthError('Çıkış işlemi sırasında hata oluştu.');
  }
});

// === Grafik Sayfasına Geçiş ===
goToGraphBtn.addEventListener('click', () => {
  window.location.href = '/grafik';
});

const toggleBtn = document.getElementById('toggleThemeBtn');
const body = document.body;

// LocalStorage'dan temayı yükle
if (localStorage.getItem('theme') === 'dark') {
  body.classList.add('dark-mode');
  toggleBtn.textContent = 'Açık Mod';
}

toggleBtn.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  if (body.classList.contains('dark-mode')) {
    toggleBtn.textContent = 'Açık Mod';
    localStorage.setItem('theme', 'dark');
  } else {
    toggleBtn.textContent = 'Koyu Mod';
    localStorage.setItem('theme', 'light');
  }
});
