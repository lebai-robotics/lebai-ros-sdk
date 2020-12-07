// Auto-generated. Do not edit!

// (in-package lebai_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let UntilInfo = require('./UntilInfo.js');

//-----------------------------------------------------------

class MoveCommon {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.vel = null;
      this.acc = null;
      this.time = null;
      this.is_continous_mode = null;
      this.continuation_type = null;
      this.until = null;
      this.until_info = null;
    }
    else {
      if (initObj.hasOwnProperty('vel')) {
        this.vel = initObj.vel
      }
      else {
        this.vel = 0.0;
      }
      if (initObj.hasOwnProperty('acc')) {
        this.acc = initObj.acc
      }
      else {
        this.acc = 0.0;
      }
      if (initObj.hasOwnProperty('time')) {
        this.time = initObj.time
      }
      else {
        this.time = 0.0;
      }
      if (initObj.hasOwnProperty('is_continous_mode')) {
        this.is_continous_mode = initObj.is_continous_mode
      }
      else {
        this.is_continous_mode = false;
      }
      if (initObj.hasOwnProperty('continuation_type')) {
        this.continuation_type = initObj.continuation_type
      }
      else {
        this.continuation_type = 0;
      }
      if (initObj.hasOwnProperty('until')) {
        this.until = initObj.until
      }
      else {
        this.until = false;
      }
      if (initObj.hasOwnProperty('until_info')) {
        this.until_info = initObj.until_info
      }
      else {
        this.until_info = new UntilInfo();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MoveCommon
    // Serialize message field [vel]
    bufferOffset = _serializer.float64(obj.vel, buffer, bufferOffset);
    // Serialize message field [acc]
    bufferOffset = _serializer.float64(obj.acc, buffer, bufferOffset);
    // Serialize message field [time]
    bufferOffset = _serializer.float64(obj.time, buffer, bufferOffset);
    // Serialize message field [is_continous_mode]
    bufferOffset = _serializer.bool(obj.is_continous_mode, buffer, bufferOffset);
    // Serialize message field [continuation_type]
    bufferOffset = _serializer.uint8(obj.continuation_type, buffer, bufferOffset);
    // Serialize message field [until]
    bufferOffset = _serializer.bool(obj.until, buffer, bufferOffset);
    // Serialize message field [until_info]
    bufferOffset = UntilInfo.serialize(obj.until_info, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MoveCommon
    let len;
    let data = new MoveCommon(null);
    // Deserialize message field [vel]
    data.vel = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [acc]
    data.acc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [time]
    data.time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [is_continous_mode]
    data.is_continous_mode = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [continuation_type]
    data.continuation_type = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [until]
    data.until = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [until_info]
    data.until_info = UntilInfo.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += UntilInfo.getMessageSize(object.until_info);
    return length + 27;
  }

  static datatype() {
    // Returns string type for a message object
    return 'lebai_msgs/MoveCommon';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4ddffee09af26b88275ddf204fecc8d2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 vel
    float64 acc
    float64 time
    bool is_continous_mode
    # 0: normal move, 1: smooth move
    uint8 continuation_type
    # until data
    bool until
    lebai_msgs/UntilInfo until_info
    ================================================================================
    MSG: lebai_msgs/UntilInfo
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
    const resolved = new MoveCommon(null);
    if (msg.vel !== undefined) {
      resolved.vel = msg.vel;
    }
    else {
      resolved.vel = 0.0
    }

    if (msg.acc !== undefined) {
      resolved.acc = msg.acc;
    }
    else {
      resolved.acc = 0.0
    }

    if (msg.time !== undefined) {
      resolved.time = msg.time;
    }
    else {
      resolved.time = 0.0
    }

    if (msg.is_continous_mode !== undefined) {
      resolved.is_continous_mode = msg.is_continous_mode;
    }
    else {
      resolved.is_continous_mode = false
    }

    if (msg.continuation_type !== undefined) {
      resolved.continuation_type = msg.continuation_type;
    }
    else {
      resolved.continuation_type = 0
    }

    if (msg.until !== undefined) {
      resolved.until = msg.until;
    }
    else {
      resolved.until = false
    }

    if (msg.until_info !== undefined) {
      resolved.until_info = UntilInfo.Resolve(msg.until_info)
    }
    else {
      resolved.until_info = new UntilInfo()
    }

    return resolved;
    }
};

module.exports = MoveCommon;
