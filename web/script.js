const urlInput = document.getElementById('urlInput');
const pathInput = document.getElementById('pathInput');
const btnDownload = document.getElementById('btnDownload');
const btnCancel = document.getElementById('btnCancel');
const progressBar = document.getElementById('progressBar');
const statusText = document.getElementById('statusText');

// Elementos do Modal
const modalOverlay = document.getElementById('customModal');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');
const modalIconArea = document.getElementById('modalIconArea');

let isDownloading = false;

// --- Funções Auxiliares ---

async function pasteFromClipboard() {
    try {
        const text = await navigator.clipboard.readText();
        urlInput.value = text;
    } catch (err) {
        urlInput.focus();
        showAlert('Atenção', 'Não foi possível acessar a área de transferência. Use Ctrl+V.', 'info');
    }
}

function clearInput() {
    urlInput.value = "";
    urlInput.focus();
    setStatus("Pronto");
}

function toggleFullscreen() {
    pywebview.api.toggle_fullscreen();
}

function setStatus(text, isError = false) {
    statusText.innerText = text;
    statusText.style.color = isError ? '#ff4444' : '#a0a0a0';
}

function setProgress(percent) {
    progressBar.style.width = percent + '%';
}

function toggleInterface(downloading) {
    isDownloading = downloading;
    btnDownload.disabled = downloading;
    btnCancel.disabled = !downloading;
    urlInput.disabled = downloading;

    if (downloading) {
        btnDownload.innerHTML = `
            <svg class="spin-svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px;">
                <path d="M12 4V2C6.48 2 2 6.48 2 12h2c0-4.41 3.59-8 8-8z"/>
            </svg>
            Processando...
        `;
    } else {
        btnDownload.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px;">
                <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
            </svg>
            Baixar Agora
        `;
    }
}

// --- Funções do Modal ---

function showAlert(title, message, type = 'info') {
    modalTitle.innerText = title;
    modalMessage.innerText = message;

    let iconSvg = '';

    if (type === 'success') {
        iconSvg = `<svg class="icon-success" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 13.17l7.59-7.59L19 7l-9 9z"/></svg>`;
    } else if (type === 'error') {
        iconSvg = `<svg class="icon-error" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>`;
    } else {
        iconSvg = `<svg class="icon-info" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>`;
    }

    modalIconArea.innerHTML = iconSvg;

    modalOverlay.style.display = 'flex';
    // Timeout pequeno para permitir a transição CSS de opacidade
    setTimeout(() => {
        modalOverlay.classList.add('show');
    }, 10);
}

function closeModal() {
    modalOverlay.classList.remove('show');
    setTimeout(() => {
        modalOverlay.style.display = 'none';
    }, 300); // Espera a animação terminar
}

// Fecha o modal se clicar fora do conteúdo
modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
        closeModal();
    }
});

// --- Comunicação com Python ---

async function chooseFolder() {
    if (isDownloading) return;
    const path = await pywebview.api.select_folder();
    if (path) {
        pathInput.value = path;
    }
}

function startDownload() {
    const url = urlInput.value.trim();
    const path = pathInput.value.trim();

    if (!url) {
        showAlert("Campo Obrigatório", "Por favor, insira um link válido do YouTube.", "error");
        return;
    }
    if (!path) {
        showAlert("Campo Obrigatório", "Por favor, selecione uma pasta de destino para salvar o arquivo.", "error");
        return;
    }

    const folderName = document.getElementById('folderName').value;
    const createSubfolder = document.getElementById('createSubfolder').checked;
    const formatMode = document.querySelector('input[name="format"]:checked').value;

    toggleInterface(true);
    setProgress(0);
    setStatus("Inicializando...");

    pywebview.api.start_download(url, path, formatMode, folderName, createSubfolder).then((started) => {
        if (!started) {
            toggleInterface(false);
            showAlert("Erro", "Não foi possível iniciar o download. Verifique o link e tente novamente.", "error");
        }
    });
}

function cancelDownload() {
    if (isDownloading) {
        setStatus("Cancelando...");
        pywebview.api.cancel_download();
    }
}

// --- Callbacks do Python ---

window.updateProgress = function (percent, message, status) {
    setProgress(percent);
    setStatus(message);
};

window.onDownloadComplete = function (success) {
    toggleInterface(false);
    if (success) {
        setProgress(100);
        setStatus("Concluído!");
        showAlert("Sucesso!", "O download foi concluído com sucesso. O arquivo está na pasta selecionada.", "success");
    } else {
        setProgress(0);
        if (statusText.innerText !== "Cancelado pelo usuário") {
            setStatus("Falhou");
            // O alerta de erro detalhado já vem do onDownloadError ou pode ser chamado aqui se necessário
        }
    }
};

window.onDownloadError = function (errorMsg) {
    toggleInterface(false);
    setProgress(0);
    setStatus("Erro");
    showAlert("Ocorreu um Erro", "Detalhes: " + errorMsg, "error");
};