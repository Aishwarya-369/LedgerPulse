function checkStoredUser() {
  const stored = localStorage.getItem("lp_user");
  const storedWs = localStorage.getItem("lp_workspaces");

  // Force redirect to login page if user is not authenticated
  if (!stored || !storedWs) {
    window.location.href = "/login";
    return;
  }

  currentUser = JSON.parse(stored);
  userWorkspaces = JSON.parse(storedWs);
  applyUserSession();
}

function handleLogout() {
  localStorage.removeItem("lp_user");
  localStorage.removeItem("lp_workspaces");
  currentUser = null;
  userWorkspaces = [];
  activeWorkspaceId = null;
  // Redirect back to landing page on sign out
  window.location.href = "/";
}
