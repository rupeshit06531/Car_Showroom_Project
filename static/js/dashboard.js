/* ======================================================
   Car Showroom Management System
   Dashboard JS v2.0
====================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ==========================================
       DataTables Auto Initialize
    ========================================== */

    if (window.jQuery && $.fn.DataTable) {

        $("table").DataTable({
            responsive: true,
            pageLength: 10,
            lengthChange: true,
            autoWidth: false,
            ordering: true,
            searching: true,
            language: {
                search: "Search:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                paginate: {
                    previous: "Previous",
                    next: "Next"
                }
            }
        });

    }

    /* ==========================================
       Counter Animation
    ========================================== */

    document.querySelectorAll(".stat-number").forEach(function (item) {

        let target = parseInt(item.innerText.replace(/[^0-9]/g, ""));

        if (isNaN(target)) return;

        let count = 0;

        let step = Math.max(1, Math.ceil(target / 60));

        let timer = setInterval(function () {

            count += step;

            if (count >= target) {

                count = target;

                clearInterval(timer);

            }

            item.innerText = count.toLocaleString();

        }, 20);

    });

    /* ==========================================
       Fade Animation
    ========================================== */

    document.querySelectorAll(".card, .stat-card").forEach(function (card) {

        card.classList.add("fade-up");

    });

});


/* ==========================================
   Dark Mode
========================================== */

const themeButton = document.getElementById("themeToggle");

if (themeButton) {

    themeButton.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            localStorage.setItem("theme", "dark");

        } else {

            localStorage.setItem("theme", "light");

        }

    });

}

window.addEventListener("load", function () {

    if (localStorage.getItem("theme") === "dark") {

        document.body.classList.add("dark-mode");

    }

});


/* ==========================================
   Bootstrap Tooltips
========================================== */

const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

tooltipTriggerList.forEach(function (tooltipTriggerEl) {

    new bootstrap.Tooltip(tooltipTriggerEl);

});


/* ==========================================
   Bootstrap Popovers
========================================== */

const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

popoverTriggerList.forEach(function (popoverTriggerEl) {

    new bootstrap.Popover(popoverTriggerEl);

});

new Chart(document.getElementById("salesChart"),{
type:"line",
data:{
labels:months,
datasets:[{
label:"Sales",
data:sales,
borderWidth:3,
fill:true,
tension:.4
}]
}
});

new Chart(document.getElementById("companyChart"),{
type:"doughnut",
data:{
labels:companies,
datasets:[{
data:company_count
}]
}
});

new Chart(document.getElementById("fuelChart"),{
type:"pie",
data:{
labels:fuel_labels,
datasets:[{
data:fuel_count
}]
}
});

new Chart(document.getElementById("revenueChart"),{
type:"bar",
data:{
labels:months,
datasets:[{
label:"Revenue",
data:revenue
}]
}
});