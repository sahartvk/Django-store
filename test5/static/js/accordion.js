var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}



document.getElementById("apply-filter").addEventListener("click", function() {
    var filterAccordion = document.getElementById("filterAccordion");

    // Change the text to "فیلتر شده"
    filterAccordion.innerHTML = "فیلتر شده";

    // Toggle between adding and removing the "active" class
    filterAccordion.classList.toggle("active");

    // Toggle between hiding and showing the active panel
    var panel = filterAccordion.nextElementSibling;
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
});

document.getElementById("clear-filter").addEventListener("click", function() {
    var filterAccordion = document.getElementById("filterAccordion");

    // Change the text back to "فیلتر"
    filterAccordion.innerHTML = "فیلتر";

    // Toggle between adding and removing the "active" class
    filterAccordion.classList.toggle("active");

    // Toggle between hiding and showing the active panel
    var panel = filterAccordion.nextElementSibling;
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }
});