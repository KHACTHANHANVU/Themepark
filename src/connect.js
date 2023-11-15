
function send_login_info() {
    user = document.getElementById("login-username");
    pssd = document.getElementById("login-password");

    json = {
        user: user,
        password: pssd
    };

    fetch("/connect", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(json)
    });
}

function send_signup_info() {

}