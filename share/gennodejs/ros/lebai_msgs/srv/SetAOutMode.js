// Auto-generated. Do not edit!

// (in-package lebai_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

let industrial_msgs = _finder('industrial_msgs');

//-----------------------------------------------------------

class SetAOutModeRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.group = null;
      this.index = null;
      this.mode = null;
    }
    else {
      if (initObj.hasOwnProperty('group')) {
        this.group = initObj.group
      }
      else {
        this.group = 0;
      }
      if (initObj.hasOwnProperty('index')) {
        this.index = initObj.index
      }
      else {
        this.index = 0;
      }
      if (initObj.hasOwnProperty('mode')) {
        this.mode = initObj.mode
      }
      else {
        this.mode = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetAOutModeRequest
    // Serialize message field [group]
    bufferOffset = _serializer.uint8(obj.group, buffer, bufferOffset);
    // Serialize message field [index]
    bufferOffset = _serializer.uint16(obj.index, buffer, bufferOffset);
    // Serialize message field [mode]
    bufferOffset = _serializer.uint8(obj.mode, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetAOutModeRequest
    let len;
    let data = new SetAOutModeRequest(null);
    // Deserialize message field [group]
    data.group = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [index]
    data.index = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [mode]
    data.mode = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetAOutModeRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4af607cdbbd245f2058b461b68608500';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 group
    uint16 index
    uint8 mode
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetAOutModeRequest(null);
    if (msg.group !== undefined) {
      resolved.group = msg.group;
    }
    else {
      resolved.group = 0
    }

    if (msg.index !== undefined) {
      resolved.index = msg.index;
    }
    else {
      resolved.index = 0
    }

    if (msg.mode !== undefined) {
      resolved.mode = msg.mode;
    }
    else {
      resolved.mode = 0
    }

    return resolved;
    }
};

class SetAOutModeResponse {
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
    // Serializes a message object of type SetAOutModeResponse
    // Serialize message field [code]
    bufferOffset = industrial_msgs.msg.ServiceReturnCode.serialize(obj.code, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetAOutModeResponse
    let len;
    let data = new SetAOutModeResponse(null);
    // Deserialize message field [code]
    data.code = industrial_msgs.msg.ServiceReturnCode.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetAOutModeResponse';
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
    const resolved = new SetAOutModeResponse(null);
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
  Request: SetAOutModeRequest,
  Response: SetAOutModeResponse,
  md5sum() { return 'faf7ab1e93a1650eb66028ad6d75331c'; },
  datatype() { return 'lebai_msgs/SetAOutMode'; }
};
