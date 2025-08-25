async function tick(){
try{
const res = await fetch('/price',{cache:'no-store'});
const data = await res.json();
const n = data.now || '';
const pNum = Number.parseFloat(data.price);
const shown = Number.isFinite(pNum)
? pNum.toLocaleString('en-US',{minimumFractionDigits:2, maximumFractionDigits:2})
: String(data.price);
document.getElementById('line').textContent = `${n} | BTC/USDT: ${shown}`;
}catch(e){
document.getElementById('line').textContent = '接続エラー';
}
}
setInterval(tick,1000); tick();