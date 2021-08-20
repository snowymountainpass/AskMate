function getSortedItems(items, sortField, sortDirection) {
    console.log(items);
    console.log(sortField);
    console.log(sortDirection);

    let sortedItems = items;
    if (sortDirection === "asc") {
        sorted_items = items.sort(function (a, b) {
            if (a["Description"] > b["Description"]) {
                return 1;
            }
            if (a["Description"] < b["Description"]) {
                return -1;
            }
            return 0;
        });
    } else {
        sorted_items = items.sort(function (a, b) {
            if (a["Description"] > b["Description"]) {
                return -1;
            }
            if (a["Description"] < b["Description"]) {
                return 1;
            }
            return 0;
        });
    }

    return sortedItems;
}

function getFilteredItems(items, filterValue) {
    console.log(items);
    console.log(filterValue);

    if (filterValue === "") {
        return items;
    } else if (filterValue.toLowerCase().startsWith("description:")) {
        return items.filter((item) =>
            item["Description"].includes(filterValue.split(":")[1])
        );
    } else if (filterValue.toLowerCase().startsWith("!description:")) {
        return items.filter(
            (item) => !item["Description"].includes(filterValue.split(":")[1])
        );
    } else if (filterValue.startsWith("!")) {
        return items.filter(
            (item) => !item["Title"].includes(filterValue.slice(1))
        );
    } else if (
        filterValue !== "description:" &&
        filterValue !== "!description:"
    ) {
        return items.filter((item) => item["Title"].includes(filterValue));
    }

    return items;
}

function toggleTheme() {
    console.log("toggle theme");
}

function increaseFont() {
    console.log("increaseFont");
}

function decreaseFont() {
    console.log("decreaseFont");
}
