// main.js
import { initActionsToolbar } from "./actions_toolbar.js";
import { initPopups } from "./popup.js";
import { initAddItemForm } from "./item_add.js";
import { initDelete } from "./item_delete.js";
import { initEdit } from "./item_edit.js";
import { renderPhraseToolbar, initPhraseToolbar } from "./phrase_toolbar.js";
import { initMainToolbar } from "./main_toolbar.js";
import { initLanguage } from "./language.js";
import { initProfile } from "./profile.js";
import { initFeedback } from "./feedback.js";

document.addEventListener("DOMContentLoaded", function () {
    initActionsToolbar();
    initPopups();
    initAddItemForm();
    initDelete();
    initEdit();
    initPhraseToolbar();
    renderPhraseToolbar();
    initMainToolbar();
    initLanguage();
    initProfile();
    initFeedback();
    const loader = document.getElementById("loader");
    if(loader) {
        loader.style.display = "none"; // Hide loader once content is loaded
    }
});
