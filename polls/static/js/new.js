//モーダルウィンドウの動作プログラム
//DOM
const modal = document.getElementById('modal');
const del_url = document.getElementById('del_url')
const del_pk = document.getElementById('del_pk')
const closeBtn = document.getElementById('close_btn');

//関数
function del_click(button){
  modal.style.display = 'block';
  const pk = button.dataset.pk;
  const url = button.dataset.url;
  del_url.href = url;
  del_pk.textContent = pk
}
closeBtn.addEventListener('click', function() {
  modal.style.display = 'none';
})