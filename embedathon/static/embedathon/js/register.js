function checkPassword(form) {
    p1 = form.password.value;
    p2 = form.confirmation.value;

    if (p1 != p2 || p1 == '' || p2 == '') {
        form.password.setCustomValidity("Passwords don't match");
        form.confirmation.setCustomValidity("Passwords don't match");
        return false;
    }
    form.password.setCustomValidity('');
    form.confirmation.setCustomValidity('');
    return true;
}
