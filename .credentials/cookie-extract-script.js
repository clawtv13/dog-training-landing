// Pega esto en Console (F12) cuando estés en YouTube logged in
// Copia el output y mándamelo

let cookies = document.cookie.split('; ');
let needed = ['SID', 'HSID', 'SSID', 'APISID', 'SAPISID'];
let found = {};

cookies.forEach(c => {
  let [key, val] = c.split('=');
  if (needed.includes(key)) {
    found[key] = val;
  }
});

console.log('=== YOUTUBE COOKIES ===');
console.log(JSON.stringify(found, null, 2));
console.log('\n✅ Cookies copiadas al clipboard');
copy(JSON.stringify(found, null, 2));
