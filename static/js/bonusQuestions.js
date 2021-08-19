// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // if (sortDirection === "asc") {
    //     const firstItem = items.shift()
    //     if (firstItem) {
    //         items.push(firstItem)
    //     }
    // } else {
    //     const lastItem = items.pop()
    //     if (lastItem) {
    //         items.push(lastItem)
    //     }
    // }

    // if (sortDirection === "asc") {
    //     items = items.sort()
    // } else {
    //     items = items.sort(function (first_element, second_element) {
    //         if (first_element > second_element) {
    //             return -1;
    //         }
    //         if (second_element > first_element) {
    //             return 1;
    //         }
    //         return 0;
    //     });
    // }
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

    return sortedItems
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // for (let i=0; i<filterValue.length; i++) {
    //     items.pop()
    //     // console.log(filterValue)
    // }

    if (filterValue === '') {
        return items
    }
    else if (filterValue.toLowerCase().startsWith('description:')) {
        return items.filter(item => item["Description"].includes(filterValue.split(':')[1]))
    }
    else if (filterValue.toLowerCase().startsWith('!description:')) {
        return items.filter(item => !item["Description"].includes(filterValue.split(':')[1]))
    }
    else if (filterValue.startsWith('!')) {
        return items.filter(item => !item["Title"].includes(filterValue.slice(1)));
    } else if (filterValue !== 'description:' && filterValue !== '!description:') {
        // return items.filter(value => Object.keys(value).some(k => value[k].toLowerCase().includes(filterValue.toLowerCase())));
        return items.filter(item => item["Title"].includes(filterValue));
    }


    return items
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}