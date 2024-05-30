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

    // Função para atualizar o input hidden com os docentes selecionados
    const updateHiddenInput = () => {
        const selectedDocentes = [];
        docenteItems.forEach(item => {
            if (item.classList.contains('checked')) {
                selectedDocentes.push(item.getAttribute('data-docente'));
            }
        });
        hiddenInput.value = selectedDocentes.join(';');
    };

    // Alterna a classe 'open' no botão de seleção
    selectBtn.addEventListener("click", () => {
        selectBtn.classList.toggle("open");
    });

    // Adiciona ou remove a classe 'checked' nos itens ao clicar
    items.forEach(item => {
        item.addEventListener("click", () => {
            item.classList.toggle("checked");
            const checked = document.querySelectorAll(".docente-item-checkbox.checked");

            if (checked.length > 0) {
                btnText.innerText = `${checked.length} Selecionado${checked.length > 1 ? 's' : ''}`;
            } else {
                btnText.innerText = "Selecionar Docente";
            }

            updateHiddenInput();
        });
    });

    // Selecionar todos os itens
    selectAllButton.addEventListener('click', () => {
        docenteItems.forEach(item => {
            item.classList.add('checked');
        });
        updateHiddenInput();
        const checked = document.querySelectorAll(".docente-item-checkbox.checked");
        btnText.innerText = `${checked.length} Selecionado${checked.length > 1 ? 's' : ''}`;
    });

    // Deselecionar todos os itens
    deselectAllButton.addEventListener('click', () => {
        docenteItems.forEach(item => {
            item.classList.remove('checked');
        });
        updateHiddenInput();
        btnText.innerText = "Selecionar Docente";
    });

    // Inicializa o estado do input hidden quando a página é carregada
    updateHiddenInput();
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


