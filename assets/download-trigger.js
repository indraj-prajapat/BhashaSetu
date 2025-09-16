// When the download button is clicked, wait 1 sec, then trigger hidden button
document.addEventListener("DOMContentLoaded", function () {
    const downloadLink = document.getElementById("download-btn");
    const helperButton = document.getElementById("download-btn-helper");

    if (downloadLink && helperButton) {
        downloadLink.addEventListener("click", function () {
            setTimeout(() => {
                helperButton.click();
            }, 1000); // 1000 ms = 1 second delay
        });
    }
});
