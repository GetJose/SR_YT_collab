function buscarVideos() {
    let input = document.getElementById("search_videos").value.toLowerCase();
    let videos = document.querySelectorAll(".video-item");

    let encontrados = 0;

    videos.forEach(video => {
        let text = video.getAttribute("data-title");
        let checkbox = video.querySelector("input");

        // Garante que vídeos já selecionados sempre fiquem visíveis
        if (checkbox.checked) {
            video.style.display = "block";
        } else if (text.includes(input) && encontrados < 15) {
            video.style.display = "block";
            encontrados++;
        } else {
            video.style.display = "none";
        }
    });

    // Se a busca estiver vazia, restaurar os primeiros 15 vídeos + os selecionados
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
    document.querySelectorAll(".remover-video").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            if (!confirm("Tem certeza que deseja remover este vídeo da playlist?")) {
                return;
            }

            let playlistId = this.getAttribute("data-playlist");
            let videoItem = this.closest(".video-item");
            let videoIndex = Array.from(videoItem.parentNode.children).indexOf(videoItem);  

            fetch(`/playlists/remover_video/${playlistId}/${videoIndex}/`, {
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
