// Generated by gencpp from file lebai_msgs/GripperStatus.msg
// DO NOT EDIT!


#ifndef LEBAI_MSGS_MESSAGE_GRIPPERSTATUS_H
#define LEBAI_MSGS_MESSAGE_GRIPPERSTATUS_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace lebai_msgs
{
template <class ContainerAllocator>
struct GripperStatus_
{
  typedef GripperStatus_<ContainerAllocator> Type;

  GripperStatus_()
    : position(0.0)
    , force(0.0)  {
    }
  GripperStatus_(const ContainerAllocator& _alloc)
    : position(0.0)
    , force(0.0)  {
  (void)_alloc;
    }



   typedef double _position_type;
  _position_type position;

   typedef double _force_type;
  _force_type force;





  typedef boost::shared_ptr< ::lebai_msgs::GripperStatus_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::lebai_msgs::GripperStatus_<ContainerAllocator> const> ConstPtr;

}; // struct GripperStatus_

typedef ::lebai_msgs::GripperStatus_<std::allocator<void> > GripperStatus;

typedef boost::shared_ptr< ::lebai_msgs::GripperStatus > GripperStatusPtr;
typedef boost::shared_ptr< ::lebai_msgs::GripperStatus const> GripperStatusConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::lebai_msgs::GripperStatus_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::lebai_msgs::GripperStatus_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::lebai_msgs::GripperStatus_<ContainerAllocator1> & lhs, const ::lebai_msgs::GripperStatus_<ContainerAllocator2> & rhs)
{
  return lhs.position == rhs.position &&
    lhs.force == rhs.force;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::lebai_msgs::GripperStatus_<ContainerAllocator1> & lhs, const ::lebai_msgs::GripperStatus_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace lebai_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::GripperStatus_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::GripperStatus_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::GripperStatus_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
{
  static const char* value()
  {
    return "fead2ec07015c5b0fb77c4988270a39b";
  }

  static const char* value(const ::lebai_msgs::GripperStatus_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xfead2ec07015c5b0ULL;
  static const uint64_t static_value2 = 0xfb77c4988270a39bULL;
};

template<class ContainerAllocator>
struct DataType< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
{
  static const char* value()
  {
    return "lebai_msgs/GripperStatus";
  }

  static const char* value(const ::lebai_msgs::GripperStatus_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 position\n"
"float64 force\n"
;
  }

  static const char* value(const ::lebai_msgs::GripperStatus_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.position);
      stream.next(m.force);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GripperStatus_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::lebai_msgs::GripperStatus_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::lebai_msgs::GripperStatus_<ContainerAllocator>& v)
  {
    s << indent << "position: ";
    Printer<double>::stream(s, indent + "  ", v.position);
    s << indent << "force: ";
    Printer<double>::stream(s, indent + "  ", v.force);
  }
};

} // namespace message_operations
} // namespace ros

#endif // LEBAI_MSGS_MESSAGE_GRIPPERSTATUS_H