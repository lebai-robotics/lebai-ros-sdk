
(cl:in-package :asdf)

(defsystem "lebai_msgs-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :industrial_msgs-msg
               :lebai_msgs-msg
)
  :components ((:file "_package")
    (:file "MoveCircle" :depends-on ("_package_MoveCircle"))
    (:file "_package_MoveCircle" :depends-on ("_package"))
    (:file "MoveJoint" :depends-on ("_package_MoveJoint"))
    (:file "_package_MoveJoint" :depends-on ("_package"))
    (:file "MoveLine" :depends-on ("_package_MoveLine"))
    (:file "_package_MoveLine" :depends-on ("_package"))
    (:file "SetAMode" :depends-on ("_package_SetAMode"))
    (:file "_package_SetAMode" :depends-on ("_package"))
    (:file "SetAO" :depends-on ("_package_SetAO"))
    (:file "_package_SetAO" :depends-on ("_package"))
    (:file "SetDO" :depends-on ("_package_SetDO"))
    (:file "_package_SetDO" :depends-on ("_package"))
    (:file "SetGripper" :depends-on ("_package_SetGripper"))
    (:file "_package_SetGripper" :depends-on ("_package"))
  ))