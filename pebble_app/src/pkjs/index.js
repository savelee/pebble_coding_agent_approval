// Copyright 2026 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview PebbleKit JS application for Pebble Agent Approvals & Target App Selection.
 */

var messageKeys;
try {
  messageKeys = require('message_keys');
} catch (e) {
  messageKeys = {
    ACTION: 0,
    STATUS: 1,
    HOST: 2,
    PORT: 3,
    PROMPT_TEXT: 4,
  };
}

var DEFAULT_HOST = '127.0.0.1';
var DEFAULT_PORT = '5000';
var DEFAULT_TARGET_APP = 'active';

function getServerConfig() {
  var host = localStorage.getItem('HOST') || DEFAULT_HOST;
  var port = localStorage.getItem('PORT') || DEFAULT_PORT;
  var targetApp = localStorage.getItem('TARGET_APP') || DEFAULT_TARGET_APP;
  return { host: host, port: port, targetApp: targetApp };
}

function sendStatusToWatch(statusMsg) {
  var statusKey = (messageKeys && typeof messageKeys.STATUS !== 'undefined')
    ? messageKeys.STATUS
    : 1;
  var dict = {};
  dict[statusKey] = statusMsg;
  dict[1] = statusMsg;
  dict[10001] = statusMsg;

  Pebble.sendAppMessage(
    dict,
    function() {
      console.log('Successfully sent status to watch: ' + statusMsg);
    },
    function(e) {
      console.error('Failed to send status to watch: ' + JSON.stringify(e));
    }
  );
}

function sendPromptToWatch(promptText) {
  var promptKey = (messageKeys && typeof messageKeys.PROMPT_TEXT !== 'undefined')
    ? messageKeys.PROMPT_TEXT
    : 4;
  var dict = {};
  dict[promptKey] = promptText;
  dict[4] = promptText;
  dict[10004] = promptText;

  console.log('Pushing prompt to watch with payload: ' + JSON.stringify(dict));

  Pebble.sendAppMessage(
    dict,
    function() {
      console.log('Successfully pushed prompt to watch: ' + promptText);
    },
    function(e) {
      console.error('Failed to push prompt to watch: ' + JSON.stringify(e));
    }
  );
}

function postActionToListener(action) {
  var config = getServerConfig();
  var url = 'http://' + config.host + ':' + config.port + '/api/action';
  console.log('Sending action: ' + action + ' to ' + url + ' (target_app: ' + config.targetApp + ')');

  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.timeout = 5000;

  xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
      console.log('Server response: ' + xhr.responseText);
      sendStatusToWatch('SENT OK');
    } else {
      console.error('Server returned error status: ' + xhr.status);
      sendStatusToWatch('HTTP ' + xhr.status);
    }
  };

  xhr.onerror = function() {
    console.error('Network request failed for ' + url);
    sendStatusToWatch('NET ERROR');
  };

  xhr.ontimeout = function() {
    console.error('Request timed out for ' + url);
    sendStatusToWatch('TIMEOUT');
  };

  var payload = {
    action: action,
    target_app: config.targetApp
  };
  xhr.send(JSON.stringify(payload));
}

// Background Notification Poller (Pulls from /api/notifications every 2.5 seconds)
function pollNotifications() {
  var config = getServerConfig();
  var url = 'http://' + config.host + ':' + config.port + '/api/notifications';

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.timeout = 2000;

  xhr.onload = function() {
    if (xhr.status === 200) {
      try {
        var data = JSON.parse(xhr.responseText);
        if (data.notifications && data.notifications.length > 0) {
          for (var i = 0; i < data.notifications.length; i++) {
            var n = data.notifications[i];
            var msg = n.body || n.message || n.title;
            if (msg) {
              console.log('Fetched notification from listener: ' + msg);
              sendPromptToWatch(msg);
            }
          }
        }
      } catch (err) {
        console.error('Failed to parse notifications: ' + err);
      }
    }
  };

  xhr.send();
}

var pollInterval = null;
Pebble.addEventListener('ready', function() {
  console.log('PebbleKit JS ready for Agent Approvals & Notifications.');
  if (!pollInterval) {
    // Initial poll and recurring poll
    pollNotifications();
    pollInterval = setInterval(pollNotifications, 2500);
  }
});

