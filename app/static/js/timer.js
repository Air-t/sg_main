$(function(){
  // this functionality handles existance of countdoun timer to express remaining
  // time to end of the currently started exam. Once time is finish, JS should
  // redirect user to "Finish Exam page" where finishing utils should be done
  // to properly end the exam.

  console.log("Jolo!");
  var seconds = document.getElementById("seconds")
  var finish = document.getElementById("finish_exam")

  if (seconds) {
    seconds = seconds.innerHTML
    // Set the date we're counting down to
    var ends = new Date();
    ends.setSeconds(ends.getSeconds() + parseInt(seconds));

    // Update the count down every 1 second
    var x = setInterval(function() {

      // Get today's date and time
      var now = new Date().getTime();

      // Find the distance between now and the count down date
      var distance = ends - now;

      // Time calculations for days, hours, minutes and seconds
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      // Display the result in the element with id="demo"
      document.getElementById("timer").innerHTML = hours + "h "
      + minutes + "m " + seconds + "s ";

      // If the count down is finished, write some text
      if (distance < 0) {
        clearInterval(x);
        document.getElementById("timer").innerHTML = "Time is up!";
        finish.click();
      }
    }, 1000);
  }
})
