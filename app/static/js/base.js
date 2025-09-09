// main.js
import { initActionsToolbar } from "./actions_toolbar.js";
import { initPopups } from "./popup.js";
import { initAddItemForm } from "./item_add.js";
import { initDelete } from "./item_delete.js";
import { initEdit } from "./item_edit.js";

document.addEventListener("DOMContentLoaded", function () {
    initActionsToolbar();
    initPopups();
    initAddItemForm();
    initDelete();
    initEdit();
});
