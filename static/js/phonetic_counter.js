//widged variables declarations
var input_text_radiobutton = document.getElementById("customRadioInline1");
var input_file_radiobutton = document.getElementById("customRadioInline2");
var load_button_label = document.getElementById('load_button_label');
var load_button = document.getElementById('load_button');
var start_button = document.getElementById('start_button');
var user_text = document.getElementById('exampleFormControlTextarea1');
var loaded_text_label = document.getElementById('loaded_text_label');
var results_label = document.getElementById('results_label');
var close_link = document.getElementById('close_link');
var user_text_state = "input_text"
var results_text = document.getElementById('final_results');


//radiobuttons functionality START
//////////////////////////////////
input_file_radiobutton.addEventListener('click', function (e) {
  if (input_file_radiobutton.checked) {
    load_button_label.className = "btn btn-outline-primary btn-sm";
    load_button.disabled = false;
    user_text.value = "";
    user_text.disabled = true;
    user_text_state = "input_file";
  }
})

input_text_radiobutton.addEventListener('click', function (e) {
  if (input_text_radiobutton.checked && user_text_state=="input_file") {
    user_text.disabled = false;
    load_button_label.className = "btn btn-outline-dark btn-sm";
    load_button.disabled = true;
    user_text.value = "";
    loaded_text_label.innerText = "";
    user_text_state = "input_text";

  }
})
//radiobuttons functionality ENDED
//////////////////////////////////



// load button functionality START
//////////////////////////////////

// this function clears the value kept in the button so that
// a file is loaded each time, not only when a new file is chose
load_button.addEventListener('click', function (e) {
  load_button.value = "";
});


var openFile = function(event) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function(){
    var text = reader.result;
    var fileName = document.getElementById('load_button').files[0].name;
    user_text.value = text;
    loaded_text_label.innerText = "Loaded: " + fileName;
    user_text.disabled = true;
  };
  reader.readAsText(input.files[0]);
};
// load button functionality ENDED
//////////////////////////////////



// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// JS - PYTHON INTERFACE FUNCTIONALITY
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



// American consonants
document.getElementById('count_consonants_american').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function (e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of consonants for American English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_consonants_a/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});



// British consonants
document.getElementById('count_consonants_british').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of consonants for British English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_consonants_b/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});


// American vowels
document.getElementById('count_vowels_american').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of vowels for American English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_vowels_a/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});



// British vowels
document.getElementById('count_vowels_british').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of vowels for British English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_vowels_b/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});



// American phonemes
document.getElementById('count_phonemes_american').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of phonemes for American English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_phonemes_a/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});



// British phonemes
document.getElementById('count_phonemes_british').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of phonemes for British English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_phonemes_b/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});



// syllables
document.getElementById('count_syllables').addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let result = response_object.result;
      results_text.innerText = "The number of syllables for both American English and British English is " + result + ".";
      document.getElementById('the_spinner').style.visibility = 'hidden';
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');
  document.getElementById('the_spinner').style.visibility = 'visible';
  results_text.innerText = "Please wait, processing..."

  xhr.open('POST', '/count_syllables/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);
});
