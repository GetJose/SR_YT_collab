document.addEventListener("DOMContentLoaded", function () {
    

    // Fecha o menu ao clicar fora dele
    document.addEventListener("click", function () {
        document.querySelectorAll(".options-menu").forEach(menu => {
            menu.style.display = "none";
        });
    });
});

// Função para copiar o link do vídeo sem fechar o menu
function copyVideoLink(event, videoId) {
    event.stopPropagation(); // Impede que o clique feche o menu

    let url = `https://www.youtube.com/watch?v=${videoId}`;
    navigator.clipboard.writeText(url).then(() => {
        alert("Link copiado!");
    }).catch(err => console.error("Erro ao copiar link:", err));
}

// Função para abrir a seleção de playlists sem fechar o menu
function openPlaylistSelection(event, videoId) {
    event.stopPropagation(); // Impede que o clique feche o menu

    window.location.href = `/playlists/enviar-video/${videoId}/`;
}

// Função para criar uma nova playlist sem fechar o menu
function openCreatePlaylist(event, videoId) {
    event.stopPropagation(); // Impede que o clique feche o menu

    window.location.href = `/playlists/criar/?video_id=${videoId}`;
}

// Função para alternar menu de opções
function toggleOptionsMenu(event, button) {
    event.stopPropagation(); // Impede que o clique afete o vídeo abaixo

    let menu = button.nextElementSibling;

    // Fecha todos os menus antes de abrir o atual
    document.querySelectorAll(".options-menu").forEach(m => {
        if (m !== menu) m.style.display = "none";
    });

    // Alterna a visibilidade do menu
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}