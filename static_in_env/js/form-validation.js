// Example starter JavaScript for disabling form submissions if there are invalid fields

  'use strict'

  window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation')

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function (form) {
      form.addEventListener('submit', function (event) {
        if (form.checkValidity() === false) {
          event.preventDefault()
          event.stopPropagation()
        }
        else{
            var xhttp = XMLHttpRequest();
            xhttp.open("POST", {% url 'core:accept-checkout'%}, false);
            xhttp.send();
        }
        form.classList.add('was-validated')
      }, false)
    })
  }, false)

