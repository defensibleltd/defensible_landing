---
title: "Contact" # in any language you want
url: "/contact"
description: "Drop us a line about anything!"
# Migrate this to Netlify forms?
hidemeta: true
---
<style>
/* Style the form - display items horizontally */
.form-inline {
  display: flex;
  flex-flow: column wrap;
	flex-wrap: wrap;
}

/* Add some margins for each label */
.form-inline label {
  margin: 5px 5px 5px 5px;
}

/* Style the input fields */
.form-inline input, textarea {
  vertical-align: middle;
  margin: 5px 5px 5px 5px;
  padding: 5px;
  background-color: #fff;
  border: 1px solid #ddd;
	width: 100%;
}

/* Style the submit button */
.form-inline button {
  padding: 10px 10px 10px 10px;
  margin: 5px 5px 5px 5px;
  background-color: dodgerblue;
  border: 1px solid #ddd;
  color: white;
	width: 100%;
}

.form-inline button:hover {
  background-color: royalblue;
}

/* Add responsiveness - display the form controls vertically instead of horizontally on screens that are less than 800px wide */
@media (max-width: 800px) {
  .form-inline input {
    margin: 10px 0;
  }

  .form-inline {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>

<form class="form-inline" name="contact" method="POST" data-netlify="true" action="/form_success">
  <p>
    <label>Name: <input type="text" name="name" /></label>
  </p>
  <p>
    <label>Email: <input type="email" name="email" /></label>
  </p>
  <p>
    <label>Message: <textarea name="message"></textarea></label>
  </p>
    <button type="submit">Send</button>
</form>
