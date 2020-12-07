;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::UntilInfo)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'UntilInfo (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::UNTILINFO")
  (make-package "LEBAI_MSGS::UNTILINFO"))

(in-package "ROS")
;;//! \htmlinclude UntilInfo.msg.html


(intern "*LOGIC_AND*" (find-package "LEBAI_MSGS::UNTILINFO"))
(shadow '*LOGIC_AND* (find-package "LEBAI_MSGS::UNTILINFO"))
(defconstant lebai_msgs::UntilInfo::*LOGIC_AND* 0)
(intern "*LOGIC_OR*" (find-package "LEBAI_MSGS::UNTILINFO"))
(shadow '*LOGIC_OR* (find-package "LEBAI_MSGS::UNTILINFO"))
(defconstant lebai_msgs::UntilInfo::*LOGIC_OR* 1)
(defclass lebai_msgs::UntilInfo
  :super ros::object
  :slots (_io_express_logic _io_express ))

(defmethod lebai_msgs::UntilInfo
  (:init
   (&key
    ((:io_express_logic __io_express_logic) 0)
    ((:io_express __io_express) (let (r) (dotimes (i 0) (push (instance lebai_msgs::IOConditionalExpress :init) r)) r))
    )
   (send-super :init)
   (setq _io_express_logic (round __io_express_logic))
   (setq _io_express __io_express)
   self)
  (:io_express_logic
   (&optional __io_express_logic)
   (if __io_express_logic (setq _io_express_logic __io_express_logic)) _io_express_logic)
  (:io_express
   (&rest __io_express)
   (if (keywordp (car __io_express))
       (send* _io_express __io_express)
     (progn
       (if __io_express (setq _io_express (car __io_express)))
       _io_express)))
  (:serialization-length
   ()
   (+
    ;; uint8 _io_express_logic
    1
    ;; lebai_msgs/IOConditionalExpress[] _io_express
    (apply #'+ (send-all _io_express :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _io_express_logic
       (write-byte _io_express_logic s)
     ;; lebai_msgs/IOConditionalExpress[] _io_express
     (write-long (length _io_express) s)
     (dolist (elem _io_express)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _io_express_logic
     (setq _io_express_logic (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; lebai_msgs/IOConditionalExpress[] _io_express
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _io_express (let (r) (dotimes (i n) (push (instance lebai_msgs::IOConditionalExpress :init) r)) r))
     (dolist (elem- _io_express)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get lebai_msgs::UntilInfo :md5sum-) "0907ad90f772aaa5fd1b8f10a92d018a")
(setf (get lebai_msgs::UntilInfo :datatype-) "lebai_msgs/UntilInfo")
(setf (get lebai_msgs::UntilInfo :definition-)
      "uint8 io_express_logic
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



(provide :lebai_msgs/UntilInfo "0907ad90f772aaa5fd1b8f10a92d018a")


