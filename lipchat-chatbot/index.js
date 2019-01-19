/*var backend_url_w2v = "http://lipchat.dumontierlab.com/w2v";
var backend_url_ont = "http://lipchat.dumontierlab.com/ontology";
var backend_url_qa = "http://lipchat.dumontierlab.com/qa";*/
/*var backend_url_w2v = "http://127.0.0.1:5566";
var backend_url_ont = "http://127.0.0.1:5577";
var backend_url_qa = "http://127.0.0.1:5588";*/
var backend_url_w2v = "http://localhost/w2v";
var backend_url_ont = "http://localhost:8080";
var backend_url_qa = "http://localhost/qa";
var using_ontology = false;
var isEnglishInput = false;
var ontology_support = [];
var ontology_response = '';
var ontology_same_response_count = 0;
var chat_id = 0;
var qa_index = 0;
var qa_data = [];
var response_counter = 0;
var number_of_trys = 0
var use = 0;  // 0 - baduse, 1 - wear and tear or natural disaster
var object = 0; // 0 - bigobject, 1 - smallobject
var cost = 0; // 0 - highcost, 1 - lowcost
var smallobjects = [
"cable",
"chair",
"couch",
"doorknob",
"doorbell",
"doorstep",
"switch",
"spare",
"part",
"handrail",
"key",
"lamp",
"light",
"mailbox",
"letterbox",
"shutter",
"table",
"socket",
"hinge"
]

var bigobjects = [
"bath",
"bed",
"bookshelf",
"cabinet",
"carpet",
"ceiling",
"central heating",
"chimney",
"cooker",
"stove",
"cupboard",
"garbage",
"floor",
"drain",
"dryer",
"electrical",
"faucet",
"tap",
"gutter",
"heating",
"internet",
"lock",
"oven",
"refrigerator",
"roof",
"septic",
"toilet",
"sink",
"stove",
"tv",
"ventilation",
"wall",
"washing",
"window"
]


function getBotResponse() {
  var rawText = $("#textInput").val();
  $("#textInput").val("");
  appendToChat(false, rawText);
  $(".typing").css("display", "block");
  //console.log("kody1");
  isEnglish(rawText, function (isEnglish) {
    //console.log("kody2");
    if (isEnglish) {
      if (using_ontology) {
        //console.log("kody3");
        if ((rawText.toLowerCase() === 'why?' || rawText.toLowerCase() === 'why' || rawText.toLowerCase() === 'how come' || rawText.toLowerCase() === 'explain') && ontology_support.length > 0) {
          //console.log("kody4");
          console.log(ontology_support);
          appendToChat(true, ontology_support.join('<br/>'));
          $(".typing").css("display", "none");
          using_ontology = false;
        } else if(ontology_support.length > 0) {
          //console.log("kody5");
          // Reset ontology flow
          using_ontology = false;
          ontology_response = '';
          ontology_support = [];
          getWatsonResponse(rawText);
        } else {
          getOntologyResponse(rawText);
        }
      } else {
        // Use secondary answers
        if (rawText.toLowerCase().slice(0,2) === 'no' && qa_index > 0 && qa_index < qa_data.length) {
          //console.log("kody6");
          appendToChat(true, qa_data[qa_index]);
          qa_index += 1;
          $(".typing").css("display", "none");
        } else {
          //console.log("kody7");
          // Get new answer
          getWatsonResponse(rawText);
        }
      }
    } else {
      //console.log("kody8");
      appendToChat(true, 'Sorry, I can only understand English conversation.');
      $(".typing").css("display", "none");
    }
  });
}
//Word2Vec
function getW2vResponse(text) {
  $.get(backend_url_ont + "/get_w2v", { msg: text }).done(function(data) {
    if (data) {
      appendToChat(true, data);
      $(".typing").css("display", "none");
    }
  });
}
//DeepQA
function getQaResponse(text) {
  $.get(backend_url_qa + "/lstm", { msg: text }).done(function(data) {
    if (data) {
      if (data[0]) {
        qa_data = data;
        qa_index = 0;
        appendToChat(true, "I found the following answer for you: <br/><br/><span style='font-style: italic;     padding-left: 10px; display: inherit;'>" + data[qa_index] + "</span><br/><br/>" + "Was this answer helpful?");
        qa_index += 1;
      } else {
        appendToChat(true, data);
      }
      $(".typing").css("display", "none");
    }
  });
}
function getWatsonResponse(text) {
  //console.log("kody9");
  //console.log(text);
  $.ajax({ 
    // url: '/frontend/index.php',
    url: 'index.php',
    data: {text: text},
    type: 'post',
    success: function(output) {
      if (output == 'MAINTENANCE_ISSUE') {
        //console.log("kody10");
        console.log(output);
        using_ontology = true;
        chat_id = makeid(16);
        getOntologyResponse(text);
      } else if (output == 'OTHER_ISSUE'){
        //console.log("kody11");
        console.log(output);
        //getQaResponse(text);

        // Using word2vec temp
         getW2vResponse(text);
      } else {
        appendToChat(true, output);
        $(".typing").css("display", "none");
      }
    },
    error: function (err) {
      //console.log("kody12");
      //console.log(err);

      // appendToChat(true, 'Sorry, I can not help you with that');
      // $(".typing").css("display", "none");

      // Fallback
      getWatsonResponse('help');
      // getQaResponse(text);
      // getW2vResponse(text);

    }
  });
}





