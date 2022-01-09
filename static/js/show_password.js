'use strict';

function viewPassword() {
    var pw = document.getElementById("password");
    if (pw.type === "password") {
    pw.type = "text";
    }
}