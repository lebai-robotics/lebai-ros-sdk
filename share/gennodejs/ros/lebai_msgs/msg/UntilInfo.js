// Auto-generated. Do not edit!

// (in-package lebai_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let IOConditionalExpress = require('./IOConditionalExpress.js');

//-----------------------------------------------------------

class UntilInfo {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.io_express_logic = null;
      this.io_express = null;
    }
    else {
      if (initObj.hasOwnProperty('io_express_logic')) {
        this.io_express_logic = initObj.io_express_logic
      }
      else {
        this.io_express_logic = 0;
      }
      if (initObj.hasOwnProperty('io_express')) {
        this.io_express = initObj.io_express
      }
      else {
        this.io_express = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type UntilInfo
    // Serialize message field [io_express_logic]
    bufferOffset = _serializer.uint8(obj.io_express_logic, buffer, bufferOffset);
    // Serialize message field [io_express]
    // Serialize the length for message field [io_express]
    bufferOffset = _serializer.uint32(obj.io_express.length, buffer, bufferOffset);
    obj.io_express.forEach((val) => {
      bufferOffset = IOConditionalExpress.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type UntilInfo
    let len;
    let data = new UntilInfo(null);
    // Deserialize message field [io_express_logic]
    data.io_express_logic = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [io_express]
    // Deserialize array length for message field [io_express]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.io_express = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.io_express[i] = IOConditionalExpress.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 22 * object.io_express.length;
    return length + 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'lebai_msgs/UntilInfo';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0907ad90f772aaa5fd1b8f10a92d018a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 io_express_logic
    lebai_msgs/IOConditionalExpress[] io_express
    
    uint8 LOGIC_AND=0
    uint8 LOGIC_OR=1
    
    
    ================================================================================
    MSG: lebai_msgs/IOConditionalExpress
    uint32 group
    uint32 pin
    uint32 type
    float64 float_value
    uint8 uint_value
    uint8 logic_operation
    
    uint8 GROUP_ROBOT=0
    uint8 GROUP_FLANGE=1
    
    uint8 TYPE_ANALOG=0
    uint8 TYPE_DIGITAL=1
    
    # great >
    uint8 LOGIC_OP_GT=0
    # great and equal >=
    uint8 LOGIC_OP_GE=1
    # equal
    uint8 LOGIC_OP_EQ=2
    # not equal
    uint8 LOGIC_OP_NE=3
    # less than
    uint8 LOGIC_OP_LT=4
    # less than and equal
    uint8 LOGIC_OP_LE=5
    
    
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new UntilInfo(null);
    if (msg.io_express_logic !== undefined) {
      resolved.io_express_logic = msg.io_express_logic;
    }
    else {
      resolved.io_express_logic = 0
    }

    if (msg.io_express !== undefined) {
      resolved.io_express = new Array(msg.io_express.length);
      for (let i = 0; i < resolved.io_express.length; ++i) {
        resolved.io_express[i] = IOConditionalExpress.Resolve(msg.io_express[i]);
      }
    }
    else {
      resolved.io_express = []
    }

    return resolved;
    }
};

// Constants for message
UntilInfo.Constants = {
  LOGIC_AND: 0,
  LOGIC_OR: 1,
}

module.exports = UntilInfo;
