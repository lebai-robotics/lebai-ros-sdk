;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::IOStatus)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'IOStatus (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::IOSTATUS")
  (make-package "LEBAI_MSGS::IOSTATUS"))

(in-package "ROS")
;;//! \htmlinclude IOStatus.msg.html


(intern "*VOLTAGETYPE*" (find-package "LEBAI_MSGS::IOSTATUS"))
(shadow '*VOLTAGETYPE* (find-package "LEBAI_MSGS::IOSTATUS"))
(defconstant lebai_msgs::IOStatus::*VOLTAGETYPE* 0)
(intern "*CURRENTTYPE*" (find-package "LEBAI_MSGS::IOSTATUS"))
(shadow '*CURRENTTYPE* (find-package "LEBAI_MSGS::IOSTATUS"))
(defconstant lebai_msgs::IOStatus::*CURRENTTYPE* 1)
(defclass lebai_msgs::IOStatus
  :super ros::object
  :slots (_robot_din _robot_dout _robot_ain _robot_aout _robot_ain_type _robot_aout_type _flange_din _flange_dout ))

(defmethod lebai_msgs::IOStatus
  (:init
   (&key
    ((:robot_din __robot_din) (let (r) (dotimes (i 0) (push nil r)) r))
    ((:robot_dout __robot_dout) (let (r) (dotimes (i 0) (push nil r)) r))
    ((:robot_ain __robot_ain) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:robot_aout __robot_aout) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:robot_ain_type __robot_ain_type) (make-array 0 :initial-element 0 :element-type :char))
    ((:robot_aout_type __robot_aout_type) (make-array 0 :initial-element 0 :element-type :char))
    ((:flange_din __flange_din) (let (r) (dotimes (i 0) (push nil r)) r))
    ((:flange_dout __flange_dout) (let (r) (dotimes (i 0) (push nil r)) r))
    )
   (send-super :init)
   (setq _robot_din __robot_din)
   (setq _robot_dout __robot_dout)
   (setq _robot_ain __robot_ain)
   (setq _robot_aout __robot_aout)
   (setq _robot_ain_type __robot_ain_type)
   (setq _robot_aout_type __robot_aout_type)
   (setq _flange_din __flange_din)
   (setq _flange_dout __flange_dout)
   self)
  (:robot_din
   (&optional __robot_din)
   (if __robot_din (setq _robot_din __robot_din)) _robot_din)
  (:robot_dout
   (&optional __robot_dout)
   (if __robot_dout (setq _robot_dout __robot_dout)) _robot_dout)
  (:robot_ain
   (&optional __robot_ain)
   (if __robot_ain (setq _robot_ain __robot_ain)) _robot_ain)
  (:robot_aout
   (&optional __robot_aout)
   (if __robot_aout (setq _robot_aout __robot_aout)) _robot_aout)
  (:robot_ain_type
   (&optional __robot_ain_type)
   (if __robot_ain_type (setq _robot_ain_type __robot_ain_type)) _robot_ain_type)
  (:robot_aout_type
   (&optional __robot_aout_type)
   (if __robot_aout_type (setq _robot_aout_type __robot_aout_type)) _robot_aout_type)
  (:flange_din
   (&optional __flange_din)
   (if __flange_din (setq _flange_din __flange_din)) _flange_din)
  (:flange_dout
   (&optional __flange_dout)
   (if __flange_dout (setq _flange_dout __flange_dout)) _flange_dout)
  (:serialization-length
   ()
   (+
    ;; bool[] _robot_din
    (* 1    (length _robot_din)) 4
    ;; bool[] _robot_dout
    (* 1    (length _robot_dout)) 4
    ;; float32[] _robot_ain
    (* 4    (length _robot_ain)) 4
    ;; float32[] _robot_aout
    (* 4    (length _robot_aout)) 4
    ;; uint8[] _robot_ain_type
    (* 1    (length _robot_ain_type)) 4
    ;; uint8[] _robot_aout_type
    (* 1    (length _robot_aout_type)) 4
    ;; bool[] _flange_din
    (* 1    (length _flange_din)) 4
    ;; bool[] _flange_dout
    (* 1    (length _flange_dout)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool[] _robot_din
     (write-long (length _robot_din) s)
     (dotimes (i (length _robot_din))
       (if (elt _robot_din i) (write-byte -1 s) (write-byte 0 s))
       )
     ;; bool[] _robot_dout
     (write-long (length _robot_dout) s)
     (dotimes (i (length _robot_dout))
       (if (elt _robot_dout i) (write-byte -1 s) (write-byte 0 s))
       )
     ;; float32[] _robot_ain
     (write-long (length _robot_ain) s)
     (dotimes (i (length _robot_ain))
       (sys::poke (elt _robot_ain i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _robot_aout
     (write-long (length _robot_aout) s)
     (dotimes (i (length _robot_aout))
       (sys::poke (elt _robot_aout i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; uint8[] _robot_ain_type
     (write-long (length _robot_ain_type) s)
     (princ _robot_ain_type s)
     ;; uint8[] _robot_aout_type
     (write-long (length _robot_aout_type) s)
     (princ _robot_aout_type s)
     ;; bool[] _flange_din
     (write-long (length _flange_din) s)
     (dotimes (i (length _flange_din))
       (if (elt _flange_din i) (write-byte -1 s) (write-byte 0 s))
       )
     ;; bool[] _flange_dout
     (write-long (length _flange_dout) s)
     (dotimes (i (length _flange_dout))
       (if (elt _flange_dout i) (write-byte -1 s) (write-byte 0 s))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool[] _robot_din
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _robot_din (make-list n))
     (dotimes (i n)
     (setf (elt _robot_din i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;; bool[] _robot_dout
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _robot_dout (make-list n))
     (dotimes (i n)
     (setf (elt _robot_dout i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;; float32[] _robot_ain
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _robot_ain (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _robot_ain i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _robot_aout
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _robot_aout (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _robot_aout i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; uint8[] _robot_ain_type
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _robot_ain_type (make-array n :element-type :char))
     (replace _robot_ain_type buf :start2 ptr-) (incf ptr- n))
   ;; uint8[] _robot_aout_type
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _robot_aout_type (make-array n :element-type :char))
     (replace _robot_aout_type buf :start2 ptr-) (incf ptr- n))
   ;; bool[] _flange_din
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _flange_din (make-list n))
     (dotimes (i n)
     (setf (elt _flange_din i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;; bool[] _flange_dout
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _flange_dout (make-list n))
     (dotimes (i n)
     (setf (elt _flange_dout i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;;
   self)
  )

(setf (get lebai_msgs::IOStatus :md5sum-) "50c134754be339b506d0926e86b51aa1")
(setf (get lebai_msgs::IOStatus :datatype-) "lebai_msgs/IOStatus")
(setf (get lebai_msgs::IOStatus :definition-)
      "bool[] robot_din
bool[] robot_dout
float32[] robot_ain
float32[] robot_aout
uint8[] robot_ain_type
uint8[] robot_aout_type
bool[] flange_din
bool[] flange_dout

uint8 VOLTAGETYPE=0
uint8 CURRENTTYPE=1

")



(provide :lebai_msgs/IOStatus "50c134754be339b506d0926e86b51aa1")


