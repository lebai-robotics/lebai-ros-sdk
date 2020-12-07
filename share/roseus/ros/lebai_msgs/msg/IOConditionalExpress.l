;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::IOConditionalExpress)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'IOConditionalExpress (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS")
  (make-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))

(in-package "ROS")
;;//! \htmlinclude IOConditionalExpress.msg.html


(intern "*GROUP_ROBOT*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*GROUP_ROBOT* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*GROUP_ROBOT* 0)
(intern "*GROUP_FLANGE*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*GROUP_FLANGE* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*GROUP_FLANGE* 1)
(intern "*TYPE_ANALOG*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*TYPE_ANALOG* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*TYPE_ANALOG* 0)
(intern "*TYPE_DIGITAL*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*TYPE_DIGITAL* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*TYPE_DIGITAL* 1)
(intern "*LOGIC_OP_GT*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*LOGIC_OP_GT* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*LOGIC_OP_GT* 0)
(intern "*LOGIC_OP_GE*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*LOGIC_OP_GE* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*LOGIC_OP_GE* 1)
(intern "*LOGIC_OP_EQ*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*LOGIC_OP_EQ* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*LOGIC_OP_EQ* 2)
(intern "*LOGIC_OP_NE*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*LOGIC_OP_NE* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*LOGIC_OP_NE* 3)
(intern "*LOGIC_OP_LT*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*LOGIC_OP_LT* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*LOGIC_OP_LT* 4)
(intern "*LOGIC_OP_LE*" (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(shadow '*LOGIC_OP_LE* (find-package "LEBAI_MSGS::IOCONDITIONALEXPRESS"))
(defconstant lebai_msgs::IOConditionalExpress::*LOGIC_OP_LE* 5)
(defclass lebai_msgs::IOConditionalExpress
  :super ros::object
  :slots (_group _pin _type _float_value _uint_value _logic_operation ))

(defmethod lebai_msgs::IOConditionalExpress
  (:init
   (&key
    ((:group __group) 0)
    ((:pin __pin) 0)
    ((:type __type) 0)
    ((:float_value __float_value) 0.0)
    ((:uint_value __uint_value) 0)
    ((:logic_operation __logic_operation) 0)
    )
   (send-super :init)
   (setq _group (round __group))
   (setq _pin (round __pin))
   (setq _type (round __type))
   (setq _float_value (float __float_value))
   (setq _uint_value (round __uint_value))
   (setq _logic_operation (round __logic_operation))
   self)
  (:group
   (&optional __group)
   (if __group (setq _group __group)) _group)
  (:pin
   (&optional __pin)
   (if __pin (setq _pin __pin)) _pin)
  (:type
   (&optional __type)
   (if __type (setq _type __type)) _type)
  (:float_value
   (&optional __float_value)
   (if __float_value (setq _float_value __float_value)) _float_value)
  (:uint_value
   (&optional __uint_value)
   (if __uint_value (setq _uint_value __uint_value)) _uint_value)
  (:logic_operation
   (&optional __logic_operation)
   (if __logic_operation (setq _logic_operation __logic_operation)) _logic_operation)
  (:serialization-length
   ()
   (+
    ;; uint32 _group
    4
    ;; uint32 _pin
    4
    ;; uint32 _type
    4
    ;; float64 _float_value
    8
    ;; uint8 _uint_value
    1
    ;; uint8 _logic_operation
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _group
       (write-long _group s)
     ;; uint32 _pin
       (write-long _pin s)
     ;; uint32 _type
       (write-long _type s)
     ;; float64 _float_value
       (sys::poke _float_value (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; uint8 _uint_value
       (write-byte _uint_value s)
     ;; uint8 _logic_operation
       (write-byte _logic_operation s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _group
     (setq _group (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _pin
     (setq _pin (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; uint32 _type
     (setq _type (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64 _float_value
     (setq _float_value (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; uint8 _uint_value
     (setq _uint_value (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _logic_operation
     (setq _logic_operation (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get lebai_msgs::IOConditionalExpress :md5sum-) "35d2fc6b432f8da8c61c0faaba79afff")
(setf (get lebai_msgs::IOConditionalExpress :datatype-) "lebai_msgs/IOConditionalExpress")
(setf (get lebai_msgs::IOConditionalExpress :definition-)
      "uint32 group
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



(provide :lebai_msgs/IOConditionalExpress "35d2fc6b432f8da8c61c0faaba79afff")


