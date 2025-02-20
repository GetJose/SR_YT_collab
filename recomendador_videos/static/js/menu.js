document.addEventListener("DOMContentLoaded", function () {
    // Alternar exibição do menu em telas pequenas
    document.querySelector(".menu-toggle").addEventListener("click", function () {
        document.getElementById("menu").classList.toggle("active");
    });

    // Alternar exibição do submenu de recomendações ao clicar
    document.getElementById("recommendationMenu").addEventListener("click", function (event) {
        event.preventDefault();
        document.getElementById("recommendationSubmenu").classList.toggle("open");
    });

    // Fechar submenu se clicar fora dele
    document.addEventListener("click", function (event) {
        let menu = document.querySelector(".menu-recommendations");
        if (!menu.contains(event.target)) {
            document.getElementById("recommendationSubmenu").classList.remove("open");
        }
    });
});

function confirmLogout() {
    return confirm("Tem certeza que deseja sair?");
}
