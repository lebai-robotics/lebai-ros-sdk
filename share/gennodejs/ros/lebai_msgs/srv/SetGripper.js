// Auto-generated. Do not edit!

// (in-package lebai_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let ExecuteMode = require('../msg/ExecuteMode.js');

//-----------------------------------------------------------


//-----------------------------------------------------------

class SetGripperRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.val = null;
      this.execute_mode = null;
    }
    else {
      if (initObj.hasOwnProperty('val')) {
        this.val = initObj.val
      }
      else {
        this.val = 0.0;
      }
      if (initObj.hasOwnProperty('execute_mode')) {
        this.execute_mode = initObj.execute_mode
      }
      else {
        this.execute_mode = new ExecuteMode();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetGripperRequest
    // Serialize message field [val]
    bufferOffset = _serializer.float64(obj.val, buffer, bufferOffset);
    // Serialize message field [execute_mode]
    bufferOffset = ExecuteMode.serialize(obj.execute_mode, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetGripperRequest
    let len;
    let data = new SetGripperRequest(null);
    // Deserialize message field [val]
    data.val = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [execute_mode]
    data.execute_mode = ExecuteMode.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 9;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetGripperRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '55d855bd3cc6e73201d5b102ef34651b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 val
    lebai_msgs/ExecuteMode execute_mode
    
    ================================================================================
    MSG: lebai_msgs/ExecuteMode
    uint8 data
    uint8 EXECUTE_MODE_BUFFER=0
    uint8 EXECUTE_MODE_IMMED=1
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetGripperRequest(null);
    if (msg.val !== undefined) {
      resolved.val = msg.val;
    }
    else {
      resolved.val = 0.0
    }

    if (msg.execute_mode !== undefined) {
      resolved.execute_mode = ExecuteMode.Resolve(msg.execute_mode)
    }
    else {
      resolved.execute_mode = new ExecuteMode()
    }

    return resolved;
    }
};

class SetGripperResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.ret = null;
    }
    else {
      if (initObj.hasOwnProperty('ret')) {
        this.ret = initObj.ret
      }
      else {
        this.ret = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetGripperResponse
    // Serialize message field [ret]
    bufferOffset = _serializer.bool(obj.ret, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetGripperResponse
    let len;
    let data = new SetGripperResponse(null);
    // Deserialize message field [ret]
    data.ret = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetGripperResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e2cc9e9d8c464550830df49c160979ad';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool ret
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetGripperResponse(null);
    if (msg.ret !== undefined) {
      resolved.ret = msg.ret;
    }
    else {
      resolved.ret = false
    }

    return resolved;
    }
};

module.exports = {
  Request: SetGripperRequest,
  Response: SetGripperResponse,
  md5sum() { return '38cc51b5a105d56ff2e64d1889e45a66'; },
  datatype() { return 'lebai_msgs/SetGripper'; }
};
