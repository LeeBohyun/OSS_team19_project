document.getElementById("searchform").onsubmit = function () {
    let search_element = document.querySelector("#searchinput");
    const search_value = search_element.value;

    if (!search_value.length) {
        console.log("empty");
        return false;
    } else {
        console.log(search_value);
        return true;
    }
};
