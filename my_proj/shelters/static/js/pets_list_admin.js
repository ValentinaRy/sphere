function changeTable(resp) {
    table = document.getElementsByClassName('main-div')[0];
    console.log(resp);
    table.innerHTML = "";
    resp.data.forEach(function(elem, num) {
        table.innerHTML += '<div>'
        + '<div class="pet_elem ">' + "<a href='" + pet_list_link + "../" + elem.id + "'>"
        + '<img height=200 width=200 src="'+media_url+elem.photo+'" class="img-rounded"/>'
        + '<p>'+elem.name.substring(0,22)+'</p>' + '</a></div></div>';
    });
}

function getPage(link, param) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var resp = JSON.parse(this.responseText);
            changeTable(resp);
        }
    };
    req.open("GET", link+param, false);
    req.send();
}

next = document.getElementsByClassName('next');

for (var i=0; i<next.length; i++) {
    next[i].onclick = function () {
        page = document.getElementById('page');
        page.innerHTML++;
        ptype = document.getElementById('id_ptype').value;
        sex = document.getElementById('id_sex').value;
        avail = document.getElementById('id_avail').value;
        params = "?page="+page.innerHTML+"&ptype="+ptype+"&sex="+sex+"&avail="+avail+"&shel_id="+shel_id;
        getPage(ajax_link, params);
    };
}

prev = document.getElementsByClassName('prev');

for (var i=0; i<prev.length; i++) {
    prev[i].onclick = function () {
        page = document.getElementById('page');
        if (page.innerHTML == '1') return;
        page.innerHTML--;
        ptype = document.getElementById('id_ptype').value;
        sex = document.getElementById('id_sex').value;
        avail = document.getElementById('id_avail').value;
        params = "?page="+page.innerHTML+"&ptype="+ptype+"&sex="+sex+"&avail="+avail+"&shel_id="+shel_id;
        getPage(ajax_link, params);
    };
}

find = document.getElementById('find');
find.onclick = function() {
    console.log('btn');
    page = document.getElementById('page');
    ptype = document.getElementById('id_ptype').value;
    sex = document.getElementById('id_sex').value;
    avail = document.getElementById('id_avail').value;
    params = "?page="+page.innerHTML+"&ptype="+ptype+"&sex="+sex+"&avail="+avail+"&shel_id="+shel_id;
    getPage(ajax_link, params);
}