Pebble.addEventListener('appmessage', function(e) {
  var dict = e.payload;
  console.log('Received AppMessage from watch: ' + JSON.stringify(dict));

  var actionKey = (messageKeys && typeof messageKeys.ACTION !== 'undefined')
    ? messageKeys.ACTION
    : 0;

  var actionVal = typeof dict[actionKey] !== 'undefined'
    ? dict[actionKey]
    : (typeof dict[0] !== 'undefined' ? dict[0] : (typeof dict[10000] !== 'undefined' ? dict[10000] : dict.ACTION));

  if (typeof actionVal !== 'undefined') {
    var actionStr = (actionVal === 0 || actionVal === '0') ? 'confirm' : 'disapprove';
    postActionToListener(actionStr);
  }
});

function generateConfigHtml() {
  var config = getServerConfig();
  var html = '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<style>' +
    'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; color: #333; }' +
    '.card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); max-width: 400px; margin: auto; }' +
    'h2 { margin-top: 0; color: #1a73e8; font-size: 20px; }' +
    'p.sub { font-size: 13px; color: #444; line-height: 1.4; margin-top: 6px; margin-bottom: 18px; }' +
    'label { font-size: 13px; font-weight: 600; color: #555; display: block; margin-top: 15px; margin-bottom: 5px; }' +
    'input, select { width: 100%; box-sizing: border-box; padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; font-family: sans-serif; background: white; }' +
    'input { font-family: monospace; }' +
    'button { width: 100%; margin-top: 25px; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }' +
    'button:active { background: #1557b0; }' +
    '</style></head><body>' +
    '<div class="card">' +
    '<h2>Agent Approvals Settings</h2>' +
    '<p class="sub">Approve your coding agent (Antigravity, Claude Code, Cursor) from your wrist with physical buttons.</p>' +
    '<form id="settings-form">' +
    '<label>Target Coding Agent / Window</label>' +
    '<select id="target_app">' +
    '  <option value="active"' + (config.targetApp === 'active' ? ' selected' : '') + '>Active Window (No Switch / Default)</option>' +
    '  <option value="Antigravity"' + (config.targetApp === 'Antigravity' ? ' selected' : '') + '>Antigravity IDE</option>' +
    '  <option value="Cursor"' + (config.targetApp === 'Cursor' ? ' selected' : '') + '>Cursor</option>' +
    '  <option value="Terminal"' + (config.targetApp === 'Terminal' ? ' selected' : '') + '>Terminal / iTerm2 (Claude Code)</option>' +
    '  <option value="Code"' + (config.targetApp === 'Code' ? ' selected' : '') + '>Visual Studio Code</option>' +
    '</select>' +
    '<label>Listener Host / IP Address</label>' +
    '<input type="text" id="host" value="' + config.host + '" placeholder="127.0.0.1 (emulator) or LAN IP" required>' +
    '<label>Port</label>' +
    '<input type="number" id="port" value="' + config.port + '" placeholder="5000" required>' +
    '<button type="submit">Save & Close</button>' +
    '</form></div>' +
    '<script>' +
    'document.getElementById("settings-form").addEventListener("submit", function(e) {' +
    '  e.preventDefault();' +
    '  var hostVal = document.getElementById("host").value.trim();' +
    '  var portVal = document.getElementById("port").value.trim();' +
    '  var targetAppVal = document.getElementById("target_app").value;' +
    '  var options = { host: hostVal, port: portVal, target_app: targetAppVal };' +
    '  var locationUri = "pebblejs://close#" + encodeURIComponent(JSON.stringify(options));' +
    '  window.location.href = locationUri;' +
    '});' +
    '</script></body></html>';
  return 'data:text/html;charset=utf-8,' + encodeURIComponent(html);
}

Pebble.addEventListener('showConfiguration', function() {
  var url = generateConfigHtml();
  Pebble.openURL(url);
});

Pebble.addEventListener('webviewclosed', function(e) {
  if (e && e.response) {
    try {
      var options = JSON.parse(decodeURIComponent(e.response));
      if (options.host) {
        localStorage.setItem('HOST', options.host);
      }
      if (options.port) {
        localStorage.setItem('PORT', options.port);
      }
      if (options.target_app) {
        localStorage.setItem('TARGET_APP', options.target_app);
      }
      console.log('Saved settings: Host=' + options.host + ', Port=' + options.port + ', Target=' + options.target_app);
      sendStatusToWatch('CFG SAVED');
    } catch (err) {
      console.error('Failed to parse config response: ' + err);
    }
  }
});
