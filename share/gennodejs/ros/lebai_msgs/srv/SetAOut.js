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

class SetAOutRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.group = null;
      this.index = null;
      this.value = null;
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
      if (initObj.hasOwnProperty('value')) {
        this.value = initObj.value
      }
      else {
        this.value = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetAOutRequest
    // Serialize message field [group]
    bufferOffset = _serializer.uint8(obj.group, buffer, bufferOffset);
    // Serialize message field [index]
    bufferOffset = _serializer.uint16(obj.index, buffer, bufferOffset);
    // Serialize message field [value]
    bufferOffset = _serializer.float64(obj.value, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetAOutRequest
    let len;
    let data = new SetAOutRequest(null);
    // Deserialize message field [group]
    data.group = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [index]
    data.index = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [value]
    data.value = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 11;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetAOutRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ea7eca226d31910fccddba8c483e4857';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 group
    uint16 index
    float64 value
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetAOutRequest(null);
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

    if (msg.value !== undefined) {
      resolved.value = msg.value;
    }
    else {
      resolved.value = 0.0
    }

    return resolved;
    }
};

class SetAOutResponse {
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
    // Serializes a message object of type SetAOutResponse
    // Serialize message field [code]
    bufferOffset = industrial_msgs.msg.ServiceReturnCode.serialize(obj.code, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetAOutResponse
    let len;
    let data = new SetAOutResponse(null);
    // Deserialize message field [code]
    data.code = industrial_msgs.msg.ServiceReturnCode.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/SetAOutResponse';
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
    const resolved = new SetAOutResponse(null);
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
  Request: SetAOutRequest,
  Response: SetAOutResponse,
  md5sum() { return '51928732046ffb5b5606f765ba7fcd8b'; },
  datatype() { return 'lebai_msgs/SetAOut'; }
};
