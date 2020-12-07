// Auto-generated. Do not edit!

// (in-package lebai_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class IOConditionalExpress {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.group = null;
      this.pin = null;
      this.type = null;
      this.float_value = null;
      this.uint_value = null;
      this.logic_operation = null;
    }
    else {
      if (initObj.hasOwnProperty('group')) {
        this.group = initObj.group
      }
      else {
        this.group = 0;
      }
      if (initObj.hasOwnProperty('pin')) {
        this.pin = initObj.pin
      }
      else {
        this.pin = 0;
      }
      if (initObj.hasOwnProperty('type')) {
        this.type = initObj.type
      }
      else {
        this.type = 0;
      }
      if (initObj.hasOwnProperty('float_value')) {
        this.float_value = initObj.float_value
      }
      else {
        this.float_value = 0.0;
      }
      if (initObj.hasOwnProperty('uint_value')) {
        this.uint_value = initObj.uint_value
      }
      else {
        this.uint_value = 0;
      }
      if (initObj.hasOwnProperty('logic_operation')) {
        this.logic_operation = initObj.logic_operation
      }
      else {
        this.logic_operation = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type IOConditionalExpress
    // Serialize message field [group]
    bufferOffset = _serializer.uint32(obj.group, buffer, bufferOffset);
    // Serialize message field [pin]
    bufferOffset = _serializer.uint32(obj.pin, buffer, bufferOffset);
    // Serialize message field [type]
    bufferOffset = _serializer.uint32(obj.type, buffer, bufferOffset);
    // Serialize message field [float_value]
    bufferOffset = _serializer.float64(obj.float_value, buffer, bufferOffset);
    // Serialize message field [uint_value]
    bufferOffset = _serializer.uint8(obj.uint_value, buffer, bufferOffset);
    // Serialize message field [logic_operation]
    bufferOffset = _serializer.uint8(obj.logic_operation, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type IOConditionalExpress
    let len;
    let data = new IOConditionalExpress(null);
    // Deserialize message field [group]
    data.group = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [pin]
    data.pin = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [type]
    data.type = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [float_value]
    data.float_value = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [uint_value]
    data.uint_value = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [logic_operation]
    data.logic_operation = _deserializer.uint8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 22;
  }

  static datatype() {
    // Returns string type for a message object
    return 'lebai_msgs/IOConditionalExpress';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '35d2fc6b432f8da8c61c0faaba79afff';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    const resolved = new IOConditionalExpress(null);
    if (msg.group !== undefined) {
      resolved.group = msg.group;
    }
    else {
      resolved.group = 0
    }

    if (msg.pin !== undefined) {
      resolved.pin = msg.pin;
    }
    else {
      resolved.pin = 0
    }

    if (msg.type !== undefined) {
      resolved.type = msg.type;
    }
    else {
      resolved.type = 0
    }

    if (msg.float_value !== undefined) {
      resolved.float_value = msg.float_value;
    }
    else {
      resolved.float_value = 0.0
    }

    if (msg.uint_value !== undefined) {
      resolved.uint_value = msg.uint_value;
    }
    else {
      resolved.uint_value = 0
    }

    if (msg.logic_operation !== undefined) {
      resolved.logic_operation = msg.logic_operation;
    }
    else {
      resolved.logic_operation = 0
    }

    return resolved;
    }
};

// Constants for message
IOConditionalExpress.Constants = {
  GROUP_ROBOT: 0,
  GROUP_FLANGE: 1,
  TYPE_ANALOG: 0,
  TYPE_DIGITAL: 1,
  LOGIC_OP_GT: 0,
  LOGIC_OP_GE: 1,
  LOGIC_OP_EQ: 2,
  LOGIC_OP_NE: 3,
  LOGIC_OP_LT: 4,
  LOGIC_OP_LE: 5,
}

module.exports = IOConditionalExpress;
