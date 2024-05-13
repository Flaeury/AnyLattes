/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

const selectBtn = document.querySelector(".select-btn"),
      items = document.querySelectorAll(".item");

selectBtn.addEventListener("click", () => {
    selectBtn.classList.toggle("open");
});

const updateInputWithSelected = () => {
    let selected = document.querySelectorAll(".docente-item-checkbox.checked"),
        result = [];

    for (const item of selected) {
        docente = item.getAttribute('data-docente');
        result.push(docente);
    }

    document.getElementById("docentes-input-hidden").value = result.join(';');
};

items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");

        let checked = document.querySelectorAll(".checked"),
            btnText = document.querySelector(".btn-text");

        if(checked && checked.length > 0) {
            btnText.innerText = `${checked.length} Selected`; // Correção aqui
        } else {
            btnText.innerText = "Select Language";
        }

        updateInputWithSelected();
    });
});


// ocultar ou não a barra de navegação.
window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

// Popup alerta de sucesso ou falha, limitado a alguns segundos.
$(document).ready(function(){			
    setTimeout(function() {
	$("#alert").fadeOut("slow", function(){
		$(this).alert('close');
	});				
    }, 500);			
});

// Datatable implementando pesquisa em tabelas.
$(document).ready(function () {
    $('#resultados').DataTable();
});
$(document).ready(function () {
    $('#notas').DataTable();
});
$(document).ready(function () {
    $('#contadorEstratos').DataTable();
});

$(document).ready(function () {
    $('#dadosProducaoIntelectual').DataTable();
});

const spinnerWrapperEl = document.querySelector('.spinner-wrapper');
window.addEventListener('load',()=>{
    spinnerWrapperEl.style.opacity = '0';
    
    setTimeout(()=>{
        spinnerWrapperEl.style.display = 'none';
    },200);

});


