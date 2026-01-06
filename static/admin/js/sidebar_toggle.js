document.addEventListener('DOMContentLoaded', function() {
    const filterEl = document.getElementById('changelist-filter');
    const changelistEl = document.getElementById('changelist');

    if (filterEl && changelistEl) {
        // Create the Toggle Button (The Slicer)
        const toggleBtn = document.createElement('div');
        toggleBtn.id = 'sidebar-slicer';
        toggleBtn.innerHTML = '◀'; // Arrow icon
        toggleBtn.title = 'Toggle Filter Sidebar';

        // Add button to the page
        document.body.appendChild(toggleBtn);

        toggleBtn.addEventListener('click', function() {
            filterEl.classList.toggle('sidebar-hidden');
            changelistEl.classList.toggle('full-width');

            // Flip the arrow direction
            if (filterEl.classList.contains('sidebar-hidden')) {
                toggleBtn.innerHTML = '▶';
                toggleBtn.style.right = '0';
            } else {
                toggleBtn.innerHTML = '◀';
                toggleBtn.style.right = '240px'; // Matches filter width
            }
        });
    }
});