function handleSubmit(event) {
    document.getElementById("submitButton").style.display = "none";
    document.getElementById("loadingButton").style.display = "block";
    document.getElementById("myForm").submit();
  }