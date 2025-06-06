function buscarVideos() {
    let input = document.getElementById("search_videos").value.toLowerCase();
    let videos = document.querySelectorAll(".video-item");

    let encontrados = 0;

    videos.forEach(video => {
        let text = video.getAttribute("data-title");
        let checkbox = video.querySelector("input");

        if (checkbox.checked) {
            video.style.display = "block";
        } else if (text.includes(input) && encontrados < 15) {
            video.style.display = "block";
            encontrados++;
        } else {
            video.style.display = "none";
        }
    });

    if (input === "") {
        encontrados = 0;
        videos.forEach(video => {
            let checkbox = video.querySelector("input");
            if (checkbox.checked || encontrados < 15) {
                video.style.display = "block";
                encontrados++;
            } else {
                video.style.display = "none";
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const lista = document.getElementById("lista-videos");

    let draggedItem = null;

    document.querySelectorAll(".video-item").forEach(item => {
        item.addEventListener("dragstart", function (event) {
            draggedItem = this;
            setTimeout(() => this.style.display = "none", 0);
        });

        item.addEventListener("dragend", function (event) {
            setTimeout(() => this.style.display = "block", 0);
            draggedItem = null;
        });

        item.addEventListener("dragover", function (event) {
            event.preventDefault();
        });

        item.addEventListener("drop", function (event) {
            event.preventDefault();
            if (draggedItem) {
                this.parentNode.insertBefore(draggedItem, this.nextSibling);
                atualizarOrdem();
            }
        });
    });

    function atualizarOrdem() {
        let ordem = [];
        document.querySelectorAll(".video-item").forEach((item, index) => {
            ordem.push(item.getAttribute("data-id"));
        });

        fetch(atualizarOrdemUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ordem: ordem })
        }).then(response => response.json())
          .then(data => console.log("Ordem atualizada:", data))
          .catch(error => console.error("Erro ao atualizar ordem:", error));
    }
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-video").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            if (!confirm("Tem certeza que deseja remover este vídeo da playlist?")) {
                return;
            }

            let playlistId = this.getAttribute("data-playlist");
            let videoId = this.getAttribute("data-video");  
            let videoItem = this.closest(".video-item");  

            fetch(`/playlists/remover_video/${playlistId}/${videoId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken  
                }
            }).then(response => response.json())
              .then(data => {
                  if (data.status === "success") {
                      videoItem.remove(); 
                  } else {
                      alert(data.message);
                  }
              }).catch(error => console.error("Erro ao remover vídeo:", error));
        });
    });
});

function mostrarModal() {
    console.log("Abrindo modal...");
    document.getElementById("modalRecomendacao").style.display = "block";
}


function fecharModal() {
    document.getElementById("modalRecomendacao").style.display = "none";
}
function buscarUsuarios() {
    let termo = document.getElementById("pesquisarUsuario").value;

    if (termo.length < 1) {
        document.getElementById("listaUsuarios").innerHTML = "";
        return;
    }

    fetch(`/accounts/buscar_usuarios?q=${termo}`)
        .then(response => response.json())
        .then(data => {
            let listaUsuarios = document.getElementById("listaUsuarios");
            listaUsuarios.innerHTML = "";

            if (data.length === 0) {
                listaUsuarios.innerHTML = "<p>Nenhum usuário encontrado.</p>";
            }

            data.forEach(user => {
                let btn = document.createElement("button");
                btn.textContent = user.username;
                btn.classList.add("usuario-btn");
                btn.onclick = () => enviarRecomendacao(user.id);
                listaUsuarios.appendChild(btn);
            });
        })
        .catch(error => console.error("Erro ao buscar usuários:", error));
}

// Enviar a recomendação da playlist
function enviarRecomendacao(usuarioId) {
    let playlistId = document.getElementById("modalRecomendacao").dataset.playlistId;
    
    fetch("/playlists/recomendar_playlist/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `usuario_id=${usuarioId}&playlist_id=${playlistId}`
    })
    .then(response => response.json())
    .then(data => {
        alert(data.success || data.error);
        fecharModalRecomendacao();
    });
}

// Obter o CSRF Token dos cookies para segurança nas requisições POST
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken"))
        ?.split("=")[1];
}

function removerRecomendacao(playlistId) {
    if (confirm("Tem certeza que deseja remover esta recomendação?")) {
        fetch(`/playlists/remover_recomendacao/${playlistId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.href = data.redirect_url;  // Redireciona para a listagem de playlists
        })
        .catch(error => console.error("Erro ao remover recomendação:", error));
    }
}