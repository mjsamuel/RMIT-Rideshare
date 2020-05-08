function isLoggedIn() {
    if (sessionStorage.getItem('username') == null) {
        window.location.href = "/login"
        console.log("not logged in");
    }
}
