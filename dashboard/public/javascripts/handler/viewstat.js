$("document").ready(()=>{
setInterval(() => {
fetch("/utils/usrcpu")
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
        console.log(data)
        $("#cpu").html(data["%usr"]);
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
}, 3000);

})