function redirectToPage(url) {
    window.location.href = url;
}

function submitForm() {
    document.getElementById("Form").submit();
}

function confirmDelete() {
    if (confirm("Biztosan törölni szeretné ezt a hirdetést?")) {
        document.getElementById("deleteForm").submit();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var inputElement = document.getElementById("image");
    var previewImageElement = document.getElementById("preview");

    inputElement.addEventListener("change", function (event) {
        var file = event.target.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                previewImageElement.src = e.target.result;
                previewImageElement.style.display = "block"; // Megjelenítjük az előnézetet
            }
            reader.readAsDataURL(file);

            // Frissítjük a rejtett input mezőt a kiválasztott fájl nevével
            document.getElementById("preview_image").value = file.name;
        }
    });
});
