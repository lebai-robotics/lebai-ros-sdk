;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::MoveCommon)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'MoveCommon (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::MOVECOMMON")
  (make-package "LEBAI_MSGS::MOVECOMMON"))

(in-package "ROS")
;;//! \htmlinclude MoveCommon.msg.html


(defclass lebai_msgs::MoveCommon
  :super ros::object
  :slots (_vel _acc _time _is_continous_mode _continuation_type _until _until_info ))

(defmethod lebai_msgs::MoveCommon
  (:init
   (&key
    ((:vel __vel) 0.0)
    ((:acc __acc) 0.0)
    ((:time __time) 0.0)
    ((:is_continous_mode __is_continous_mode) nil)
    ((:continuation_type __continuation_type) 0)
    ((:until __until) nil)
    ((:until_info __until_info) (instance lebai_msgs::UntilInfo :init))
    )
   (send-super :init)
   (setq _vel (float __vel))
   (setq _acc (float __acc))
   (setq _time (float __time))
   (setq _is_continous_mode __is_continous_mode)
   (setq _continuation_type (round __continuation_type))
   (setq _until __until)
   (setq _until_info __until_info)
   self)
  (:vel
   (&optional __vel)
   (if __vel (setq _vel __vel)) _vel)
  (:acc
   (&optional __acc)
   (if __acc (setq _acc __acc)) _acc)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:is_continous_mode
   (&optional __is_continous_mode)
   (if __is_continous_mode (setq _is_continous_mode __is_continous_mode)) _is_continous_mode)
  (:continuation_type
   (&optional __continuation_type)
   (if __continuation_type (setq _continuation_type __continuation_type)) _continuation_type)
  (:until
   (&optional __until)
   (if __until (setq _until __until)) _until)
  (:until_info
   (&rest __until_info)
   (if (keywordp (car __until_info))
       (send* _until_info __until_info)
     (progn
       (if __until_info (setq _until_info (car __until_info)))
       _until_info)))
  (:serialization-length
   ()
   (+
    ;; float64 _vel
    8
    ;; float64 _acc
    8
    ;; float64 _time
    8
    ;; bool _is_continous_mode
    1
    ;; uint8 _continuation_type
    1
    ;; bool _until
    1
    ;; lebai_msgs/UntilInfo _until_info
    (send _until_info :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _vel
       (sys::poke _vel (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _acc
       (sys::poke _acc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _time
       (sys::poke _time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; bool _is_continous_mode
       (if _is_continous_mode (write-byte -1 s) (write-byte 0 s))
     ;; uint8 _continuation_type
       (write-byte _continuation_type s)
     ;; bool _until
       (if _until (write-byte -1 s) (write-byte 0 s))
     ;; lebai_msgs/UntilInfo _until_info
       (send _until_info :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _vel
     (setq _vel (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _acc
     (setq _acc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _time
     (setq _time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; bool _is_continous_mode
     (setq _is_continous_mode (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; uint8 _continuation_type
     (setq _continuation_type (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; bool _until
     (setq _until (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; lebai_msgs/UntilInfo _until_info
     (send _until_info :deserialize buf ptr-) (incf ptr- (send _until_info :serialization-length))
   ;;
   self)
  )

(setf (get lebai_msgs::MoveCommon :md5sum-) "4ddffee09af26b88275ddf204fecc8d2")
(setf (get lebai_msgs::MoveCommon :datatype-) "lebai_msgs/MoveCommon")
(setf (get lebai_msgs::MoveCommon :definition-)
      "float64 vel
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




")



(provide :lebai_msgs/MoveCommon "4ddffee09af26b88275ddf204fecc8d2")


