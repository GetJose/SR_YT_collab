// Função para pegar o CSRF token nos cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Configuração AJAX para incluir CSRF Token automaticamente
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Exibir submenu de recomendações
document.addEventListener("DOMContentLoaded", function() {
    const recommendationMenu = document.getElementById("recommendationMenu");
    const recommendationSubmenu = document.getElementById("recommendationSubmenu");

    if (recommendationMenu && recommendationSubmenu) {
        recommendationMenu.addEventListener("click", function(event) {
            event.preventDefault();
            recommendationSubmenu.style.display =
                recommendationSubmenu.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function(event) {
            if (!recommendationMenu.contains(event.target) && !recommendationSubmenu.contains(event.target)) {
                recommendationSubmenu.style.display = "none";
            }
        });
    }
});


