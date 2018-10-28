let login_form = document.getElementById("login_form")
login_form.onsubmit = function login_validate() {
	var username = document.getElementById("username").value;
	var password = document.getElementById("password").value;
	if(username.length == 0){
		text = "Username cannot be blank";
		document.getElementById("message_login").innerHTML = text;
		return false;
		/**alert(text);
		return false;**/
	}
	if(password.length == 0){
		text = "Password cannot be blank";
		document.getElementById("message_login").innerHTML = text;
		return false;
		/**alert(text);
		return false;**/
	}
	return true;
}

let register_form = document.getElementById("register_form")

register_form.onsubmit = function.register_validate(){
	var username = document.getElementById("username");
	var password = document.getElementById("password");
	var password_confirm = document.getElementById("password confirmation");
	var text;
	text = (username.length == 0) ? "Please enter a username" : null;
	text = (password.length == 0) ? "Please provide a password": null;
	text = (password_confirm.length == 0) ? "Please enter password confirmation" : null;
	text = (password_confirm === password) ? null : "Password and password confirmation do not match";
	switch(text){
		case null:
			return true;
		default:
			document.getElementById("message_register").innerHTML = text;
			return false;
	}
}
