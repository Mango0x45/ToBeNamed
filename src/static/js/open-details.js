function openTarget()
{
	const hash = location.hash.substring(1)
	const details = hash ? document.getElementById(hash) : null
	if (details?.tagName?.toLowerCase() === "details")
		details.open = true;
}

window.addEventListener("load", openTarget);
window.addEventListener("hashchange", openTarget);
