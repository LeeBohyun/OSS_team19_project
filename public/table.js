function sortTable(target) {
    const t = sort_info[target];
    const idx = t[0];
    const state = t[1];

    sort_info[target] = [idx, !state];

    table = document.querySelector("#tablebody");
    let rows = table.rows;

    let values = [];

    let switching = true,
        x,
        y;
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 0; i < rows.length - 1; i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[idx];
            y = rows[i + 1].getElementsByTagName("TD")[idx];

            if (state) {
                if (parseInt(x.textContent) > parseInt(y.textContent)) {
                    shouldSwitch = true;
                    break;
                }
            } else {
                if (parseInt(x.textContent) < parseInt(y.textContent)) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}
