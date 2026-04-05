document.addEventListener('DOMContentLoaded', function() {


    const modal = document.getElementById('stockModal');
    const openBtn = document.getElementById('openModal');
    const closeBtn = document.getElementById('closeModal');


    if (openBtn) {
        openBtn.addEventListener('click', function() {
            modal.style.display = 'block';
        });
    }


    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    const deleteLinks = document.querySelectorAll('.text-danger');

    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            const confirmed = confirm("Tem certeza que deseja remover esta ação da sua carteira?");

            // Se o usuário clicar em "Cancelar" no alerta do navegador,
            // impedimos o link de seguir adiante (event.preventDefault)
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

});


// --- LÓGICA DO MODAL DE EDIÇÃO ---
    const editModal = document.getElementById('editModal');
    const closeEditBtn = document.getElementById('closeEditModal');
    const editForm = document.getElementById('editForm');

    // Inputs do formulário de edição
    const editTickerInput = document.getElementById('editTicker');
    const editQuantityInput = document.getElementById('editQuantity');

    // Seleciona todos os botões "Editar" da tabela
    const editButtons = document.querySelectorAll('.btn-edit');

    editButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            // 1. Pega os dados do botão clicado
            const id = btn.getAttribute('data-id');
            const ticker = btn.getAttribute('data-ticker');
            const quantity = btn.getAttribute('data-quantity');

            // 2. Preenche o Modal
            editTickerInput.value = ticker;
            editQuantityInput.value = quantity;

            // 3. Atualiza a URL de envio do formulário dinamicamente
            // Isso faz o form enviar para /stock/edit/ID_DA_ACAO
            editForm.action = `/main/stock/edit/${id}`;

            // 4. Abre o modal
            editModal.style.display = 'block';
        });
    });

    // Fechar Modal de Edição
    if (closeEditBtn) {
        closeEditBtn.addEventListener('click', function() {
            editModal.style.display = 'none';
        });
    }

    // Fechar clicando fora
    window.addEventListener('click', function(event) {
        if (event.target == editModal) {
            editModal.style.display = 'none';
        }
    });