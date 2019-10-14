var host = 'localhost';
var port = 11883;
var useTLS = false;
var cleansession = false;
var mqtt;
var clientId;
var reconnectTimeout = 2000;

var livingTempSensorCanva = document.getElementById('living-chart').getContext('2d');
var labelslivingTempSensor = new Array();
var datalivingTempSensor = new Array();

var basementTempSensorChartCanva = document.getElementById('basement-chart').getContext('2d');
var labelsbasementTempSensor = new Array();
var databasementTempSensor = new Array();


var topics = [
    'home/basement/temp',
    'home/living/temp',
    'home/front/door',
    'home/back/door',
    'home/kitchen/door',
    'home/front/window',
    'home/back/window',
    'home/kitchen/window',
]

var itemsTable = ["timestamp", "topic", "message"];

function loadMessages() {

  // DRAW THE HTML TABLE
  let perrow = 3, // 3 items per row
      html = "<table class='table table-bordered table-striped mb-0'><tr>";

  // Loop through array and add table cells
  for (let i=0; i<itemsTable.length; i++) {
    html += "<td>" + itemsTable[i] + "</td>";
    // Break into next row
    let next = i+1;
    if (next%perrow==0 && next!=itemsTable.length) {
      html += "</tr><tr>";
    }
  }
  html += "</tr></table>";

  // ATTACH HTML TO CONTAINER
  document.getElementById("tableDinamic").innerHTML = html;
}

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

function MQTTconnect() {
    if (typeof path == "undefined") {
        path = '/mqtt';
    }
    clientId = "mqtt_panel" + uuidv4();
    mqtt = new Paho.Client(host, Number(port), clientId);
    var options = {
        invocationContext: { host: host, port: port, path: path, clientId: clientId },
        keepAliveInterval: 60,
        userName: 'mosquitto',
        password: 'mosquitto',
        reconnect: true,
        timeout: 3,
        useSSL: useTLS,
        cleanSession: cleansession,
        onSuccess: onConnect,
        onFailure: function(message) {
            $('#status').html("Connection failed: " + message.errorMessage + "Retrying...");
            // setTimeout(MQTTconnect, reconnectTimeout);
        }
    };

    mqtt.onConnectionLost = onConnectionLost;
    mqtt.onMessageArrived = onMessageArrived;
    console.log("Host: " + host + ", Port: " + port + ", Path: " + path + " TLS: " + useTLS + ' Client ID ' + clientId);
    mqtt.connect(options);
};

function onConnect() {
    $('#status').html('Connected to ' + host + ':' + port + path);
    // mqtt.subscribe(topic, { qos: 1 });
    topics.forEach(function(topicName) {
        mqtt.subscribe(topicName, { qos: 0 });
        console.log("subscribed to ", topicName);
    });
    $('#topic').html(topic);
};

function onConnectionLost(response) {
    // setTimeout(MQTTconnect, reconnectTimeout);
    $('#status').html("Connection lost: " + response.errorMessage + ". Reconnecting...");
};

function onMessageArrived(message) {
    var topic = message.destinationName;
    var payload = message.payloadString;
    // console.log("Topic: " + topic + ", Message payload: " + payload);
    $('#message').html(topic + ', ' + payload);
    var message = topic.split('/');
    var area = message[1];
    var state = message[2];

    var timestamp = Math.round((new Date()).getTime() / 1000);
    var dateString = new Date().toLocaleString();

    itemsTable.push(dateString, topic, payload);

    loadMessages();
    switch (area) {
        case 'kitchen':
            $('#kitchen').html('(Switch value: ' + payload + ')');
            if (payload == 'true') {
                $('#kitchen-value').text('Closed');
                $('#kitchen-value').removeClass('badge-danger').addClass('badge-success');
            } else {
                $('#kitchen-value').text('Open');
                $('#kitchen-value').removeClass('badge-success').addClass('badge-danger');
            }
            break;
        case 'front':
            $('#entrance').html('(Switch value: ' + payload + ')');
            if (payload == 'true') {
                $('#entrance-value').text('Closed');
                $('#entrance-value').removeClass('badge-danger').addClass('badge-success');
            } else {
                $('#entrance-value').text('Open');
                $('#entrance-value').removeClass('badge-success').addClass('badge-danger');
            }
            break;
        case 'back':
            $('#backdoor').html('(Switch value: ' + payload + ')');
            if (payload == 'true') {
                $('#backdoor-value').text('Closed');
                $('#backdoor-value').removeClass('badge-danger').addClass('badge-success');
            } else {
                $('#backdoor-value').text('Open');
                $('#backdoor-value').removeClass('badge-success').addClass('badge-danger');
            }
            break;
        case 'living':
            $('#living').html('(Sensor value: ' + payload + ')');
            $('#living-value').text(payload + '°C');
            $('#living-value').removeClass('').addClass('badge-default');


            labelslivingTempSensor.push(dateString);
            datalivingTempSensor.push(parseInt(payload));

            var livingTempSensorChart = new Chart(livingTempSensorCanva, {
                "type": "line",
                "data": { 
                    "labels": labelslivingTempSensor,
                    "datasets": [
                        { 
                        "label": "Living room temperature",
                        "data": datalivingTempSensor, 
                        "fill": false,
                        "borderColor": "rgb(75, 192, 192)",
                        "lineTension": 0.1 }
                        ]
                },
                "options": {}
            });




            break;
        case 'basement':
            $('#basement').html('(Sensor value: ' + payload + ')');
            if (payload >= 25) {
                $('#basement-value').text(payload + '°C - too hot');
                $('#basement-value').removeClass('badge-warning badge-success badge-info badge-primary').addClass('badge-danger');
            } else if (payload >= 21) {
                $('#basement-value').text(payload + '°C - hot');
                $('#basement-value').removeClass('badge-danger badge-success badge-info badge-primary').addClass('badge-warning');
            } else if (payload >= 18) {
                $('#basement-value').text(payload + '°C - normal');
                $('#basement-value').removeClass('badge-danger badge-warning badge-info badge-primary').addClass('badge-success');
            } else if (payload >= 15) {
                $('#basement-value').text(payload + '°C - low');
                $('#basement-value').removeClass('badge-danger badge-warning badge-success badge-primary').addClass('badge-info');
            } else if (mpayload <= 12) {
                $('#basement-value').text(payload + '°C - too low');
                $('#basement-value').removeClass('badge-danger badge-warning badge-success badge-info').addClass('badge-primary');

            }


            labelsbasementTempSensor.push(dateString);
            databasementTempSensor.push(parseInt(payload));

            var basementTempSensorChart = new Chart(basementTempSensorChartCanva, {
                "type": "line",
                "data": { 
                    "labels": labelsbasementTempSensor,
                    "datasets": [
                        { 
                        "label": "Basement room temperature",
                        "data": databasementTempSensor, 
                        "fill": false,
                        "borderColor": "rgb(75, 192, 192)",
                        "lineTension": 0.1 }
                        ]
                },
                "options": {}
            });
            break;
        default:
            console.log('Error: Data do not match the MQTT topic.');
            break;
    }
};
$(document).ready(function() {
    MQTTconnect();
});