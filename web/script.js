const urlInput = document.getElementById('urlInput');
const pathInput = document.getElementById('pathInput');
const btnDownload = document.getElementById('btnDownload');
const btnCancel = document.getElementById('btnCancel');
const progressBar = document.getElementById('progressBar');
const statusText = document.getElementById('statusText');

let isDownloading = false;

// --- Funções Auxiliares ---

async function pasteFromClipboard() {
    try {
        // Tenta usar a API do navegador primeiro
        const text = await navigator.clipboard.readText();
        urlInput.value = text;
    } catch (err) {
        urlInput.focus();
        setStatus("Use Ctrl+V para colar", true);
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
        // Ícone de loading (Spinner)
        btnDownload.innerHTML = `
            <svg class="spin-svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px;">
                <path d="M12 4V2C6.48 2 2 6.48 2 12h2c0-4.41 3.59-8 8-8z"/>
            </svg>
            Processando...
        `;
    } else {
        // Ícone de Download normal
        btnDownload.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px;">
                <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
            </svg>
            Baixar Agora
        `;
    }
}

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
        setStatus("Erro: Insira um link válido", true);
        urlInput.focus();
        return;
    }
    if (!path) {
        setStatus("Erro: Selecione uma pasta de destino", true);
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
            setStatus("Falha ao iniciar o download", true);
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
        setStatus("Download Concluído com Sucesso!");
    } else {
        setProgress(0);
        if (statusText.innerText !== "Cancelado pelo usuário") {
            setStatus("Download finalizado (verifique erros)", true);
        }
    }
};

window.onDownloadError = function (errorMsg) {
    setStatus("Erro: " + errorMsg, true);
    toggleInterface(false);
    setProgress(0);
};