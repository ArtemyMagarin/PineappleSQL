var subscribe = function(event, newclass, newtext, do_link) {
	event.preventDefault ? event.preventDefault() : (event.returnValue=false);
	url = event.target.getAttribute('href');
	var xhr = new XMLHttpRequest();
	xhr.open('GET', url, false);
	xhr.send();
	if (xhr.status != 200) {
	} else {

		if (!newtext) {
			newtext = 'Вы подписаны'
		};

		if (!do_link) {
			elem = document.createElement('span');
		} else {
			elem = document.createElement('a');
		}
		
		elem.innerText = newtext;
		elem.setAttribute('href', url.replace('subscribe', 'unsubscribe'))
		elem.setAttribute('onclick', 'unsubscribe(event)')

		if (newclass) {
			elem.className = event.target.className.replace(/btn-[psldwi][reuani][a-z]+/g, newclass)
		} else {
			newclass = 'btn-danger'
			elem.className = event.target.className.replace(/btn-[psldwi][reuani][a-z]+/g, newclass)

		};

		event.target.parentElement.replaceChild(elem, event.target)
	}
}	

var unsubscribe = function(event, newclass) {
	event.preventDefault ? event.preventDefault() : (event.returnValue=false);
	url = event.target.getAttribute('href');
	var xhr = new XMLHttpRequest();
	xhr.open('GET', url, false);
	xhr.send();
	if (xhr.status != 200) {
	} else {
		if (!newclass) {
			newclass = 'btn-primary'
		};
		console.log(event.target.className)
		event.target.className = event.target.className.replace(/btn-[psldwi][reuani][a-z]+/g, newclass)
		event.target.innerText = 'Подписаться'
		event.target.setAttribute('href', url.replace('unsubscribe', 'subscribe'))
		event.target.setAttribute('onclick', 'subscribe(event, "", "Отписаться", true)')
		event.target.parentElement.innerHTML = event.target.parentElement.innerHTML.replace(/span/, 'a')
	}
}