function displayResponse(txt) {
  $(".typing").css("display", "block");
    setTimeout(function(){
      $(".typing").css("display", "none");
      appendToChat(true, txt);
    },800);
}







function getOntologyResponse(text) {
  var lowercaseStr = text.toLowerCase();
  if (response_counter == '0'){
    displayResponse('Your issue seems to be about a property maintenance or property damage issue, is this correct?');
    response_counter++;
  }
  else if (response_counter == '1'){
    if (lowercaseStr.includes("yes") || lowercaseStr == 'y' || lowercaseStr == 'ya' || lowercaseStr.includes("yeah") || lowercaseStr == 'yep'){
      displayResponse('Okay, what item of property was damaged or needs maintenance?');
      response_counter++;
    }
    else if ((lowercaseStr[0] == 'n' && lowercaseStr[1] == 'o') || lowercaseStr == 'n' || lowercaseStr == 'nah' || lowercaseStr.includes("nope") || lowercaseStr == 'nay' || lowercaseStr.includes("nope")){
      displayResponse('Okay, it seems your issue is not related to property damage or maintenance and I do not have enough knowledge to answer it right now. Perhaps I will in the near future! If I can assist with any other issue, you are welcome to mention it now. Otherwise, take care and goodbye!');
      response_counter = 0; 
      using_ontology = false;
      
    } 
    else{
      displayResponse('Hmmm. I do not understand that. I need a yes or no response.');  
      response_counter = 1;
      
    } 
  }
  else if (response_counter == '2'){  // object
    var foundBig = false;
    var foundSmall = false;
    var item = '';
    for (i = 0; i < bigobjects.length; i++) {
      if (lowercaseStr.indexOf(bigobjects[i]) !== -1){
        item = bigobjects[i];
        lowercaseStr = "big";
        foundBig = true;
        break;
      }
    }

    if (!foundBig){
      for (i = 0; i < smallobjects.length; i++) {
        if (lowercaseStr.indexOf(smallobjects[i]) !== -1){
          item = smallobjects[i];
          lowercaseStr = "small";
          foundSmall = true;
          break;
        }
      }
    }

    thing = JSON.stringify(item);
    thing = thing.replace(/^"(.*)"$/, '$1');
    if (lowercaseStr == 'big'){
      displayResponse("If your " + thing + " was damaged, could it have been caused through negligence or irregular maintenance on your part (yes / no)?");
      object = 0;
      response_counter++;
      
    }
    else if (lowercaseStr == 'small'){
      displayResponse("If your " + thing + " was damaged, could it have been caused through negligence or irregular maintenance on your part (yes / no)?");
      object = 1;
      response_counter++;
      
    }
    else { 
      displayResponse('Hmmm. I am sorry, I do not recognize such an object. Perhaps I will in the near future! If I can assist with any other issue, you are welcome to mention it now. Otherwise, take care and goodbye!');  
      response_counter = 0; 
      using_ontology = false;
      
    }
  }
  else if (response_counter == '3'){  // use
    if (lowercaseStr.includes("yes") || lowercaseStr == 'y' || lowercaseStr == 'ya' || lowercaseStr.includes("yeah") || lowercaseStr == 'yep'){
      displayResponse('Can you give an estimate in EURO how much it might cost to address your ' + thing + ' issue?');
      use = 0;
      response_counter++;
      
    }
    else if ((lowercaseStr[0] == 'n' && lowercaseStr[1] == 'o') || lowercaseStr == 'n' || lowercaseStr == 'nah' || lowercaseStr.includes("nope") || lowercaseStr == 'nay' || lowercaseStr.includes("nope")){
      displayResponse('Can you give an estimate in EURO how much it might cost to address your ' + thing + ' issue?');
      use = 1;
      response_counter++;       
      
    } 
    else{
      displayResponse('Hmmm. I do not understand that. I need a yes or no response.');
      
    } 
  }
  else if (response_counter == '4'){  // object response
    var numStr= lowercaseStr.replace( /[^\d\.]*/g, '');

    if (lowercaseStr.includes("yes") || lowercaseStr == 'y' || lowercaseStr == 'ya' || lowercaseStr.includes("yeah") || lowercaseStr == 'yep'){
      displayResponse('How much?');
      //response_counter++;       
      
    }
    else if (numStr.length != 0){
      var num = parseFloat(numStr);
      if (num >= 80.00){
        cost = 0;
      }
      else{
        cost = 1;
      }
      
      $.get(backend_url_ont + "/get_ont", { usage: use, propertyitem: object, actioncost: cost, token: chat_id }).done(function(data) {
        if (data.text){
          var html = '<li class="sent sent-multi" style="margin-top: 15px;"><img src="resources/images/robot512x512.png" alt=""/><p>' + data.text + '</p></li>';
          $("#chatbox").append(html);
          
        }
        $(".typing").css("display", "none");        
      });

      response_counter = 0; 
      using_ontology = false;
      
    } 
    else{
      displayResponse('Hmmm. I am sorry, unfortunately I do not have enough information to help with this issue. If I can assist with any other issue, you are welcome to mention it now. Otherwise, take care and goodbye!');  
      response_counter = 0; 
      using_ontology = false;
      
    }  

  }

/*  $.get(backend_url_ont + "/get", { msg: text, token: chat_id, respcount: response_counter }).done(function(data) {
    appendToChat(true, data.ask[ontology_property]);
    console.log(data);
    if response_c
    if (data.ask) { // chatbot question is sent back
      console.log(Object.keys(data.ask)[0]);
      console.log(data.ask[ontology_property]);
      var ontology_property = Object.keys(data.ask)[0];
      ontology_support = [];
      if (ontology_response === data.ask[ontology_property]) {
        ontology_same_response_count += 1;
        if (ontology_same_response_count > 3) {
          appendToChat(true, "Sorry, I don't know.");

          // reset flow
          ontology_support = [];
          using_ontology = false;
          ontology_response = '';
        } else {
          appendToChat(true, data.ask[ontology_property]);
        }
      } else {
        ontology_same_response_count = 0;
        ontology_response = data.ask[ontology_property];
        appendToChat(true, data.ask[ontology_property]);
      }
    } else if (data.text) { // chatbot response or answer is sent back
      if (data.support) {
        ontology_support = data.support;
        var html = '<li class="sent sent-multi" style="margin-top: 15px;"><img src="resources/images/robot512x512.png" alt=""/><p>' + data.text + '</p></li>';
        for(var i = 0; i < ontology_support.length; i++) {
          html += '<li class="sent sent-multi"><img src="" alt=""/><p style="padding: 5px 5px 5px 30px;';
          if (i === ontology_support.length-1) {
            html += ' margin-bottom: 36px; padding-bottom: 15px;'
          }
          html += '"> - ' + ontology_support[i] + '</p></li>';
        }
        $("#chatbox").append(html);
        $("#messages").animate({ scrollTop: 100000}, 1000);
      } else {
        appendToChat(true, data.text);
      }
    } else {
      /*if (number_of_trys < 3){
        appendToChat(true, 'Sorry, I do not understand...')
      }else {
        appendToChat(true, 'Sorry, I could not be of assistance. Could you try agin?');
        using_ontology = false;
        isEnglishInput = false;
        ontology_support = [];
        ontology_response = '';
        ontology_same_response_count = 0;
        chat_id = 0;
        qa_index = 0;
        qa_data = [];
        number_of_trys = 0;
      }
      number_of_trys++;
    }
    $(".typing").css("display", "none");
  });*/
}













function isEnglish(text, callback) {
  if (isEnglishInput || text.length < 20) {callback(true);}
  else {
    $.get(backend_url_ont + "/language", { msg: text }).done(function(data) {
      if (data == 'english') {isEnglishInput = true;}
      callback(isEnglishInput)
    });
  }
}
function appendToChat(isRobot, text) {
  //console.log("seunanthan!!!")
  var html = '<li class="replies"><img src="" alt=""/><p>' + text + '</p></li>';
  if (isRobot) {html = '<li class="sent"><img src="resources/images/robot512x512.png" alt=""/><p>' + text + '</p></li>';}
  $("#chatbox").append(html);
  $("#messages").animate({ scrollTop: 100000}, 1000);
}
$("#textInput").keypress(function(e) {
  if(e.which == 13) {
    getBotResponse();
  }
});
$("#buttonInput").click(function() {
  getBotResponse();
})
function makeid(length) {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var timestamp = Date.now();

  for (var i = 0; i < length; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text + "_" + timestamp;
}
