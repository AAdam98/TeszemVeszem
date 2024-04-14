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
