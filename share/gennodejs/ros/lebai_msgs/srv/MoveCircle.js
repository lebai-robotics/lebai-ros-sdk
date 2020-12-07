// Auto-generated. Do not edit!

// (in-package lebai_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let MoveCommon = require('../msg/MoveCommon.js');
let ExecuteMode = require('../msg/ExecuteMode.js');
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------


//-----------------------------------------------------------

class MoveCircleRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.way_point_is_joint_pose = null;
      this.way_point_joint_pose = null;
      this.way_point_cartesian_pose = null;
      this.end_point_is_joint_pose = null;
      this.end_point_joint_pose = null;
      this.end_point_cartesian_pose = null;
      this.circle_angle = null;
      this.common = null;
      this.execute_mode = null;
    }
    else {
      if (initObj.hasOwnProperty('way_point_is_joint_pose')) {
        this.way_point_is_joint_pose = initObj.way_point_is_joint_pose
      }
      else {
        this.way_point_is_joint_pose = false;
      }
      if (initObj.hasOwnProperty('way_point_joint_pose')) {
        this.way_point_joint_pose = initObj.way_point_joint_pose
      }
      else {
        this.way_point_joint_pose = [];
      }
      if (initObj.hasOwnProperty('way_point_cartesian_pose')) {
        this.way_point_cartesian_pose = initObj.way_point_cartesian_pose
      }
      else {
        this.way_point_cartesian_pose = new geometry_msgs.msg.Pose();
      }
      if (initObj.hasOwnProperty('end_point_is_joint_pose')) {
        this.end_point_is_joint_pose = initObj.end_point_is_joint_pose
      }
      else {
        this.end_point_is_joint_pose = false;
      }
      if (initObj.hasOwnProperty('end_point_joint_pose')) {
        this.end_point_joint_pose = initObj.end_point_joint_pose
      }
      else {
        this.end_point_joint_pose = [];
      }
      if (initObj.hasOwnProperty('end_point_cartesian_pose')) {
        this.end_point_cartesian_pose = initObj.end_point_cartesian_pose
      }
      else {
        this.end_point_cartesian_pose = new geometry_msgs.msg.Pose();
      }
      if (initObj.hasOwnProperty('circle_angle')) {
        this.circle_angle = initObj.circle_angle
      }
      else {
        this.circle_angle = 0.0;
      }
      if (initObj.hasOwnProperty('common')) {
        this.common = initObj.common
      }
      else {
        this.common = new MoveCommon();
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
    // Serializes a message object of type MoveCircleRequest
    // Serialize message field [way_point_is_joint_pose]
    bufferOffset = _serializer.bool(obj.way_point_is_joint_pose, buffer, bufferOffset);
    // Serialize message field [way_point_joint_pose]
    bufferOffset = _arraySerializer.float64(obj.way_point_joint_pose, buffer, bufferOffset, null);
    // Serialize message field [way_point_cartesian_pose]
    bufferOffset = geometry_msgs.msg.Pose.serialize(obj.way_point_cartesian_pose, buffer, bufferOffset);
    // Serialize message field [end_point_is_joint_pose]
    bufferOffset = _serializer.bool(obj.end_point_is_joint_pose, buffer, bufferOffset);
    // Serialize message field [end_point_joint_pose]
    bufferOffset = _arraySerializer.float64(obj.end_point_joint_pose, buffer, bufferOffset, null);
    // Serialize message field [end_point_cartesian_pose]
    bufferOffset = geometry_msgs.msg.Pose.serialize(obj.end_point_cartesian_pose, buffer, bufferOffset);
    // Serialize message field [circle_angle]
    bufferOffset = _serializer.float64(obj.circle_angle, buffer, bufferOffset);
    // Serialize message field [common]
    bufferOffset = MoveCommon.serialize(obj.common, buffer, bufferOffset);
    // Serialize message field [execute_mode]
    bufferOffset = ExecuteMode.serialize(obj.execute_mode, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MoveCircleRequest
    let len;
    let data = new MoveCircleRequest(null);
    // Deserialize message field [way_point_is_joint_pose]
    data.way_point_is_joint_pose = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [way_point_joint_pose]
    data.way_point_joint_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [way_point_cartesian_pose]
    data.way_point_cartesian_pose = geometry_msgs.msg.Pose.deserialize(buffer, bufferOffset);
    // Deserialize message field [end_point_is_joint_pose]
    data.end_point_is_joint_pose = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [end_point_joint_pose]
    data.end_point_joint_pose = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [end_point_cartesian_pose]
    data.end_point_cartesian_pose = geometry_msgs.msg.Pose.deserialize(buffer, bufferOffset);
    // Deserialize message field [circle_angle]
    data.circle_angle = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [common]
    data.common = MoveCommon.deserialize(buffer, bufferOffset);
    // Deserialize message field [execute_mode]
    data.execute_mode = ExecuteMode.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.way_point_joint_pose.length;
    length += 8 * object.end_point_joint_pose.length;
    length += MoveCommon.getMessageSize(object.common);
    return length + 131;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/MoveCircleRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '26e0f80d402217d95277f55cf77dc8cb';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool way_point_is_joint_pose
    float64[] way_point_joint_pose
    geometry_msgs/Pose way_point_cartesian_pose
    bool end_point_is_joint_pose
    float64[] end_point_joint_pose
    geometry_msgs/Pose end_point_cartesian_pose
    float64 circle_angle
    lebai_msgs/MoveCommon common
    lebai_msgs/ExecuteMode execute_mode
    
    ================================================================================
    MSG: geometry_msgs/Pose
    # A representation of pose in free space, composed of position and orientation. 
    Point position
    Quaternion orientation
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    ================================================================================
    MSG: lebai_msgs/MoveCommon
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
    const resolved = new MoveCircleRequest(null);
    if (msg.way_point_is_joint_pose !== undefined) {
      resolved.way_point_is_joint_pose = msg.way_point_is_joint_pose;
    }
    else {
      resolved.way_point_is_joint_pose = false
    }

    if (msg.way_point_joint_pose !== undefined) {
      resolved.way_point_joint_pose = msg.way_point_joint_pose;
    }
    else {
      resolved.way_point_joint_pose = []
    }

    if (msg.way_point_cartesian_pose !== undefined) {
      resolved.way_point_cartesian_pose = geometry_msgs.msg.Pose.Resolve(msg.way_point_cartesian_pose)
    }
    else {
      resolved.way_point_cartesian_pose = new geometry_msgs.msg.Pose()
    }

    if (msg.end_point_is_joint_pose !== undefined) {
      resolved.end_point_is_joint_pose = msg.end_point_is_joint_pose;
    }
    else {
      resolved.end_point_is_joint_pose = false
    }

    if (msg.end_point_joint_pose !== undefined) {
      resolved.end_point_joint_pose = msg.end_point_joint_pose;
    }
    else {
      resolved.end_point_joint_pose = []
    }

    if (msg.end_point_cartesian_pose !== undefined) {
      resolved.end_point_cartesian_pose = geometry_msgs.msg.Pose.Resolve(msg.end_point_cartesian_pose)
    }
    else {
      resolved.end_point_cartesian_pose = new geometry_msgs.msg.Pose()
    }

    if (msg.circle_angle !== undefined) {
      resolved.circle_angle = msg.circle_angle;
    }
    else {
      resolved.circle_angle = 0.0
    }

    if (msg.common !== undefined) {
      resolved.common = MoveCommon.Resolve(msg.common)
    }
    else {
      resolved.common = new MoveCommon()
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

class MoveCircleResponse {
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
    // Serializes a message object of type MoveCircleResponse
    // Serialize message field [ret]
    bufferOffset = _serializer.bool(obj.ret, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MoveCircleResponse
    let len;
    let data = new MoveCircleResponse(null);
    // Deserialize message field [ret]
    data.ret = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'lebai_msgs/MoveCircleResponse';
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
    const resolved = new MoveCircleResponse(null);
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
  Request: MoveCircleRequest,
  Response: MoveCircleResponse,
  md5sum() { return '76aefbda84057bd81221aca855230727'; },
  datatype() { return 'lebai_msgs/MoveCircle'; }
};
