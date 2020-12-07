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

let industrial_msgs = _finder('industrial_msgs');

//-----------------------------------------------------------

class SetDORequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.pin = null;
      this.value = null;
      this.execute_mode = null;
    }
    else {
      if (initObj.hasOwnProperty('pin')) {
        this.pin = initObj.pin
      }
      else {
        this.pin = 0;
      }
      if (initObj.hasOwnProperty('value')) {
        this.value = initObj.value
      }
      else {
        this.value = false;
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
    // Serializes a message object of type SetDORequest
    // Serialize message field [pin]
    bufferOffset = _serializer.uint16(obj.pin, buffer, bufferOffset);
    // Serialize message field [value]
    bufferOffset = _serializer.bool(obj.value, buffer, bufferOffset);
    // Serialize message field [execute_mode]
    bufferOffset = ExecuteMode.serialize(obj.execute_mode, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetDORequest
    let len;
    let data = new SetDORequest(null);
    // Deserialize message field [pin]
    data.pin = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [value]
    data.value = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [execute_mode]
    data.execute_mode = ExecuteMode.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetDORequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '34d10c89d89e1253d8901caa256a4b06';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint16 pin
    bool value
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
    const resolved = new SetDORequest(null);
    if (msg.pin !== undefined) {
      resolved.pin = msg.pin;
    }
    else {
      resolved.pin = 0
    }

    if (msg.value !== undefined) {
      resolved.value = msg.value;
    }
    else {
      resolved.value = false
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

class SetDOResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.code = null;
    }
    else {
      if (initObj.hasOwnProperty('code')) {
        this.code = initObj.code
      }
      else {
        this.code = new industrial_msgs.msg.ServiceReturnCode();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetDOResponse
    // Serialize message field [code]
    bufferOffset = industrial_msgs.msg.ServiceReturnCode.serialize(obj.code, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetDOResponse
    let len;
    let data = new SetDOResponse(null);
    // Deserialize message field [code]
    data.code = industrial_msgs.msg.ServiceReturnCode.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetDOResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '50b1f38f75f5677e5692f3b3e7e1ea48';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    industrial_msgs/ServiceReturnCode code
    
    ================================================================================
    MSG: industrial_msgs/ServiceReturnCode
    # Service return codes for simple requests.  All ROS-Industrial service
    # replies are required to have a return code indicating success or failure
    # Specific return codes for different failure should be negative.
    int8 val
    
    int8 SUCCESS = 1
    int8 FAILURE = -1
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetDOResponse(null);
    if (msg.code !== undefined) {
      resolved.code = industrial_msgs.msg.ServiceReturnCode.Resolve(msg.code)
    }
    else {
      resolved.code = new industrial_msgs.msg.ServiceReturnCode()
    }

    return resolved;
    }
};

module.exports = {
  Request: SetDORequest,
  Response: SetDOResponse,
  md5sum() { return '5a536dfb6aaff1ccac47c5a754efe2e6'; },
  datatype() { return 'lebai_msgs/SetDO'; }
};
