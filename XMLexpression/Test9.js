function check(elem){
	if(elem.value != elem.attributes['data-answer'].value){
		alert("Your answer is wrong!");
		elem.focus();
		return false;
	}
	alert("Your answer is right!");
	elem.focus();
	return true;
}