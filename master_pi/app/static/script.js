function isLoggedIn() {
    if (sessionStorage.getItem('username') == null) {
        window.location.href = "/login"
    }
}

function logout() {
  sessionStorage.removeItem('username')
  window.location.href = "/login"
}

function outputErrors(errors) {
  var output = "<strong>Error:</strong><ul>\n"
  for (e in errors) {
    output += "<li>" + errors[e] + "</li>\n"
  }
  output += "</ul>\n"
  return output
}
