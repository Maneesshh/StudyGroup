let form = document.getElementById('lobby__form')
let videoCall = document.getElementById('video_call_btn')

var scriptElement = document.currentScript;
var roomid = scriptElement.getAttribute('data-room-id');
console.log(roomid)

let displayName = sessionStorage.getItem('display_name')
let hostId = sessionStorage.getItem('uid')

const csrftoken = getCookie('csrftoken');
if(displayName){
    form.name.value = displayName
}

document.addEventListener('DOMContentLoaded', onPageLoad);
function onPageLoad() {
  changeVideoCallStatus(roomid)
  }



form.addEventListener('submit', (e) => {
    e.preventDefault()

    sessionStorage.setItem('display_name', e.target.name.value)
    sessionStorage.setItem('uid', e.target.hostId.value)
    sessionStorage.setItem('roomId', e.target.room.value)
    let inviteCode = e.target.room.value
    if(!inviteCode){
        inviteCode = String(Math.floor(Math.random() * 10000))
    }
    const data = {
        roomId : inviteCode,
        hostId : e.target.hostId.value
      };
    changeRoomVideoStatus(data);
   // changeVideoCallStatus(inviteCode);
   onPageLoad()
   // console.log(inviteCode);
  //  window.location = `/chat-room/${inviteCode}`;
    var dynamicURL = "/chat-room/" + inviteCode + "/";
    console.log(dynamicURL);
     window.open(dynamicURL, "_blank");
})


async function changeRoomVideoStatus(data) {
    console.log(data)
    fetch(`/api/rooms/call-status/active`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, 
      },
      body: JSON.stringify(data),
    })
      .then(response => {
        if (response.ok) {
            // Request succeeded
            console.log('Status 200: Success');
          } else if (response.status === 404) {
            // Room does not exist
            console.log('Status 404: Room Not Found');
          } else {
            // Other error occurred
            console.log(`Status ${response.status}: Error`);
          }
      })
      .catch(error => {
        console.error('An error occurred:', error);
      });
  }

  // Function to retrieve the CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  
 function changeVideoCallStatus(roomId){

    fetch(`/api/rooms/call-status/${roomId}`, {
        method: 'GET',
      })
        .then(response => {
          if (response.ok) {
            return response.json();          
            } else if (response.status === 404) {
              // Room does not exist
              console.log('Status 404: VideoStatus Not Found');
              videoCall.innerText = 'Group Call'
            } else {
              // Other error occurred
              console.log(`Status ${response.status}: Error`);
              videoCall.innerText = 'Group Call'
            }
        })
        .then(data => {
          //  let video= data.json();
            // Process the extracted data
            //console.log(data);
            if(data.status == 'active'){
                videoCall.innerText = 'Join Call'
            }
            if(data.status == 'inactive' || data.status == null){
                videoCall.innerText = 'Group Call'
            }

            // Do something with the data
          })
        .catch(error => {
          console.error('An error occurred:', error);
          videoCall.innerText = 'Group Call'
        });

 }



 // to scroll downward

 // Get the message box element
const messageBox = document.getElementById('message-box');


// Scroll to the bottom of the message box
messageBox.scrollTop = messageBox.scrollHeight;

// Get the necessary elements
const fileInput = document.getElementById('upload');
const previewDiv = document.getElementById('preview');
const fileNameSpan = document.getElementById('file-name');
const removeButton = document.getElementById('remove-button');

// Add event listener for file input change
fileInput.addEventListener('change', handleFileUpload);

// Function to handle file upload
function handleFileUpload() {
  const file = fileInput.files[0];
  if (file) {
    // Show the preview div
    previewDiv.classList.add('show');

    // Display the file name
    fileNameSpan.textContent = file.name;
  }
}

// Add event listener for remove button click
removeButton.addEventListener('click', removeFile);

// Function to remove the file and hide the preview div
function removeFile() {
  // Clear the file input
  fileInput.value = '';

  // Hide the preview div
  previewDiv.classList.remove('show');
}


function makeUrlsClickable() {
  const msgTextElements = document.getElementsByClassName('msg_text');

  for (let i = 0; i < msgTextElements.length; i++) {
    const msgText = msgTextElements[i].innerHTML;
    const urlRegex = /(https?:\/\/[^\s]+)/g; // Regular expression to match URLs

    // Replace URLs with clickable anchor tags
    const modifiedText = msgText.replace(urlRegex, function (url) {
      return '<a href="' + url + '">' + url + '</a>';
    });

    // Update the content of the div with clickable URLs
    msgTextElements[i].innerHTML = modifiedText;
  }
}

// Call the function to make URLs clickable
makeUrlsClickable();




var appID = 'fe0567a1deda453e946b47aa6a74d931';
var roomName = scriptElement.getAttribute('data-room-id');

var apiUrl = 'https://api.agora.io/v1/apps/' + appID + '/cloud_recording/resourceid/rooms/' + roomName;

var headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer fe0567a1deda453e946b47aa6a74d931' // Replace with your access token or authentication method
};

function checkViewStatus() {
  fetch(apiUrl, {
    method: 'GET',
    headers: headers
  })
  .then(function(response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Failed to retrieve room status');
    }
  })
  .then(function(data) {
    var roomStatus = data.status;
  
    if (roomStatus === '1') {
      console.log('The room ' + roomName + ' is active');
    } else {
      console.log('The room ' + roomName + ' is not active');
    }
  })
  .catch(function(error) {
    console.error('Error:', error.message);
  });
}

// Periodically check the view status every 5 seconds (adjust as needed)
setInterval(checkViewStatus, 5000);