<?php

if (!isset($_POST['text']) || $_POST['text'] == '') {
    BadRequest();
}
$String = $_POST['text'];

$ibm_endpoint = "https://gateway.watsonplatform.net/assistant/api";
$ibm_workspace = "/v1/workspaces/4c1c95e2-eca9-4632-bd53-181266efdb95/message/";
$ibm_version = "?version=2018-02-16";
$ibm_username = "fd25cce6-e21e-4222-8fa5-808102a17a34";
$ibm_password = "nUOa1z1ON2Kt";

// Build request
$aParams = array(
  'input' => array(
    'text' => $String,
  )
);
$User = $ibm_username . ":" . $ibm_password;

$curl = curl_init();
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($aParams));
curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($curl, CURLOPT_USERPWD, $User);
curl_setopt($curl, CURLOPT_URL, $ibm_endpoint . $ibm_workspace . $ibm_version);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE);
curl_setopt($curl, CURLOPT_HTTPHEADER, [
  'Content-Type: application/json'
]);

$result = curl_exec($curl);

curl_close($curl);

if ($result == false) {
  BadRequest();
}

$decoded = json_decode($result, true);
if (isset($decoded['output']['text']) && count($decoded['output']['text']) > 0) {
  die($decoded['output']['text'][0]);
} else {
  echo $result;
  echo "SEUNNASDA";
  BadRequest();
}

function BadRequest() {
  header("HTTP/1.0 400 Bad Request");
  die('Bad Request');
}

?>