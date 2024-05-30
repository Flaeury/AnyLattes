/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 
document.addEventListener('DOMContentLoaded', function () {
    const selectBtn = document.querySelector(".select-btn");
    const items = document.querySelectorAll(".item");
    const selectAllButton = document.getElementById('select-all');
    const deselectAllButton = document.getElementById('deselect-all');
    const docenteItems = document.querySelectorAll('.docente-item');
    const hiddenInput = document.getElementById("docentes-input-hidden");
    const btnText = document.querySelector(".btn-text");

  
    const updateSelectedItems = () => {
        const checkedItems = document.querySelectorAll(".docente-item-checkbox.checked");
        const totalSelected = checkedItems.length;

        btnText.innerText = totalSelected > 0 ? `${totalSelected} Selecionado${totalSelected > 1 ? 's' : ''}` : "Selecione um docente";

        const selectedDocentes = Array.from(checkedItems).map(item => item.getAttribute('data-docente'));
        hiddenInput.value = selectedDocentes.join(';');
    };

   
    const toggleAllItems = (checked) => {
        docenteItems.forEach(item => {
            item.classList.toggle('checked', checked);
        });
        updateSelectedItems();
    };

  
    selectBtn.addEventListener("click", () => {
        selectBtn.classList.toggle("open");
    });

   
    items.forEach(item => {
        item.addEventListener("click", () => {
            item.classList.toggle("checked");
            updateSelectedItems();
        });
    });

   
    selectAllButton.addEventListener('click', () => {
        toggleAllItems(true);
    });

   
    deselectAllButton.addEventListener('click', () => {
        toggleAllItems(false);
    });

   
    updateSelectedItems();

   
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});



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


