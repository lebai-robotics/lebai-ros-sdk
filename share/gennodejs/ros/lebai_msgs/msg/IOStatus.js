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

class IOStatus {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.robot_din = null;
      this.robot_dout = null;
      this.robot_ain = null;
      this.robot_aout = null;
      this.robot_ain_type = null;
      this.robot_aout_type = null;
      this.flange_din = null;
      this.flange_dout = null;
    }
    else {
      if (initObj.hasOwnProperty('robot_din')) {
        this.robot_din = initObj.robot_din
      }
      else {
        this.robot_din = [];
      }
      if (initObj.hasOwnProperty('robot_dout')) {
        this.robot_dout = initObj.robot_dout
      }
      else {
        this.robot_dout = [];
      }
      if (initObj.hasOwnProperty('robot_ain')) {
        this.robot_ain = initObj.robot_ain
      }
      else {
        this.robot_ain = [];
      }
      if (initObj.hasOwnProperty('robot_aout')) {
        this.robot_aout = initObj.robot_aout
      }
      else {
        this.robot_aout = [];
      }
      if (initObj.hasOwnProperty('robot_ain_type')) {
        this.robot_ain_type = initObj.robot_ain_type
      }
      else {
        this.robot_ain_type = [];
      }
      if (initObj.hasOwnProperty('robot_aout_type')) {
        this.robot_aout_type = initObj.robot_aout_type
      }
      else {
        this.robot_aout_type = [];
      }
      if (initObj.hasOwnProperty('flange_din')) {
        this.flange_din = initObj.flange_din
      }
      else {
        this.flange_din = [];
      }
      if (initObj.hasOwnProperty('flange_dout')) {
        this.flange_dout = initObj.flange_dout
      }
      else {
        this.flange_dout = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type IOStatus
    // Serialize message field [robot_din]
    bufferOffset = _arraySerializer.bool(obj.robot_din, buffer, bufferOffset, null);
    // Serialize message field [robot_dout]
    bufferOffset = _arraySerializer.bool(obj.robot_dout, buffer, bufferOffset, null);
    // Serialize message field [robot_ain]
    bufferOffset = _arraySerializer.float32(obj.robot_ain, buffer, bufferOffset, null);
    // Serialize message field [robot_aout]
    bufferOffset = _arraySerializer.float32(obj.robot_aout, buffer, bufferOffset, null);
    // Serialize message field [robot_ain_type]
    bufferOffset = _arraySerializer.uint8(obj.robot_ain_type, buffer, bufferOffset, null);
    // Serialize message field [robot_aout_type]
    bufferOffset = _arraySerializer.uint8(obj.robot_aout_type, buffer, bufferOffset, null);
    // Serialize message field [flange_din]
    bufferOffset = _arraySerializer.bool(obj.flange_din, buffer, bufferOffset, null);
    // Serialize message field [flange_dout]
    bufferOffset = _arraySerializer.bool(obj.flange_dout, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type IOStatus
    let len;
    let data = new IOStatus(null);
    // Deserialize message field [robot_din]
    data.robot_din = _arrayDeserializer.bool(buffer, bufferOffset, null)
    // Deserialize message field [robot_dout]
    data.robot_dout = _arrayDeserializer.bool(buffer, bufferOffset, null)
    // Deserialize message field [robot_ain]
    data.robot_ain = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [robot_aout]
    data.robot_aout = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [robot_ain_type]
    data.robot_ain_type = _arrayDeserializer.uint8(buffer, bufferOffset, null)
    // Deserialize message field [robot_aout_type]
    data.robot_aout_type = _arrayDeserializer.uint8(buffer, bufferOffset, null)
    // Deserialize message field [flange_din]
    data.flange_din = _arrayDeserializer.bool(buffer, bufferOffset, null)
    // Deserialize message field [flange_dout]
    data.flange_dout = _arrayDeserializer.bool(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.robot_din.length;
    length += object.robot_dout.length;
    length += 4 * object.robot_ain.length;
    length += 4 * object.robot_aout.length;
    length += object.robot_ain_type.length;
    length += object.robot_aout_type.length;
    length += object.flange_din.length;
    length += object.flange_dout.length;
    return length + 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'lebai_msgs/IOStatus';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '50c134754be339b506d0926e86b51aa1';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool[] robot_din
    bool[] robot_dout
    float32[] robot_ain
    float32[] robot_aout
    uint8[] robot_ain_type
    uint8[] robot_aout_type
    bool[] flange_din
    bool[] flange_dout
    
    uint8 VOLTAGETYPE=0
    uint8 CURRENTTYPE=1
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new IOStatus(null);
    if (msg.robot_din !== undefined) {
      resolved.robot_din = msg.robot_din;
    }
    else {
      resolved.robot_din = []
    }

    if (msg.robot_dout !== undefined) {
      resolved.robot_dout = msg.robot_dout;
    }
    else {
      resolved.robot_dout = []
    }

    if (msg.robot_ain !== undefined) {
      resolved.robot_ain = msg.robot_ain;
    }
    else {
      resolved.robot_ain = []
    }

    if (msg.robot_aout !== undefined) {
      resolved.robot_aout = msg.robot_aout;
    }
    else {
      resolved.robot_aout = []
    }

    if (msg.robot_ain_type !== undefined) {
      resolved.robot_ain_type = msg.robot_ain_type;
    }
    else {
      resolved.robot_ain_type = []
    }

    if (msg.robot_aout_type !== undefined) {
      resolved.robot_aout_type = msg.robot_aout_type;
    }
    else {
      resolved.robot_aout_type = []
    }

    if (msg.flange_din !== undefined) {
      resolved.flange_din = msg.flange_din;
    }
    else {
      resolved.flange_din = []
    }

    if (msg.flange_dout !== undefined) {
      resolved.flange_dout = msg.flange_dout;
    }
    else {
      resolved.flange_dout = []
    }

    return resolved;
    }
};

// Constants for message
IOStatus.Constants = {
  VOLTAGETYPE: 0,
  CURRENTTYPE: 1,
}

module.exports = IOStatus;
