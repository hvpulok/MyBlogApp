console.log("Script is connected.");

var formLikedBlog = document.querySelectorAll('#formLikedBlog');

// Add event listener to each formLikedBlog selection and related events
for(var j=0; j < formLikedBlog.length; j++){
	formLikedBlog[j].addEventListener("click", function(){
        this.submit();
	});
}