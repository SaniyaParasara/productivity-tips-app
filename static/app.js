async function getJSON(url) {
const res = await fetch(url);
if (!res.ok) throw new Error(`HTTP ${res.status}`);
return res.json();
}


function renderRaw(el, data) {
el.textContent = JSON.stringify(data, null, 2);
}


function cardTemplate(item) {
return `
<article class="card">
<div class="meta">#${item.id} · ${item.category}</div>
<h3>${item.title}</h3>
<p>${item.text}</p>
<div class="meta">tags: ${(item.tags || []).join(', ')}</div>
</article>
`;
}


function renderCards(el, items) {
el.innerHTML = items.map(cardTemplate).join("");
}


async function fetchRandom(n) {
const data = await getJSON(`/api/random?n=${n}`);
renderCards(document.getElementById("cards"), data.items);
renderRaw(document.getElementById("raw"), data);
}


async function fetchSearch(q) {
const data = await getJSON(`/api/search?q=${encodeURIComponent(q)}`);
renderCards(document.getElementById("cards"), data.items);
renderRaw(document.getElementById("raw"), data);
}


// Wire up UI
document.getElementById("btnRandom").addEventListener("click", () => {
const n = Math.max(1, Math.min(10, parseInt(document.getElementById("count").value || "1")));
fetchRandom(n).catch(err => alert(err.message));
});


document.getElementById("btnSearch").addEventListener("click", () => {
const q = document.getElementById("search").value.trim();
if (q.length === 0) return;
fetchSearch(q).catch(err => alert(err.message));
});


// Initial load
fetchRandom(1).catch(console.error);
