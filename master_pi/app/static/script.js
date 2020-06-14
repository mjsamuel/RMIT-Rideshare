function isLoggedIn() {
    if (sessionStorage.getItem('username') == null) {
        window.location.href = "/login";
    }
}

function logout() {
  sessionStorage.removeItem('username');
  sessionStorage.removeItem('role');
  window.location.href = "/login";
}

function lockout(roles) {
  // Locks out the page to only the roles specified
  let userRole = sessionStorage.getItem('role')
  var ableToAccess = false;
  for (role in roles) {
    if (userRole == roles[role]) ableToAccess = true;
  }

  if (ableToAccess == false) {
    if (userRole == "default") redirect("");
    else if (userRole == "admin") redirect("admin-console");
    else if (userRole == "manager") redirect("manager-console");
    else if (userRole == "engineer") redirect("engineer-console");
  }
}

function redirect(url) {
  window.location.href = "/" + url;
}

function outputErrors(errors) {
  var output = "<strong>Error:</strong><ul>\n";
  for (e in errors) {
    output += "<li>" + errors[e] + "</li>\n";
  }
  output += "</ul>\n";
  return output;
}
